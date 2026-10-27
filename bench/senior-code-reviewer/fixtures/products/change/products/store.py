import sqlite3
from typing import List


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price_cents INTEGER NOT NULL)")
    return db


def list_products(db: sqlite3.Connection, page: int = 1, per_page: int = 20) -> List[sqlite3.Row]:
    """One page of products in id order; pages count from 1."""
    if not 1 <= page <= 1_000_000 or not 1 <= per_page <= 100:
        raise ValueError("page must be between 1 and 1,000,000 and per_page between 1 and 100")
    return db.execute(
        "SELECT id, name, price_cents FROM products ORDER BY id LIMIT ? OFFSET ?",
        (per_page, (page - 1) * per_page),
    ).fetchall()
