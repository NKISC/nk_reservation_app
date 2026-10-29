import sqlite3
from typing import Any, Dict
from backend import utils
from backend.utils import handle_db_error

def delete_from_table(table: str, x: Dict[str, Any]) -> Dict[str, Any]:
    """
    General deletion function.
    :param table: Table name
    :param x: Condition dictionary
    :return: Results
    """
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            if x:
                cursor.execute(
                    f"DELETE FROM {table} WHERE {utils.construct_condition(x)}",
                    utils.construct_params(x)
                )
            else:
                cursor.execute(
                    f"DELETE FROM {table} WHERE true"
                )
        return {"success": True}
    except Exception as e:
        return handle_db_error(e)

# 针对不同表的接口
def delete_record(x: Dict[str, Any]) -> Dict[str, Any]:
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            applicant_id = cursor.execute("select * from record where id = :id", {"id": x["id"]}).fetchone()[3]
            cursor.execute("update user_info set register_num = register_num - 1 where id = :id",
                           {"id": applicant_id})
            cursor.close()
        return delete_from_table("record", x)
    except Exception as e:
        return handle_db_error(e)


def delete_user(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("user_info", x)


def delete_classroom(classroom_id: str) -> Dict[str, Any]:
    """Permanently remove one classroom and its dependent reservation data."""
    if not isinstance(classroom_id, str) or not classroom_id.strip():
        return {"success": False, "error": "invalid_id"}
    try:
        with sqlite3.connect("database.db", timeout=30) as db:
            db.execute("BEGIN IMMEDIATE")
            if not db.execute("SELECT 1 FROM classroom WHERE id=?", (classroom_id,)).fetchone():
                return {"success": False, "error": "unknown_classroom"}
            removed_ids = {str(row[0]) for row in db.execute(
                "SELECT id FROM record WHERE classroom_id=?", (classroom_id,)).fetchall()}
            counts = db.execute(
                "SELECT applicant_id, COUNT(*) FROM record WHERE classroom_id=? GROUP BY applicant_id",
                (classroom_id,)).fetchall()
            for applicant_id, count in counts:
                db.execute("UPDATE user_info SET register_num=MAX(0, register_num-?) WHERE id=?",
                           (count, applicant_id))
            db.execute("DELETE FROM record WHERE classroom_id=?", (classroom_id,))

            # Match whole comma-delimited tokens only; preserve unrelated group IDs.
            for (rowid, value) in db.execute("SELECT rowid, record_id FROM cyclical_record").fetchall():
                tokens_all = (value or "").split(",")
                tokens = [token for token in tokens_all if token and token not in removed_ids]
                if len(tokens) != len([token for token in tokens_all if token]):
                    if tokens:
                        db.execute("UPDATE cyclical_record SET record_id=? WHERE rowid=?",
                                   (",".join(tokens) + ",", rowid))
                    else:
                        db.execute("DELETE FROM cyclical_record WHERE rowid=?", (rowid,))

            tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "classroom_availability" in tables:
                db.execute("DELETE FROM classroom_availability WHERE id=?", (classroom_id,))
            if "permission" in tables:
                cols = {row[1] for row in db.execute("PRAGMA table_info(permission)")}
                if {"classrooms"}.issubset(cols):
                    for rowid, value in db.execute("SELECT rowid, classrooms FROM permission").fetchall():
                        tokens_all = (value or "").split(",")
                        tokens = [token for token in tokens_all if token and (token == "*" or token != classroom_id)]
                        if len(tokens) != len([token for token in tokens_all if token]):
                            db.execute("UPDATE permission SET classrooms=? WHERE rowid=?",
                                       ((",".join(tokens) + ",") if tokens else "", rowid))
            db.execute("DELETE FROM classroom WHERE id=?", (classroom_id,))
        return {"success": True, "deleted_records": len(removed_ids)}
    except Exception:
        return {"success": False, "error": "database_error"}


def delete_cyclical(initiator: str) -> Dict[str, Any]:
    from backend import query
    cyc_records = query.get_cyclical({"record_id": [initiator]})[0]["record_id"].split(",")
    del cyc_records[-1]
    for rid in cyc_records:
        rid = int(rid)
        if query.query_record({"id": rid}):
            ret = delete_record({"id": rid})
            if not ret["success"]:
                return ret
    return {"success": True}


def delete_permission_password(password: str) -> Dict[str, Any]:
    with open("password_perm_mapping") as ppm:
        entries = ppm.read().strip().splitlines()
    for entry in entries:
        if entry.split(" ")[0] == password:
            entries.remove(entry)
    with open(f"password_perm_mapping", "w") as ppm:
        ppm.write("\n".join(entries))
    return {"success": True}
