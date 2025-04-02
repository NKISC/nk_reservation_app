import sqlite3
import time


def update_record(db: sqlite3.Connection):
    """
    Delete outdated records.
    :return:
    """
    cursor = db.cursor()
    cursor.execute('delete from record where timestamp > :threshold',
                   {"threshold": time.time() + 24 * 60 * 60})
    return {"success": True}
