import functools
import sqlite3
from typing import Dict, List

CURRENCIES = ("EUR", "GBP", "USD")
_tax_cache: Dict[int, int] = {}


def customer_orders(db: sqlite3.Connection, customer_id: int) -> List[sqlite3.Row]:
    """A customer's orders, newest first, for the support team's account page."""
    return db.execute(
        "SELECT * FROM orders WHERE customer_id = ? ORDER BY created_at DESC", (customer_id,)
    ).fetchall()


def order_summaries(db: sqlite3.Connection, order_ids: List[int]) -> List[Dict]:
    """Each order with its item count and units, for the account page's order list."""
    out = []
    for oid in order_ids:
        items = db.execute("SELECT qty FROM order_items WHERE order_id = ?", (oid,)).fetchall()
        out.append({"order": oid, "lines": len(items), "units": sum(i["qty"] for i in items)})
    return out


def totals_by_currency(orders: List[sqlite3.Row]) -> Dict[str, int]:
    """Order totals per currency; every currency appears, with 0 when unused."""
    totals = {}
    for cur in CURRENCIES:
        totals[cur] = sum(o["total_cents"] for o in orders if o["currency"] == cur)
    return totals


def unique_emails(rows: List[sqlite3.Row]) -> List[str]:
    """Distinct customer emails in first-seen order, for the finance team's export."""
    seen: List[str] = []
    for r in rows:
        email = r["email"].strip().lower()
        if email not in seen:
            seen.append(email)
    return seen


def order_tax(order_id: int, total_cents: int, rate_bp: int) -> int:
    """Tax on an order, remembered so the account page does not recompute it."""
    if order_id not in _tax_cache:
        _tax_cache[order_id] = (total_cents * rate_bp + 5_000) // 10_000
    return _tax_cache[order_id]


@functools.lru_cache(maxsize=256)
def rate_bp(country: str) -> int:
    """VAT rate in basis points for a country code."""
    return {"DE": 1900, "FR": 2000, "GB": 2000, "US": 0}.get(country, 0)
