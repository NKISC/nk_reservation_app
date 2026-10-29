import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from backend import addition, classroom_management, query
from fastapi.testclient import TestClient


class ClassroomManagementTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir="/tmp/opencode")
        self.old = os.getcwd()
        os.chdir(self.tmp.name)
        with sqlite3.connect("database.db") as db:
            db.executescript("""
                CREATE TABLE classroom (id TEXT PRIMARY KEY, display TEXT, place TEXT, pic_url TEXT, func_tag TEXT);
                CREATE TABLE user_info (id TEXT PRIMARY KEY, display TEXT, permission TEXT, register_num INTEGER DEFAULT 0);
                CREATE TABLE record (id INTEGER, classroom_id TEXT, noon INTEGER, applicant_id TEXT, time_stamp INTEGER);
                CREATE TABLE cyclical_record (record_id TEXT);
                INSERT INTO user_info(id,display,permission) VALUES
                    ('user','User','*,'), ('admin','Admin','admin,'), ('not-admin','Not Admin','notadmin,');
            """)
        with open("recent_id", "w") as f:
            f.write("1")

    def tearDown(self):
        os.chdir(self.old)
        self.tmp.cleanup()

    def payload(self, **kw):
        result = dict(id="room", display="Room", place="south", pic_url="", func_tag="club", available=True)
        result.update(kw)
        return result

    def test_add_edit_disable_reenable_and_history(self):
        self.assertTrue(classroom_management.manage(self.payload())["success"])
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO record VALUES (1,'room',0,'user',1)")
        self.assertEqual(classroom_management.manage(self.payload(display="Changed", func_tag="a,,b"), True), {"success": True})
        self.assertEqual(query.query_classroom({})[0]["func_tag"], "a,b,")
        classroom_management.manage(self.payload(available=False), True)
        self.assertFalse(query.query_classroom({})[0]["available"])
        self.assertEqual(query.query_classroom({}, True), [])
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM record WHERE id=1").fetchone()[0], 1)
        classroom_management.manage(self.payload(available=True), True)
        self.assertEqual(len(query.query_classroom({}, True)), 1)

    def test_validation_and_edit_unknown(self):
        self.assertEqual(classroom_management.manage(self.payload(id="bad,id"))["error"], "invalid_id")
        self.assertEqual(classroom_management.manage(self.payload(place="invalid"))["error"], "invalid_place")
        self.assertEqual(classroom_management.manage(self.payload(display=" "))["error"], "invalid_display")
        self.assertEqual(classroom_management.manage(self.payload(), True)["error"], "unknown_classroom")

    def test_auth_uses_fresh_code_openid_permission(self):
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            self.assertTrue(classroom_management.authorized("fresh"))
        with patch("backend.utils.exchange_admin_code", return_value="user"):
            self.assertFalse(classroom_management.authorized("fresh"))
        with patch("backend.utils.exchange_admin_code", return_value="not-admin"):
            self.assertFalse(classroom_management.authorized("fresh"))
        with patch("backend.utils.exchange_admin_code", return_value=None):
            self.assertFalse(classroom_management.authorized("invalid"))

    def test_wechat_code_exchange_success_and_fail_closed_cases(self):
        from backend import utils
        with open("appid", "w") as f:
            f.write("test-app")
        with open("appSecret", "w") as f:
            f.write("test-secret")
        class Response:
            def __init__(self, payload):
                self.payload = payload
            def raise_for_status(self):
                return None
            def json(self):
                return self.payload
        with patch("backend.utils.requests.get", return_value=Response({"openid": "admin"})) as get:
            self.assertEqual(utils.exchange_admin_code("fresh-code"), "admin")
            self.assertEqual(get.call_args.kwargs["params"]["js_code"], "fresh-code")
        with patch("backend.utils.requests.get", return_value=Response({"errcode": 401, "errmsg": "bad"})):
            self.assertIsNone(utils.exchange_admin_code("bad-code"))
        with patch("backend.utils.requests.get", side_effect=OSError("offline")):
            self.assertIsNone(utils.exchange_admin_code("offline-code"))

    def test_route_contract_and_legacy_availability_default(self):
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO classroom VALUES ('legacy','Legacy','north','','')")
        self.assertTrue(query.query_classroom({})[0]["available"])
        from backend.app import app
        client = TestClient(app)
        body = {"code": "fresh", "id": "new-room", "display": "New Room",
                "place": "office2", "pic_url": "", "func_tag": "", "available": True}
        with patch("backend.utils.exchange_admin_code", return_value="not-admin"):
            denied = client.post("/addition/classroom", json=body)
        self.assertEqual(denied.json(), {"success": False, "error": "unauthorized"})
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            response = client.post("/addition/classroom", json=body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            duplicate = client.post("/addition/classroom", json=body)
        self.assertEqual(duplicate.json(), {"success": False, "error": "duplicate_id"})
        self.assertTrue(any(row["id"] == "new-room" for row in query.query_classroom({})))
        result = client.post("/query/classroom", json={"cond": {}}).json()
        row = next(row for row in result if row["id"] == "new-room")
        self.assertIs(row["available"], True)
        self.assertIsInstance(row["available"], bool)
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO record VALUES (7,'new-room',0,'user',1)")
        legacy = client.post("/delete/classroom/", json={"cond": {"id": "new-room"}})
        missing = client.post("/delete/classroom/", json={"code": "fresh", "cond": {"id": "new-room"}})
        empty = client.post("/delete/classroom/", json={"code": "fresh", "id": "  "})
        self.assertIn(legacy.status_code, (200, 422))
        self.assertEqual(missing.status_code, 422)
        self.assertEqual(empty.json(), {"success": False, "error": "invalid_id"})
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM classroom WHERE id='new-room'").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM record WHERE classroom_id='new-room'").fetchone()[0], 1)
        edit = dict(body, display="Disabled Room", available=False)
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            disabled = client.post("/alter/classroom", json=edit)
        self.assertEqual(disabled.json(), {"success": True})
        filtered = client.post("/query/classroom", json={"cond": {}, "available_only": True}).json()
        self.assertFalse(any(item["id"] == "new-room" for item in filtered))
        history = client.post("/query/classroom", json={"cond": {}}).json()
        disabled_row = next(item for item in history if item["id"] == "new-room")
        self.assertIs(disabled_row["available"], False)
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM record WHERE classroom_id='new-room'").fetchone()[0], 1)
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            deleted = client.post("/delete/classroom/", json={"code": "fresh", "id": "new-room"})
        self.assertEqual(deleted.json(), {"success": True, "deleted_records": 1})
        self.assertFalse(any(item["id"] == "new-room" for item in query.query_classroom({})))
        self.assertEqual(client.get("/connection").json(), {"status": "ok"})

    def test_direct_and_cyclical_unavailable_have_no_side_effects(self):
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO classroom VALUES ('room','Room','south','','')")
        with sqlite3.connect("database.db") as db:
            classroom_management.ensure_availability(db)
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO classroom_availability(id, available) VALUES ('room', 0)")
        self.assertEqual(addition.add_records("missing", False, "user", 1)["err_code"], 602)
        self.assertEqual(addition.add_records("room", False, "user", 1)["error"], "classroom_unavailable")
        with sqlite3.connect("database.db") as db:
            self.assertEqual(addition.add_records("room", False, "user", 1, db=db)["err_code"], 602)
        self.assertEqual(addition.add_cyclical_records("missing", False, "user", 1, 10, [False] * 7)["err_code"], 602)
        self.assertEqual(addition.add_cyclical_records("room", False, "user", 1, 10, [False] * 7)["err_code"], 602)
        with open("recent_id") as id_file:
            self.assertEqual(id_file.read(), "1")
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM record").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM cyclical_record").fetchone()[0], 0)

    def test_enabled_direct_booking_still_succeeds_with_supplied_connection(self):
        with sqlite3.connect("database.db") as db:
            db.executescript("""
                CREATE TABLE permission (id TEXT, display TEXT, classrooms TEXT);
                INSERT INTO permission VALUES ('*','All','*,');
                INSERT INTO classroom VALUES ('room','Room','south','','');
            """)
        timestamp = 4102444800
        with sqlite3.connect("database.db") as db:
            result = addition.add_records("room", False, "user", timestamp, db=db)
        self.assertEqual(result, {"success": True})
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT classroom_id FROM record").fetchone()[0], "room")


if __name__ == "__main__":
    unittest.main()
