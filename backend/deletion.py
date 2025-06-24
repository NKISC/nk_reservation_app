import sqlite3
from typing import Any, Dict
from backend import utils
from backend.utils import handle_db_error

def delete_from_table(table: str, x: Dict[str, Any]) -> Dict[str, Any]:
    """
    通用删除函数
    :param table: 表名
    :param x: 删除条件
    :return: 操作结果
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
    return delete_from_table("record", x)


def delete_user(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("user_info", x)


def delete_classroom(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("classroom", x)


def delete_cyclical(initiator: str) -> Dict[str, Any]:
    import query
    cyc_records = query.get_cyclical({"cyclical_id": initiator})[0]["record_id"].split(",")
    del cyc_records[-1]
    for rid in cyc_records:
        rid = int(rid)
        if query.query_record({"id": rid}):
            ret = delete_record({"id": rid})
            if not ret["success"]:
                return ret
    return {"success": True}
