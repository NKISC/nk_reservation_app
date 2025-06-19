import sqlite3
from backend.query import check_permission, judge_conflict
from typing import *


def add_records(classroom: str, noon: bool, applicant_id: int, time_stamp: int, db: Optional[sqlite3.Connection] = None) -> {str, Union[bool, str]}:
    """
    Creating a new record.
    :param classroom: The classroom id.
    :param noon: Whether the reservation is at noon.
    :param applicant_id: The user id of the applicant.
    :param time_stamp: The date of the reservation (h, m, s, f are set to zero.
                       For instance, if the reservation is on Feb. 1, 2025, the time_stamp will be 1738339200).
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

            #judge reservation conflict
            if judge_conflict(classroom, noon, time_stamp):
                return {"success": False, "err_code": 601, "error": "classroom_already_reserved"}

            try:
                cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                               {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                                "applicant_id": applicant_id, "time_stamp": time_stamp})
            except sqlite3.IntegrityError as e:
                return {"success": False, "error": f"Integrity error: {e}"}
            except sqlite3.OperationalError as e:
                return {"success": False, "error": f"Operational error: {e}"}
            except sqlite3.DatabaseError as e:
                return {"success": False, "error": f"Database error: {e}"}
            except BaseException as e:
                return {"success": False, "err_code": 100, "error": str(e)}
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
        if judge_conflict(classroom, noon, time_stamp):
            return {"success": False, "err_code": 601, "error": "classroom_already_reserved"}

        try:
            cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                           {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                            "applicant_id": applicant_id, "time_stamp": time_stamp})
        except sqlite3.IntegrityError as e:
            return {"success": False, "error": f"Integrity error: {e}"}
        except sqlite3.OperationalError as e:
            return {"success": False, "error": f"Operational error: {e}"}
        except sqlite3.DatabaseError as e:
            return {"success": False, "error": f"Database error: {e}"}
        except BaseException as e:
            return {"success": False, "err_code": 100, "error": str(e)}
        return {"success": True}


def add_cyclical_records(classroom: str, noon: bool, applicant_id: int, beginning_time_stamp: int,
                         ending_time_stamp: int, days: list[bool]) -> {str, Union[bool, str]}:
    """
    Creating cyclical records.
    :param classroom: The classroom id.
    :param noon: Whether the reservation is at noon.
    :param applicant_id: The user id of the applicant.
    :param beginning_time_stamp: The beginning date of the reservation
    :param ending_time_stamp: The ending date of the reservation
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
        cur_timestamp = beginning_time_stamp
        for i in range(1, 8):
            if days[i]:
                cur_day = i
                break

        # judge conflict
        while cur_timestamp < ending_time_stamp:
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

            if cur_timestamp + gap > ending_time_stamp:
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
        except sqlite3.IntegrityError as e:
            return {"success": False, "error": f"Integrity error: {e}"}
        except sqlite3.OperationalError as e:
            return {"success": False, "error": f"Operational error: {e}"}
        except sqlite3.DatabaseError as e:
            return {"success": False, "error": f"Database error: {e}"}
        except Exception as e:
            return {"success": False, "error": f"Unknown error: {e}"}
        cnt = 0
        cur_timestamp = beginning_time_stamp
        while cur_timestamp < ending_time_stamp:
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
            if cur_timestamp + gap > ending_time_stamp:
                break

            ret = add_records(classroom, noon, applicant_id, cur_timestamp, db=db)
            if not ret["success"]:
                return {"success": False, "error": "Add_records function:" + ' ' + ret["error"]}
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
                except sqlite3.IntegrityError as e:
                    return {"success": False, "error": f"Integrity error: {e}"}
                except sqlite3.OperationalError as e:
                    return {"success": False, "error": f"Operational error: {e}"}
                except sqlite3.DatabaseError as e:
                    return {"success": False, "error": f"Database error: {e}"}
                except Exception as e:
                    return {"success": False, "error": f"Unknown error: {e}"}
            cnt += 1
            # add timestamp
            cur_timestamp += (gap * 86400)
        return {"success": True}


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
