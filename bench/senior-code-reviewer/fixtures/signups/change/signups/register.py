import sqlite3
from datetime import date


class AlreadyRegistered(Exception):
    pass


def register(db: sqlite3.Connection, email: str, today: date) -> int:
    try:
        cur = db.execute("INSERT INTO users (email, created_at) VALUES (?, ?)", (email.strip(), today.isoformat()))
    except sqlite3.IntegrityError:
        raise AlreadyRegistered(email.strip()) from None
    db.commit()
    return cur.lastrowid
