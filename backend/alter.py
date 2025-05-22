import sqlite3
from backend import query
from backend.query import judge_conflict


def alter_user(uid: str, display: str = None, permission: list[str] = None):
    user = query.query_user({"id": uid})[0]
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("update user_info set display = :display, permission = :permission where id = :id", {
            "display": display if display else user["display"],
            "permission": (",".join(permission) + ",") if permission else user["permission"],
            "id": uid,
        })

    return {"success": True}


def alter_record(record_id: int, noon: bool, time_stamp: int):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        record = query.query_record({"id": record_id})[0]
        if judge_conflict(record["classroom_id"], noon, time_stamp):
            return {"success": False, "err_code": 601}
        cursor.execute("update record set noon = :noon, time_stamp = :time_stamp where id = :record_id",
                       {"noon": noon, "time_stamp": time_stamp, "record_id": record_id})
        return {"success": True}
