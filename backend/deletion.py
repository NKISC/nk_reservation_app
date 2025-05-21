import sqlite3
from typing import *

from backend import utils


def delete_record(cond: dict[str, Any]) -> dict[str, Any]:
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        if cond:
            cursor.execute(f"delete from record where {utils.construct_condition(cond)}",
                           utils.construct_params(cond))
        else:
            cursor.execute("delete from record where true")
    return {"success": True}
