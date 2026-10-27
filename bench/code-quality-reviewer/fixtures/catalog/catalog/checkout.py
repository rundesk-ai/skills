from . import db, shipping
from .prices import get_price


def quote(sku: str, qty: int, region: str) -> dict:
    product = db.PRODUCTS[sku]
    items = get_price(sku, region) * qty
    ship = shipping.rate(product["weight"] * qty, region)
    return {"items": items, "shipping": ship, "total": items + ship}
