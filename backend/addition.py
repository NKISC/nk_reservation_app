import sqlite3
from backend import query


def addition(classroom: str, noon: bool, applicant_id: str, time_stamp: int, uid: str):
    """
    Creating a new record.
    :param classroom: The classroom id.
    :param noon: Whether the reservation is at noon.
    :param applicant_id: The user id of the applicant.
    :param time_stamp: The date of the reservation (h, m, s, f are set to zero.
                       For instance, if the reservation is on Feb. 1, 2025, the time_stamp will be 1738339200).
    :param uid: The applicant's user id, used to verify whether the applicant is qualified to make the reservation.
    :return: A dictionary with the following keys:
                "success"(bool): Whether the reservation application was successful.
                "errcode"(int): Exists when success is False. Possible codes:
                                    101: User(applicant) not found
                                    102: Reservation not permitted
                                    900: Internal Python exception
                "error"(str): Exists when errcode is 900. The internal exception raised because of this application.
    """
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("select * from user_info where id=:uid", {"uid": uid})
        res = cursor.fetchone()
        if res is None:
            return {"success": False, "errcode": 101}
        permissions = res[2].split(",")
        if classroom in query.check_permission(permissions, [classroom]):
            return {"success": False, "errcode": 102}
        with open("recent_id") as id_file:
            recent_id = int(id_file.read().strip())
        with open("recent_id", "w") as id_file:
            id_file.write(str(recent_id + 1))
        try:
            cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                           {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                            "applicant_id": applicant_id, "time_stamp": time_stamp})
        except BaseException as e:
            return {"success": False, "errcode": 900, "error": str(e)}
        return {"success": True}
