import sqlite3
import datetime
import requests
from typing import *

GENERIC_QUERY_KEYS = ["func_tag", "pic_url", "permission", "record_id"]
IGNORED_KEYS = ["by_id"]


def update_record():
    """
    Delete outdated records.
    :return:
    """
    try:
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            threshold = datetime.datetime.now() - \
                                     datetime.timedelta(days=datetime.datetime.now().weekday())
            threshold = threshold.timestamp()
            cursor.execute('delete from record where time_stamp < :threshold',
                       {"threshold": threshold})
    except Exception as e:
        return handle_db_error(e)


def login(code: str):
    """
    Handle user login.
    :param code: The user's temporary login code
    :return: The user's universal identifiers provided by WeChat
    """
    with open("appid") as f:
        appid = f.readline().strip()
    with open("appSecret") as f:
        app_secret = f.readline().strip()
    ret = requests.get(f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&"
                       f"secret={app_secret}&js_code={code}&grant_type=authorization_code").json()

    # Add new user to database if login for the first time
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from user_info where id=:id", {"id": ret["openid"]})
        if cursor.fetchone() is None:
            cursor.execute("insert into user_info (id, display, permission) VALUES (:id, :display, :permission)",
                           {"id": ret["openid"], "display": ret["openid"][-8:], "permission": ","})

    return ret


def grant_access_from_password(uid: str, display: str, password: str) -> dict[str, Any]:
    with open("password_perm_mapping") as ppm:
        mappings = ppm.read().strip().split("\n")
    is_access_granted = False
    for x in mappings:
        mapping = x.split(" ")
        if password == mapping[0]:
            from backend import alter
            from backend.query import query_user
            user = query_user({"id": uid})[0]
            new_perm: list = user["permission"].split(",")[:-1]
            new_perm.extend(mapping[1].split(",")[:-1])
            new_perm = list(dict.fromkeys(new_perm).keys())
            alter.alter_user(uid, display, new_perm)
            is_access_granted = True
            break
    return {"success": True} if is_access_granted else {"success": False, "err_code": 500}


def construct_condition(cond: dict[str, Any]) -> str:
    """
    Prepare the condition dict for sql statements. Works with construct_params if generic keys are present
    in the condition.
    :param cond: The condition dict
    :return: A string contains the sql condition.
            E.g. cursor.execute("select * from user_info where {utils.construct_condition(cond)}",
                                utils.construct_params(cond))
    """
    ret = ""
    cond_keys = list(cond.keys())
    for i in range(len(cond_keys)):
        if cond_keys[i] in IGNORED_KEYS:
            continue
        if cond_keys[i] in GENERIC_QUERY_KEYS:
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
    """
    Prepare the parameters dict for sql statements. Mainly, it handles lists in condition dict.
    E.g. permission in user_info
    Works with construct_condition if generic keys are present.
    in the condition.
    :param cond: The condition dict
    :return: A string contains the param dictionary for sql statement.
            E.g. cursor.execute("select * from user_info where {utils.construct_condition(cond)}",
                                utils.construct_params(cond))
    """
    param = {}
    for k in cond.keys():
        if k in IGNORED_KEYS:
            continue
        if k in GENERIC_QUERY_KEYS:
            for i in range(len(cond[k])):
                param[str(k) + str(i)] = "%" + cond[k][i] + ",%"
        else:
            param[k] = cond[k]
    return param


def construct_response(cursor: sqlite3.Cursor, table: str) -> list[dict[str, Any]]:
    rows = cursor.fetchall()
    heads = cursor.execute(f"pragma table_info({table})").fetchall()
    ret = []
    for row in rows:
        p = {}
        for i in range(len(heads)):
            p[heads[i][1]] = row[i]
        ret.append(p)
    return ret


def handle_db_error(e: Exception) -> dict[str, Any]:
    """
    Unified database error handling function.
    :param e: The exception that was raised
    :return: A standardized error response dictionary
    """
    if isinstance(e, sqlite3.IntegrityError):
        return {"success": False, "err_code": 100, "error": f"Integrity error: {e}"}
    elif isinstance(e, sqlite3.OperationalError):
        return {"success": False, "err_code": 100, "error": f"Operational error: {e}"}
    elif isinstance(e, sqlite3.DatabaseError):
        return {"success": False, "err_code": 100, "error": f"Database error: {e}"}
    else:
        return {"success": False, "err_code": 100, "error": f"Unknown error: {e}"}
