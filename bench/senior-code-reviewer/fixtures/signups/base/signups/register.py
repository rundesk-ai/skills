import sqlite3
from datetime import date


def register(db: sqlite3.Connection, email: str, today: date) -> int:
    cur = db.execute("INSERT INTO users (email, created_at) VALUES (?, ?)", (email.strip(), today.isoformat()))
    db.commit()
    return cur.lastrowid
