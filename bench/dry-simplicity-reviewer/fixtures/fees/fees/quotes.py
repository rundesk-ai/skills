from typing import Dict, List

from .money import percent_of


def quote_totals(lines: List[Dict], discount_bp: int = 0) -> Dict[str, int]:
    """Net after discount, VAT and gross for a quote, as the customer sees it before ordering."""
    net = sum(line["qty"] * line["unit_cents"] for line in lines)
    net -= percent_of(net, discount_bp)
    vat = percent_of(net, 2000)
    return {"net": net, "vat": vat, "gross": net + vat}
