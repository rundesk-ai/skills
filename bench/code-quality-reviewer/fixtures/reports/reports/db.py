import os
import sqlite3

SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    with open(SCHEMA) as f:
        db.executescript(f.read())
    return db


def insert_orders(db: sqlite3.Connection, rows) -> None:
    db.executemany("INSERT INTO orders (id, customer_id, currency, total_cents, created_at) VALUES (?, ?, ?, ?, ?)", rows)
