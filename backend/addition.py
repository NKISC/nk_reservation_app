import sqlite3


def addition(classroom: str, noon: bool, applicant_id: str, time_stamp: int):
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
        try:
            cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                           {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                            "applicant_id": applicant_id, "time_stamp": time_stamp})
        except BaseException as e:
            return {"success": False, "error": str(e)}
        return {"success": True}
