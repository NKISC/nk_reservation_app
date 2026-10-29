import io
import os
import sqlite3
import tempfile
import unittest
import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image

from backend.app import app
from backend import classroom_images


def make_image(fmt="JPEG", size=(24, 16), color="red", **save_options):
    image = Image.new("RGBA" if fmt == "PNG" else "RGB", size, color)
    output = io.BytesIO()
    image.save(output, format=fmt, **save_options)
    return output.getvalue()


class ClassroomImageUploadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir="/tmp/opencode")
        self.old = os.getcwd()
        os.chdir(self.tmp.name)
        with sqlite3.connect("database.db") as db:
            db.executescript("""
                CREATE TABLE user_info (id TEXT PRIMARY KEY, display TEXT, permission TEXT);
                CREATE TABLE classroom (id TEXT PRIMARY KEY, display TEXT, place TEXT, pic_url TEXT, func_tag TEXT);
            """)
            db.executemany("INSERT INTO user_info VALUES (?, ?, ?)", [
                ("admin", "Admin", "admin,"), ("not-admin", "No", "notadmin,"),
                ("near-admin", "Near", "superadmin,"),
            ])
        self.exchange = patch("backend.utils.exchange_admin_code", return_value="admin")
        self.exchange.start()
        self.client = TestClient(app)

    def tearDown(self):
        self.exchange.stop()
        os.chdir(self.old)
        self.tmp.cleanup()

    def upload(self, data, mime="application/octet-stream", code="good-code", **headers):
        request_headers = {"X-Wechat-Code": code, "Content-Type": mime, **headers}
        return self.client.post("/upload/classroom-image", content=data, headers=request_headers)

    def with_identity(self, identity, callback):
        with patch("backend.utils.exchange_admin_code", return_value=identity):
            return callback()

    def test_authorizes_fresh_exchanged_identity_against_exact_database_permission(self):
        data = make_image()
        for identity, expected in [("admin", True), ("not-admin", False), ("near-admin", False), (None, False)]:
            response = self.with_identity(identity, lambda: self.upload(data))
            self.assertEqual(response.json()["success"], expected)
        self.assertEqual(len(os.listdir("img")), 1)

    def test_jpeg_png_webp_are_normalized_and_served(self):
        formats = ["JPEG", "PNG"]
        if "WEBP" in Image.registered_extensions().values():
            formats.append("WEBP")
        for fmt in formats:
            with self.subTest(fmt=fmt):
                response = self.upload(make_image(fmt), "image/" + fmt.lower())
                self.assertTrue(response.json()["success"])
                ident = response.json()["pic_url"]
                self.assertRegex(ident, r"^classroom_[0-9a-f]{32}$")
                served = self.client.get(f"/img/{ident}")
                self.assertEqual(served.headers["content-type"], "image/jpeg")
                with Image.open(io.BytesIO(served.content)) as image:
                    self.assertEqual(image.format, "JPEG")

    def test_transparent_png_composites_on_white(self):
        data = make_image("PNG", size=(1, 1), color=(255, 0, 0, 0))
        ident = self.upload(data, "image/png").json()["pic_url"]
        pixel = Image.open(io.BytesIO(self.client.get(f"/img/{ident}").content)).convert("RGB").getpixel((0, 0))
        self.assertEqual(pixel, (255, 255, 255))

    def test_exif_orientation_applied_and_metadata_stripped(self):
        image = Image.new("RGB", (3, 2), "blue")
        image.getpixel((0, 0))
        exif = Image.Exif()
        exif[274] = 6
        exif[270] = "private metadata"
        output = io.BytesIO()
        image.save(output, format="JPEG", exif=exif)
        ident = self.upload(output.getvalue(), "image/jpeg").json()["pic_url"]
        with Image.open(f"img/{ident}.jpg") as saved:
            self.assertEqual(saved.size, (2, 3))
            self.assertNotIn(274, saved.getexif())
            self.assertNotIn("private metadata", str(saved.info))

    def test_upload_id_integrates_with_real_classroom_management(self):
        ident = self.upload(make_image()).json()["pic_url"]
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            response = self.client.post("/addition/classroom", json={
                "code": "good-code", "id": "room", "display": "Room", "place": "south",
                "pic_url": ident, "func_tag": "", "available": True,
            })
        self.assertEqual(response.json(), {"success": True})
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT pic_url FROM classroom WHERE id='room'").fetchone()[0], ident)

    def test_denial_and_invalid_uploads_leave_no_files(self):
        with patch("backend.classroom_management.authorized") as authorize:
            response = self.client.post("/upload/classroom-image", content=make_image())
            self.assertEqual(response.json(), {"success": False, "error": "unauthorized"})
            authorize.assert_not_called()
        response = self.with_identity("not-admin", lambda: self.upload(make_image()))
        self.assertEqual(response.json(), {"success": False, "error": "unauthorized"})
        for data, mime in [(b"not image", "application/octet-stream"), (make_image()[:30], "image/jpeg"),
                           (make_image(), "text/plain")]:
            self.assertEqual(self.upload(data, mime).json()["error"], "invalid_image")
        self.assertFalse(os.path.exists("img"))

    def test_image_limits_before_decode_and_body_stream_limit(self):
        oversized = self.upload(b"x" * (classroom_images.MAX_BYTES + 1))
        self.assertEqual(oversized.json()["error"], "image_too_large")
        # Explicitly exercise absent and under-reported Content-Length; Starlette's stream
        # receives the complete body despite either header value.
        for headers in ({"Content-Length": ""}, {"Content-Length": "1"}):
            response = self.upload(b"x" * (classroom_images.MAX_BYTES + 1), **headers)
            self.assertEqual(response.json()["error"], "image_too_large")
        huge = make_image("PNG", size=(5000, 5000))
        self.assertEqual(self.upload(huge, "image/png").json()["error"], "invalid_image")
        self.assertFalse(os.path.exists("img"))

    def test_helper_rejects_oversize_before_decode(self):
        with self.assertRaises(classroom_images.ImageTooLarge):
            classroom_images.normalize_and_store(b"x" * (classroom_images.MAX_BYTES + 1))

    def test_storage_failure_cleans_partial_file(self):
        os.mkdir("img")
        original_open = open

        def broken_open(path, mode="r", *args, **kwargs):
            if mode == "xb":
                original_open(path, mode, *args, **kwargs).close()
                raise OSError("disk failed")
            return original_open(path, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=broken_open):
            response = self.upload(make_image())
        self.assertEqual(response.json(), {"success": False, "error": "image_storage_error"})
        self.assertEqual(os.listdir("img"), [])

    def test_uuid_collision_does_not_overwrite_existing_image(self):
        os.mkdir("img")
        ident = "classroom_" + uuid.uuid4().hex
        existing = f"img/{ident}.jpg"
        with open(existing, "wb") as file:
            file.write(b"legacy")
        with patch("backend.classroom_images.uuid.uuid4", side_effect=[type("U", (), {"hex": ident[10:]})(),
                                                                          type("U", (), {"hex": uuid.uuid4().hex})()]):
            result = classroom_images.normalize_and_store(make_image())
        self.assertNotEqual(result, ident)
        with open(existing, "rb") as file:
            self.assertEqual(file.read(), b"legacy")


if __name__ == "__main__":
    unittest.main()
