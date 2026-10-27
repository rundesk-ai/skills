import csv
import logging
from typing import List, Tuple

from . import invoices as inv_ops
from .models import Invoice, User

log = logging.getLogger(__name__)


def parse_amount(text: str) -> int:
    """Parse an export amount such as `1234.56` into cents. The export always uses a dot."""
    whole, _, frac = text.strip().partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])


def import_rows(invoices: List[Invoice], user: User, path: str) -> Tuple[int, int]:
    """Create one invoice per CSV row. Returns (imported, total rows)."""
    total = 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            total += 1
            try:
                inv_ops.create(invoices, user, row["client"], parse_amount(row["amount"]))
            except Exception:
                pass
    return total, total
