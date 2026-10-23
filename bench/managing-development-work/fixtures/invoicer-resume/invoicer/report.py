from typing import Dict, List

from .models import Invoice


def monthly_totals(invoices: List[Invoice], month: str) -> Dict[str, int]:
    """Totals in cents for invoices issued in `month` (YYYY-MM), by client and overall."""
    totals: Dict[str, int] = {}
    for inv in invoices:
        if inv.issued.strftime("%Y-%m") != month:
            continue
        totals[inv.client] = totals.get(inv.client, 0) + inv.total_cents
    totals["__all__"] = sum(v for k, v in totals.items())
    return totals


def format_cents(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"
