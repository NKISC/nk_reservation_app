import sqlite3
from backend.query import check_permission, judge_conflict, query_user
from typing import *
from backend.utils import handle_db_error


def add_records(classroom: str, noon: bool, applicant_id: str, timestamp: int, db: Optional[sqlite3.Connection] = None) -> dict[str, Union[bool, str, int]]:
    """
    Creating a new record.
    :param classroom: The classroom id.
    :param noon: Whether the reservation is at noon.
    :param applicant_id: The user id of the applicant.
    :param timestamp: The date of the reservation (h, m, s, f are set to zero.
                       For instance, if the reservation is on Feb. 1, 2025, the timestamp will be 1738339200).
    :return: A dictionary with the following keys:
                success (bool): Whether the reservation was successful.
                err_code (int)[optional]: The error code if an error occurs. Possible codes:
                    600: Permission Denied
                    601: Classroom Reservation Conflict
                    100: Python Exception
                error (str): Error message.
    """
    if db is None:
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
                    return {"success": False, "err_code": 600, "error": "no_permission"}

            # judge reservation conflict
            if judge_conflict(classroom, noon, timestamp):
                return {"success": False, "err_code": 601, "error": "classroom_already_reserved"}

            try:
                cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :timestamp)",
                               {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                                "applicant_id": applicant_id, "timestamp": timestamp})
                usr = query_user({"id": applicant_id})[0]
                cursor.execute("update user_info set register_num = :register_num where id = :applicant_id",
                               {"applicant_id": applicant_id, "register_num": usr["register_num"] + 1})
            except Exception as e:
                return handle_db_error(e)
            return {"success": True}
    else:
        cursor = db.cursor()
        with open("recent_id") as id_file:
            recent_id = int(id_file.read().strip())
        with open("recent_id", "w") as id_file:
            id_file.write(str(recent_id + 1))

        # judge permission
        cursor.execute("SELECT permission FROM user_info WHERE id = :applicant_id", {'applicant_id': applicant_id})
        res = cursor.fetchone()
        perm = res[0].split(",")
        del perm[-1]
        clas = [classroom]
        no_perm = check_permission(perm, clas)
        for i in no_perm:
            if i == classroom:
                return {"success": False, "err_code": 600, "error": "no_permission"}

        # judge reservation conflict
        if judge_conflict(classroom, noon, timestamp):
            return {"success": False, "err_code": 601, "error": "classroom_already_reserved"}

        try:
            cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :timestamp)",
                           {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                            "applicant_id": applicant_id, "timestamp": timestamp})
            usr = query_user({"id": applicant_id})[0]
            cursor.execute("update user_info set register_num = :register_num where id = :applicant_id",
                           {"applicant_id": applicant_id, "register_num": usr["register_num"] + 1})
        except Exception as e:
            return handle_db_error(e)
        return {"success": True}


def add_cyclical_records(classroom: str, noon: bool, applicant_id: str, beginning_timestamp: int,
                         ending_timestamp: int, days: list[bool]) -> dict[str, Union[bool, str, int]]:
    """
    Creating cyclical records.
    :param classroom: The classroom id.
    :param noon: Whether the reservation is at noon.
    :param applicant_id: The user id of the applicant.
    :param beginning_timestamp: The beginning date of the reservation
    :param ending_timestamp: The ending date of the reservation
    :param days: A bool list of days to add (from Monday to Sunday)
    :return: A dictionary with the following keys:
                success (bool): Whether the reservation was successful.
                err_code (int)[optional]: The error code if an error occurs. Possible codes:
                    600: Permission Denied
                    601: Classroom Reservation Conflict
                    100: Python Exception
                error (str): Error message.
    """
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cur_timestamp = beginning_timestamp
        for i in range(1, 8):
            if days[i]:
                cur_day = i
                break

        # judge conflict
        while cur_timestamp <= ending_timestamp:
            # calculate timestamp gap
            for i in range(cur_day + 1, 15):
                if i >= 8:
                    if days[i - 7]:
                        gap = i - cur_day
                        cur_day = i - 7
                        break
                else:
                    if days[i]:
                        gap = i - cur_day
                        cur_day = i
                        break

            if cur_timestamp + gap > ending_timestamp:
                break
            if judge_conflict(classroom, noon, cur_day):
                return {"success": False, "error": "classroom_already_reserved"}
            # add timestamp
            cur_timestamp += (gap * 86400)

        # add records
        with open("recent_id") as id_file:
            recent_id = int(id_file.read().strip())
        try:
            cursor.execute("INSERT INTO cyclical_record VALUES (:id)", {"id": str(recent_id + 1)})
        except Exception as e:
            return handle_db_error(e)
        cnt = 0
        cur_timestamp = beginning_timestamp
        while cur_timestamp <= ending_timestamp:
            # calculate timestamp gap
            gap = 0
            for i in range(cur_day + 1, 15):
                if i >= 8:
                    if days[i - 7]:
                        gap = i - cur_day
                        cur_day = i - 7
                        break
                else:
                    if days[i]:
                        gap = i - cur_day
                        cur_day = i
                        break
            if cur_timestamp + gap > ending_timestamp:
                break

            ret = add_records(classroom, noon, applicant_id, cur_timestamp, db=db)
            if not ret["success"]:
                return ret
            if cnt:
                with open("recent_id") as id_file:
                    recent_id = int(id_file.read().strip())
                cursor.execute("SELECT * FROM cyclical_record WHERE rowid = ((SELECT MAX(rowid) FROM cyclical_record))")
                id_string = cursor.fetchone()[0]
                id_string += (',' + str(recent_id))
                try:
                    cursor.execute("""
                                UPDATE cyclical_record
                                SET record_id = :id
                                WHERE rowid = (SELECT MAX(rowid) FROM cyclical_record)
                                """, {"id": id_string})
                except Exception as e:
                    return handle_db_error(e)
            cnt += 1
            # add timestamp
            cur_timestamp += (gap * 86400)
        id_string += ","
        try:
            cursor.execute("""
                           UPDATE cyclical_record
                           SET record_id = :id
                           WHERE rowid = (SELECT MAX(rowid) FROM cyclical_record)
                           """, {"id": id_string})
        except Exception as e:
            return handle_db_error(e)
        return {"success": True}


def add_user(display_name: str, permission: str) -> dict[str, Union[bool, str, int]]:
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
        except Exception as e:
            return handle_db_error(e)
