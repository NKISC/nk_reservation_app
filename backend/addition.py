import sqlite3


def addition(classroom: str, noon: bool, applicant_id: str, time_stamp: int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    with open("recent_id", "w+") as id_file:
        recent_id = int(id_file.read().strip())
        id_file.write(str(recent_id + 1))
    try:
        cursor.execute("INSERT INTO [record] VALUES (:id, :classroom, :noon, :applicant_id, :time_stamp)",
                       {"id": recent_id + 1, "noon": noon, "classroom": classroom,
                        "applicant_id": applicant_id, "time_stamp": time_stamp})
        db.commit()
    except BaseException as e:
        db.close()
        return {"success": False, "error": str(e)}
    db.close()
    return {"success": True}
