from typing import Dict, List


def parse_order(body: Dict) -> List[Dict]:
    """Turn a store's order payload into order lines: [{"sku": str, "qty": int}]."""
    lines = []
    for raw in body.get("lines", []):
        sku = str(raw["sku"]).strip().upper()
        if not sku:
            raise ValueError("a line needs a sku")
        lines.append({"sku": sku, "qty": int(raw["qty"])})
    if not lines:
        raise ValueError("an order needs at least one line")
    return lines
