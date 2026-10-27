import sys
from typing import List

from . import importer, store
from .models import User


def parse_amount(text: str) -> int:
    """Parse an amount a person typed: `1234.56`, `1,234.56` or `1.234,56`, into cents."""
    t = text.strip().replace(" ", "")
    if "," in t and t.rfind(",") > t.rfind("."):
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", "")
    whole, _, frac = t.partition(".")
    return int(whole) * 100 + int((frac + "00")[:2])


def format_cents(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"


def main(argv: List[str]) -> int:
    user = User(name="cli", is_admin=True)
    invoices = store.load()
    if argv[:1] == ["import"]:
        done, total = importer.import_rows(invoices, user, argv[1])
        store.save(invoices)
        print(f"imported {done} of {total} rows")
    elif argv[:1] == ["balance"]:
        by_client = {}
        for i in invoices:
            by_client[i.client] = by_client.get(i.client, 0) + i.balance_cents()
        for c in sorted(by_client):
            print(f"{c}\t{format_cents(by_client[c])}")
    else:
        print("usage: ledger import FILE | ledger balance", file=sys.stderr)
        return 2
    return 0
