import sqlite3
import utils
from typing import *

def addition(db: sqlite3.Connection, classroom: str, noon: bool, applicant_id: str, time_stamp: int):
    cursor = db.cursor()
    # cursor.execute("SELECT id FROM record")
    # id_rows = cursor.fetchall()
    # max_id = id_rows[-1][0]
    cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                   {"id": id+1, "noon": noon, "classroom": classroom, "applicant_id": applicant_id, "time_stamp": time_stamp})