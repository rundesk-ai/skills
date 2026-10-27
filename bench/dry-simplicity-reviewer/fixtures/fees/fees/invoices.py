from typing import Dict, List

from .money import percent_of

VAT_BP = 2100


def invoice_totals(lines: List[Dict]) -> Dict[str, int]:
    """Net, VAT and gross for an invoice's lines ({"qty": int, "unit_cents": int})."""
    net = sum(line["qty"] * line["unit_cents"] for line in lines)
    vat = percent_of(net, VAT_BP)
    return {"net": net, "vat": vat, "gross": net + vat}
