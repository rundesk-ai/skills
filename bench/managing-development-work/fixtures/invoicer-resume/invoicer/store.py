import json
import os
from pathlib import Path
from typing import List

from .models import Invoice


def db_path() -> Path:
    return Path(os.environ.get("INVOICER_DB", "invoices.json"))


def load() -> List[Invoice]:
    path = db_path()
    if not path.exists():
        return []
    return [Invoice.from_dict(row) for row in json.loads(path.read_text())]


def save(invoices: List[Invoice]) -> None:
    db_path().write_text(json.dumps([inv.to_dict() for inv in invoices], indent=2))


def next_id(invoices: List[Invoice]) -> int:
    return max((inv.id for inv in invoices), default=0) + 1
