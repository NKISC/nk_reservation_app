import sqlite3
import time


def update_record():
    """
    Delete outdated records.
    :return:
    """
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute('delete from record where time_stamp < :threshold',
                       {"threshold": time.time() - 48 * 60 * 60})
