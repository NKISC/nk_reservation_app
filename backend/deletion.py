import sqlite3
from typing import Any, Dict
from backend import utils

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
                return {"success": False, "error": "删除条件不能为空，防止误删全部数据"}
        return {"success": True}
    except sqlite3.IntegrityError as e:
        return {"success": False, "error": f"Integrity error: {e}"}
    except sqlite3.OperationalError as e:
        return {"success": False, "error": f"Operational error: {e}"}
    except sqlite3.DatabaseError as e:
        return {"success": False, "error": f"Database error: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Unknown error: {e}"}

# 针对不同表的接口
def delete_record(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("record", x)

def delete_user(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("user_info", x)

def delete_classroom(x: Dict[str, Any]) -> Dict[str, Any]:
    return delete_from_table("classroom", x)