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
            applicant_id = cursor.execute("select * from record where id = ?", (x["id"])).fetchone()[3]
            cursor.execute("update user_info set register_num = register_num - 1 where id = :id",
                           {"id": applicant_id})
            cursor.close()
        return delete_from_table("record", x)
    except Exception as e:
        return handle_db_error(e)


def delete_user(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("user_info", x)


def delete_classroom(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("classroom", x)


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
