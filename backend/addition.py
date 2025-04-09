import sqlite3
import utils
from typing import *

def addition(db: sqlite3.Connection, classroom: str, noon: bool, applicant_id: str, time_stamp: int):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM record")
    idrows = cursor.fetchall()
    maxid = idrows[-1][0]
    cursor.execute("INSERT INTO [record] VALUES (maxid+1, classroom, noon, applicant_id, time_stamp)")