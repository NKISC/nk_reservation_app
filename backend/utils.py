import sqlite3
import time


def update_record(db: sqlite3.Connection):
    """
    Delete outdated records.
    :return:
    """
    cursor = db.cursor()
    cursor.execute('delete from record where time_stamp < :threshold',
                   {"threshold": time.time() - 48 * 60 * 60})
    db.commit()
    return {"success": True}
