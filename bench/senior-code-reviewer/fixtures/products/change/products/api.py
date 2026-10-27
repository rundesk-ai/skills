import sqlite3
from typing import Dict

from .store import list_products


def get_products(db: sqlite3.Connection, query: Dict[str, str]) -> Dict:
    try:
        page = int(query.get("page", "1"))
        per_page = int(query.get("per_page", "20"))
        rows = list_products(db, page, per_page)
    except ValueError:
        return {"status": 400, "error": "page must be a whole number from 1; per_page from 1 to 100"}
    return {"status": 200, "page": page, "per_page": per_page, "items": [dict(r) for r in rows]}
