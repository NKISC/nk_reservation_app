import sqlite3
from backend import query


def alter_user(uid: str, display: str = None, permission: list[str] = None):
    user = query.query_user({"id": uid})[0]
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("update user_info set display = :display, permission = :permission where id = :id", {
            "display": display if display else user["display"],
            "permission": (",".join(permission) + ",") if permission else user["permission"],
            "id": uid,
        })
