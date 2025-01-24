import sqlite3
from typing import *


generic_query_keys = ["func_tag", "pic_url"]


def construct_condition(cond: dict[str, Any]) -> str:
    ret = ""
    cond_keys = list(cond.keys())
    for i in range(len(cond_keys)):
        if cond_keys[i] in generic_query_keys:
            for j in range(len(cond[cond_keys[i]])):
                ret += f"{cond_keys[i]} like :{cond_keys[i]}{j}"
                if j != len(cond[cond_keys[i]]) - 1:
                    ret += " and "
        else:
            ret += f"{cond_keys[i]}=:{cond_keys[i]}"
        if i != len(cond_keys) - 1:
            ret += " and "

    return ret



def query_classroom(cond: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Query the classroom information.
    :param cond: A dictionary containing the filters that select the classrooms to return.
        id (int): The classroom id.
        display (str): The display name of the classroom.
        place (str): The place of the classroom.
        pic_url (list[str]): The pic_url(s) of the classroom.
        func_tag (list[str]): The function tag(s) of the classroom.
    :return: A list of classroom information.
    """
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    param = {}
    for k in cond.keys():
        if k in generic_query_keys:
            for i in range(len(cond[k])):
                param[str(k) + str(i)] = "%" + cond[k][i] + ",%"
        else:
            param[k] = cond[k]
    if len(cond) != 0:
        cursor.execute("select * from classroom where " + construct_condition(cond), param)
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
    db.close()

    return ret
