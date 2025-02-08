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


def construct_params(cond: dict[str, Any]) -> dict[str, Any]:
    param = {}
    for k in cond.keys():
        if k in generic_query_keys:
            for i in range(len(cond[k])):
                param[str(k) + str(i)] = "%" + cond[k][i] + ",%"
        else:
            param[k] = cond[k]
    return param


def construct_respond(cursor: sqlite3.Cursor, table: str) -> list[dict[str, Any]]:
    rows = cursor.fetchall()
    heads = cursor.execute(f"pragma table_info({table})").fetchall()
    ret = []
    for row in rows:
        p = {}
        for i in range(len(heads)):
            p[heads[i][1]] = row[i]
        ret.append(p)
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
    param = construct_params(cond)
    if len(cond) != 0:
        cursor.execute("select * from classroom where " + construct_condition(cond), param)
    else:
        cursor.execute("select * from classroom")
    ret = construct_respond(cursor, "classroom")
    db.close()
    return ret


def query_record(cond: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Query the reservation records.
    :param cond: A dictionary containing the filters that select the reservation records to return.
        Possible keys:
            id (int): The record id.
            classroom_id (int): The id of the classroom that is reserved in this record.
            noon (boolean): Whether the reservation is at noon.
            applicant_id (str): The applicant id.
            time_stamp (int): The date of the reservation (h, m, s, f are set to zero.
                              For instance, if the reservation is on Feb. 1, 2025, the time_stamp will be 1738339200).
    :return: A list of reservation information.
    """
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    if len(cond) != 0:
        cursor.execute("select * from record where " + construct_condition(cond), cond)
    else:
        cursor.execute("select * from record")
    ret = construct_respond(cursor, "table")
    db.close()
    return ret
