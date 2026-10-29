import os
import sqlite3
import tempfile
import unittest
import threading
from unittest.mock import patch

from fastapi.testclient import TestClient
from backend.app import app


class ClassroomDeletionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir="/tmp/opencode")
        self.old = os.getcwd()
        os.chdir(self.tmp.name)
        with sqlite3.connect("database.db") as db:
            db.executescript("""
                CREATE TABLE classroom(id TEXT PRIMARY KEY, display TEXT, place TEXT, pic_url TEXT, func_tag TEXT);
                CREATE TABLE record(id INTEGER, classroom_id TEXT, noon INTEGER, applicant_id TEXT, time_stamp INTEGER);
                CREATE TABLE cyclical_record(record_id TEXT);
                CREATE TABLE user_info(id TEXT PRIMARY KEY, permission TEXT, register_num INTEGER);
                CREATE TABLE classroom_availability(id TEXT, available INTEGER);
                CREATE TABLE permission(id TEXT, classrooms TEXT);
                INSERT INTO classroom VALUES ('room1','','','',''),('room10','','','','');
                INSERT INTO user_info VALUES ('admin','admin,',0),('a','*',1),('b','*',0);
                INSERT INTO record VALUES (1,'room1',0,'a',0),(11,'room10',0,'b',0),(2,'room1',0,'b',0);
                INSERT INTO cyclical_record VALUES ('1,11,2,'),('1,2,'),('11,');
                INSERT INTO classroom_availability VALUES ('room1',0),('room10',1);
                INSERT INTO permission VALUES ('u','*,room1,room10,');
            """)
        self.client = TestClient(app)

    def tearDown(self):
        os.chdir(self.old)
        self.tmp.cleanup()

    def call(self, code="fresh", ident="room1"):
        with patch("backend.utils.exchange_admin_code", return_value="admin"):
            return self.client.post("/delete/classroom/", json={"code": code, "id": ident})

    def test_deletes_only_target_and_cleans_associations(self):
        self.assertEqual(self.call().json(), {"success": True, "deleted_records": 2})
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT id FROM classroom").fetchall(), [("room10",)])
            self.assertEqual(db.execute("SELECT id FROM record").fetchall(), [(11,)])
            self.assertEqual(db.execute("SELECT record_id FROM cyclical_record ORDER BY rowid").fetchall(),
                             [("11,",), ("11,",)])
            self.assertEqual(db.execute("SELECT id,register_num FROM user_info ORDER BY id").fetchall(),
                             [("a", 0), ("admin", 0), ("b", 0)])
            self.assertEqual(db.execute("SELECT id FROM classroom_availability").fetchall(), [("room10",)])
            self.assertEqual(db.execute("SELECT classrooms FROM permission").fetchone()[0], "*,room10,")

    def test_unauthorized_invalid_unknown_and_database_failure(self):
        with patch("backend.utils.exchange_admin_code", return_value="nobody"):
            denied = self.client.post("/delete/classroom/", json={"code": "bad", "id": "room1"})
        self.assertEqual(denied.json(), {"success": False, "error": "unauthorized"})
        self.assertEqual(self.call(ident=" ").json()["error"], "invalid_id")
        self.assertEqual(self.call(ident="missing").json()["error"], "unknown_classroom")
        with sqlite3.connect("database.db") as db:
            db.execute("CREATE TRIGGER fail_delete BEFORE DELETE ON classroom BEGIN SELECT RAISE(ABORT, 'no'); END")
        self.assertEqual(self.call().json()["error"], "database_error")
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM record WHERE classroom_id='room1'").fetchone()[0], 2)
            self.assertEqual(db.execute("SELECT register_num FROM user_info WHERE id='b'").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT record_id FROM cyclical_record ORDER BY rowid").fetchall(),
                             [("1,11,2,",), ("1,2,",), ("11,",)])
            self.assertEqual(db.execute("SELECT id,available FROM classroom_availability ORDER BY id").fetchall(),
                             [("room1", 0), ("room10", 1)])
            self.assertEqual(db.execute("SELECT classrooms FROM permission").fetchone()[0], "*,room1,room10,")

    def test_no_bookings_clamp_shared_image_recent_id_and_repeat_unknown(self):
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO classroom VALUES ('empty','', '', 'shared.jpg','')")
        with open("recent_id", "w") as f:
            f.write("998")
        with open("shared.jpg", "wb") as f:
            f.write(b"shared")
        self.assertEqual(self.call(ident="empty").json(), {"success": True, "deleted_records": 0})
        self.assertEqual(self.call().json(), {"success": True, "deleted_records": 2})
        self.assertEqual(self.call().json(), {"success": False, "error": "unknown_classroom"})
        with open("recent_id") as f:
            self.assertEqual(f.read(), "998")
        # Image is not managed/deleted by classroom removal; shared assets remain intact.
        self.assertTrue(os.path.exists("shared.jpg"))

    def test_optional_association_tables_and_null_fields(self):
        with sqlite3.connect("database.db") as db:
            db.execute("UPDATE cyclical_record SET record_id=NULL WHERE rowid=1")
            db.execute("DROP TABLE classroom_availability")
            db.execute("DROP TABLE permission")
        self.assertEqual(self.call().json(), {"success": True, "deleted_records": 2})

    def test_wildcard_classroom_permission_token_is_retained(self):
        with sqlite3.connect("database.db") as db:
            db.execute("INSERT INTO classroom VALUES ('*','','','','')")
            db.execute("INSERT INTO permission VALUES ('wild','*,room1,')")
        self.assertEqual(self.call(ident="*").json(), {"success": True, "deleted_records": 0})
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT classrooms FROM permission WHERE id='wild'").fetchone()[0], "*,room1,")

    def test_immediate_write_lock_serializes_booking_check_and_deletion(self):
        # A booking holding its availability check inside BEGIN IMMEDIATE prevents another
        # writer from deleting the classroom until the booking transaction commits.
        ready, release = threading.Event(), threading.Event()
        error = []
        with sqlite3.connect("database.db") as db:
            db.execute("UPDATE classroom_availability SET available=1 WHERE id='room1'")
        def booking_transaction():
            try:
                with sqlite3.connect("database.db", timeout=1) as db:
                    db.execute("BEGIN IMMEDIATE")
                    from backend.addition import _classroom_available
                    self.assertTrue(_classroom_available("room1", db))
                    ready.set()
                    release.wait(2)
                    db.execute("INSERT INTO record VALUES (99,'room1',0,'a',0)")
            except Exception as exc:
                error.append(exc)
                ready.set()
        thread = threading.Thread(target=booking_transaction)
        thread.start()
        self.assertTrue(ready.wait(2))
        self.assertEqual(error, [])
        with sqlite3.connect("database.db", timeout=0) as other:
            with self.assertRaises(sqlite3.OperationalError):
                other.execute("BEGIN IMMEDIATE")
        release.set()
        thread.join(2)
        self.assertFalse(thread.is_alive())
        self.assertEqual(error, [])
        self.assertEqual(self.call().json(), {"success": True, "deleted_records": 3})
        with sqlite3.connect("database.db") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM record WHERE classroom_id='room1'").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
