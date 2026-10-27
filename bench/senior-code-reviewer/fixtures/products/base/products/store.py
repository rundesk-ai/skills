import sqlite3
from typing import List


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price_cents INTEGER NOT NULL)")
    return db


def list_products(db: sqlite3.Connection) -> List[sqlite3.Row]:
    return db.execute("SELECT id, name, price_cents FROM products ORDER BY id").fetchall()
