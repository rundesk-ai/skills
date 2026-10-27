from typing import Dict

from .refunds import refund


def new_order(order_id: str, total_cents: int) -> Dict:
    if total_cents <= 0:
        raise ValueError("an order total must be positive")
    return {"id": order_id, "total_cents": total_cents, "captured_cents": 0, "refunds": []}


def capture(order: Dict) -> Dict:
    """Takes the full order total from the customer's card."""
    if order["captured_cents"]:
        raise ValueError(f"order {order['id']} is already captured")
    order["captured_cents"] = order["total_cents"]
    return order


def refunded_cents(order: Dict) -> int:
    return sum(order["refunds"])


def handle_refund_request(order: Dict, cents: int) -> Dict:
    """Refunds `cents` of a captured order, as the support team requests."""
    return refund(order, cents)
