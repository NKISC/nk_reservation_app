import sqlite3
from typing import *


def construct_condition(cond: dict[str, Any]) -> str:
    ret = ""
    cond_keys = list(cond.keys())
    for i in range(len(cond_keys)):
        ret += f"{cond_keys[i]}=:{cond_keys[i]}"
        if i != len(cond_keys) - 1:
            ret += ","

    return ret



def query_classroom(cond: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Query the classroom information.
    :param cond: A dictionary containing the filters that select the classrooms to return.
        id (int): The classroom id.
        display (str): The display name of the classroom.
        place (str): The place of the classroom.
        pic_url (str): UNSUPPORTED, DO NOT USE.
        func_tag (str): UNSUPPORTED, DO NOT USE.
    :return: A list of classroom information.
    """
    # TODO: function tag support
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    if len(cond) != 0:
        cursor.execute("select * from classroom where " + construct_condition(cond), cond)
    else:
        cursor.execute("select * from classroom")
    rows = cursor.fetchall()
    heads = cursor.execute("pragma table_info(classroom)").fetchall()
    ret = []
    for row in rows:
        p = {}
        for i in range(len(heads)):
            p[heads[i][1]] = row[i]
        ret.append(p)

    return ret
