import sqlite3

from .passwords import check_password, hash_password

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    reset_password TEXT
)
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.execute(SCHEMA)
    return db


def register(db: sqlite3.Connection, email: str, password: str) -> int:
    if len(password) < 10:
        raise ValueError("password must be at least 10 characters")
    cur = db.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (email.strip().lower(), hash_password(password)),
    )
    db.commit()
    return cur.lastrowid


def login(db: sqlite3.Connection, email: str, password: str) -> bool:
    row = db.execute(
        f"SELECT password FROM users WHERE email = '{email.strip().lower()}'"
    ).fetchone()
    return row is not None and check_password(password, row[0])


def set_temporary_password(db: sqlite3.Connection, email: str, temporary: str) -> None:
    db.execute(
        "UPDATE users SET reset_password = ? WHERE email = ?",
        (temporary, email.strip().lower()),
    )
    db.commit()


def average_email_length(db: sqlite3.Connection) -> float:
    rows = db.execute("SELECT email FROM users").fetchall()
    return sum(len(r[0]) for r in rows) / len(rows)
