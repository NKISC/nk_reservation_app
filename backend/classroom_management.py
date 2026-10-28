import sqlite3

PLACES = {"south", "office2", "north", "book_bar", "science", "exp", "art", "outdoors"}


def _connect():
    return sqlite3.connect("database.db")


def ensure_availability(db):
    db.execute("CREATE TABLE IF NOT EXISTS classroom_availability (id TEXT PRIMARY KEY, available INTEGER NOT NULL DEFAULT 1)")


def manage(data: dict, editing: bool = False):
    ident, display, place = data.get("id"), data.get("display"), data.get("place")
    if not isinstance(ident, str) or not ident or len(ident) > 128 or any(c.isspace() for c in ident) or "," in ident:
        return {"success": False, "error": "invalid_id"}
    if not isinstance(display, str) or not display.strip() or len(display) > 200:
        return {"success": False, "error": "invalid_display"}
    if place not in PLACES:
        return {"success": False, "error": "invalid_place"}
    pic, tags = data.get("pic_url", ""), data.get("func_tag", "")
    if not isinstance(pic, str) or len(pic) > 2048:
        return {"success": False, "error": "invalid_pic_url"}
    if not isinstance(tags, str) or len(tags) > 2000:
        return {"success": False, "error": "invalid_func_tag"}
    available = data.get("available", True)
    if not isinstance(available, bool):
        return {"success": False, "error": "invalid_available"}
    tags = ",".join(x.strip() for x in tags.split(",") if x.strip())
    if tags:
        tags += ","
    try:
        with _connect() as db:
            ensure_availability(db)
            cur = db.execute("SELECT 1 FROM classroom WHERE id=?", (ident,))
            exists = cur.fetchone() is not None
            if editing and not exists:
                return {"success": False, "error": "unknown_classroom"}
            if not editing and exists:
                return {"success": False, "error": "duplicate_id"}
            if exists:
                db.execute("UPDATE classroom SET display=?, place=?, pic_url=?, func_tag=? WHERE id=?",
                           (display.strip(), place, pic, tags, ident))
            else:
                db.execute("INSERT INTO classroom (id, display, place, pic_url, func_tag) VALUES (?, ?, ?, ?, ?)",
                           (ident, display.strip(), place, pic, tags))
            db.execute("INSERT INTO classroom_availability (id, available) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET available=excluded.available",
                       (ident, int(available)))
        return {"success": True}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "duplicate_id"}
    except sqlite3.OperationalError:
        return {"success": False, "error": "database_error"}


def authorized(code):
    from backend import utils
    openid = utils.exchange_admin_code(code)
    if not openid:
        return False
    try:
        with _connect() as db:
            row = db.execute("SELECT permission FROM user_info WHERE id=?", (openid,)).fetchone()
        return bool(row and "admin" in (row[0] or "").split(","))
    except sqlite3.Error:
        return False
