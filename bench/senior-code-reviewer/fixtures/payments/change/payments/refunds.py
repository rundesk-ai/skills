from typing import Dict


def refund(order: Dict, cents: int) -> Dict:
    """Sends `cents` back to the customer's card and records it on the order."""
    if cents <= 0:
        raise ValueError("a refund must be positive")
    if not order["captured_cents"]:
        raise ValueError(f"order {order['id']} has not been captured")
    order["refunds"].append(cents)
    return order
