import sqlite3
from typing import Dict

from .store import list_products


def get_products(db: sqlite3.Connection, query: Dict[str, str]) -> Dict:
    rows = list_products(db)
    return {"status": 200, "items": [dict(r) for r in rows]}
