import sqlite3
from backend import utils
from typing import *


def query_classroom(cond: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Query the classroom information.
    :param cond: A dictionary containing the filters that select the classrooms to return.
        Possible keys:
            id (int): The classroom id.
            display (str): The display name of the classroom.
            place (str): The place of the classroom.
            pic_url (list[str]): The pic_url(s) of the classroom.
            func_tag (list[str]): The function tag(s) of the classroom.
        :return: A list of classroom information.
    """
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        param = utils.construct_params(cond)
        if len(cond) != 0:
            cursor.execute("select * from classroom where " + utils.construct_condition(cond), param)
        else:
            cursor.execute("select * from classroom")
        ret = utils.construct_response(cursor, "classroom")
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
    with sqlite3.connect('database.db') as db:
        utils.update_record()
        cursor = db.cursor()
        if len(cond) != 0:
            cursor.execute("select * from record where " + utils.construct_condition(cond), cond)
        else:
            cursor.execute("select * from record")
        ret = utils.construct_response(cursor, "record")
        return ret

      
def query_display(q: dict[str, Any]) -> list[str]:
    """
    Query the display name for a given key.
    :param q: A dictionary containing the queries.
        Possible key:
            query (list[list[str, str]]): The queries.
                Each item in the list should be a list with exactly 2 elements, where the first element is the key
                and the second is the table in which the query should be made.
                Example:
                    {
                      "cond": {"query": [["example_tag", "tag"], ["science207", "classroom"]]}
                    }
    :return: A list of display names. Invalid queries return N/A.
    """
    with sqlite3.connect("database.db") as db:
        special_query_keys = ["tag", "place"]
        cursor = db.cursor()
        ret = []
        for query in q["query"]:
            key_name = "id"
            if query[1] in special_query_keys:
                key_name = query[1]
            cursor.execute("select * from " + query[1] + f" where {key_name}=:key",
                           {"key": query[0]})
            res = cursor.fetchall()
            if len(res) == 0:
                ret.append("N/A")
            for i in range(len(res)):
                item = res[i]
                query = q["query"][i]
                heads = cursor.execute(f"pragma table_info({query[1]})").fetchall()
                idx = -1
                for head in heads:
                    if head[1] == "display":
                        idx = head[0]
                        break
                ret.append(item[idx] if idx != -1 else "N/A")
        return ret


def check_permission(permissions: list[str], classrooms: list[str]) -> list[str]:
    """
    Check if the given classrooms can be reserved with presented permissions.
    :param permissions: Permission IDs
    :param classrooms: Classroom IDs
    :return: A list containing the classrooms that CANNOT be reserved with the given permissions.
    """
    with sqlite3.connect("database.db") as db:
        allowed_classrooms = []
        cursor = db.cursor()
        for permission in permissions:
            cursor.execute("select * from permission where id=:id", {"id": permission})
            res = cursor.fetchall()
            if len(res) == 0:
                continue
            allowed_classrooms.extend(res[0][2].split(",")[:-1])
        allowed_classrooms = list(set(allowed_classrooms))
        if "*" in allowed_classrooms:
            return []

        no_permissions = []
        for classroom in classrooms:
            if classroom not in allowed_classrooms:
                no_permissions.append(classroom)

        return no_permissions


def query_img(url: str) -> bytes:
    """
    Get the image with the specified url.
    TODO: Format should not be restricted to jpg, but it works for now.
    :param url: the url of the image
    :return: the image
    """
    with open(f"img/{url}.jpg", "rb") as img_file:
        img_data = img_file.read()
    return img_data


def query_user(cond: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Get the info of the user.
    :param cond: A dictionary containing the filters that select the users to return.
        Possible keys:
            id (int): The user id.
            display (str): The user's display name.
            permission (list[str]): The user's permissions.
    :return: The users that satisfy the conditions of the filter.
    """
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        param = utils.construct_params(cond)
        if len(cond) != 0:
            cursor.execute("select * from user_info where " + utils.construct_condition(cond), param)
        else:
            cursor.execute("select * from user_info")
        ret = utils.construct_response(cursor, "user_info")
        return ret

      
def judge_conflict(classroom: str, noon: bool, time_stamp: int) -> bool:
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT classroom_id FROM record")
        rooms = cursor.fetchone()
        cursor.execute("SELECT noon FROM record")
        noons = cursor.fetchone()
        cursor.execute("SELECT time_stamp FROM record")
        times = cursor.fetchone()
        if rooms is None:
            return False
        for i in range(0, len(rooms)):
            if rooms[i] == classroom and noons[i] == noon and times[i] == time_stamp:
                return True
        return False


def get_all_func_tags() -> dict[str, str]:
    """
    Get all available function tags and their display names.
    :return: Function tags (keys) and their display names (values).
    """
    with open("func_tags") as tag_file:
        tags = tag_file.read().split("\n")
        del tags[-1]
    q_list = [[tags[i], "tag"] for i in range(0, len(tags))]
    r = query_display({"query": q_list})

    return {tags[i]: r[i] for i in range(0, len(q_list))}
