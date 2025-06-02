import sqlite3
from backend import query
from backend.query import judge_conflict


def alter_user(uid: str, display: str = None, permission: list[str] = None):
    user = query.query_user({"id": uid})[0]
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            cursor.execute("update user_info set display = :display, permission = :permission where id = :id", {
                "display": display if display else user["display"],
                "permission": (",".join(permission) + ",") if permission else user["permission"],
                "id": uid,
            })
        return {"success": True}
    except sqlite3.IntegrityError as e:
        return {"success": False, "err_code": 100, "error": f"Integrity error: {e}"}
    except sqlite3.OperationalError as e:
        return {"success": False, "err_code": 100, "error": f"Operational error: {e}"}
    except sqlite3.DatabaseError as e:
        return {"success": False, "err_code": 100, "error": f"Database error: {e}"}
    except Exception as e:
        return {"success": False, "err_code": 100, "error": f"Unknown error: {e}"}


def alter_record(record_id: int, noon: bool, time_stamp: int):
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            record = query.query_record({"id": record_id})[0]
            if judge_conflict(record["classroom_id"], noon, time_stamp):
                return {"success": False, "err_code": 601, "error": "classroom_already_reserved"}
            cursor.execute("update record set noon = :noon, time_stamp = :time_stamp where id = :record_id",
                           {"noon": noon, "time_stamp": time_stamp, "record_id": record_id})
        return {"success": True}
    except sqlite3.IntegrityError as e:
        return {"success": False, "err_code": 100, "error": f"Integrity error: {e}"}
    except sqlite3.OperationalError as e:
        return {"success": False, "err_code": 100, "error": f"Operational error: {e}"}
    except sqlite3.DatabaseError as e:
        return {"success": False, "err_code": 100, "error": f"Database error: {e}"}
    except Exception as e:
        return {"success": False, "err_code": 100, "error": f"Unknown error: {e}"}