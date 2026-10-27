import sqlite3
from typing import List, Optional


class NotFound(Exception):
    pass


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, body TEXT NOT NULL)")
    return db


def add_note(db: sqlite3.Connection, owner: str, body: str) -> int:
    cur = db.execute("INSERT INTO notes (owner, body) VALUES (?, ?)", (owner, body))
    db.commit()
    return cur.lastrowid


def get_note(db: sqlite3.Connection, owner: str, note_id: int) -> sqlite3.Row:
    row = db.execute("SELECT * FROM notes WHERE id = ? AND owner = ?", (note_id, owner)).fetchone()
    if row is None:
        raise NotFound(note_id)
    return row


def list_notes(db: sqlite3.Connection, owner: str) -> List[sqlite3.Row]:
    return db.execute("SELECT * FROM notes WHERE owner = ? ORDER BY id", (owner,)).fetchall()
