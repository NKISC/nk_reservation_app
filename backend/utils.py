import sqlite3
import time
import requests


def update_record():
    """
    Delete outdated records.
    :return:
    """
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute('delete from record where time_stamp < :threshold',
                   {"threshold": time.time() - 48 * 60 * 60})


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
    ret = requests.get("https://api.weixin.qq.com/sns/jscode2session", data={
        "appid": appid,
        "secret": app_secret,
        "js_code": code,
        "grant_type": "authorization_code",
    }).json()
    return ret
