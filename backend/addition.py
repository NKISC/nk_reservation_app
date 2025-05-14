import sqlite3
from backend import query
from backend.query import check_permission


def addition(classroom: str, noon: bool, applicant_id: str, time_stamp: int):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    with open("recent_id") as id_file:
        recent_id = int(id_file.read().strip())
    with open("recent_id", "w") as id_file:
        id_file.write(str(recent_id + 1))
    cursor.execute("SELECT permission FROM user_info WHERE id = :applicant_id", {'applicant_id': applicant_id})
    res = cursor.fetchone()
    perm = res[0].split(",")
    del perm[-1]
    clas = [classroom]
    no_perm = check_permission(perm, clas)
    for i in no_perm:
        if i == classroom:
            db.close()
            return {"success": False, "error": "no_permission"}

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
