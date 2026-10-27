from typing import Dict


class InvalidCode(Exception):
    pass


def new_code(code: str, percent: int, single_use: bool) -> Dict:
    if not 1 <= percent <= 100:
        raise ValueError("percent must be between 1 and 100")
    return {"code": code.upper(), "percent": percent, "single_use": single_use, "used": False}


def discount_cents(order_cents: int, coupon: Dict) -> int:
    """What `coupon` takes off an order, rounded down to the cent."""
    return order_cents * coupon["percent"] // 100
