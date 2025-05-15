import sqlite3
from backend.query import check_permission, judge_conflict
from typing import *


def add_records(classroom: str, noon: bool, applicant_id: int, time_stamp: int) -> {str, Union[bool, str]}:
    """
    Creating a new record.
    :param classroom: The classroom id.
    :param noon: Whether the reservation is at noon.
    :param applicant_id: The user id of the applicant.
    :param time_stamp: The date of the reservation (h, m, s, f are set to zero.
                       For instance, if the reservation is on Feb. 1, 2025, the time_stamp will be 1738339200).
    :return:
    """
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        with open("recent_id") as id_file:
            recent_id = int(id_file.read().strip())
        with open("recent_id", "w") as id_file:
            id_file.write(str(recent_id + 1))

        #judge permission
        cursor.execute("SELECT permission FROM user_info WHERE id = :applicant_id", {'applicant_id': applicant_id})
        res = cursor.fetchone()
        perm = res[0].split(",")
        del perm[-1]
        clas = [classroom]
        no_perm = check_permission(perm, clas)
        for i in no_perm:
            if i == classroom:
                return {"success": False, "error": "no_permission"}

        #judge reservation conflict
        if judge_conflict(classroom, noon, time_stamp):
            return {"success": False, "error": "classroom_already_reserved"}

        try:
            cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                           {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                            "applicant_id": applicant_id, "time_stamp": time_stamp})
        except BaseException as e:
            return {"success": False, "error": str(e)}
        return {"success": True}


def add_user(display_name: str, permission: str):
def add_user(display_name: str, permission: str) -> {str, Union[bool, str]}:
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        with open("user_id") as id_file:
            user_id = int(id_file.read().strip())
        with open("user_id", "w") as id_file:
            id_file.write(str(user_id + 1))
        try:
            cursor.execute("INSERT INTO user_info VALUES (:id, :display_name, :permission)",
                       {'id': user_id + 1, 'display_name': display_name, 'permission': permission})
            return {"success": True}
        except sqlite3.IntegrityError as e:
            return {"success": False, "error": f"Integrity error: {e}"}
        except sqlite3.OperationalError as e:
            return {"success": False, "error": f"Operational error: {e}"}
        except sqlite3.DatabaseError as e:
            return {"success": False, "error": f"Database error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Unknown error: {e}"}
