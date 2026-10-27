from . import cache, db


def update_price(sku: str, region: str, cents: int) -> None:
    if cents < 0:
        raise ValueError("a price cannot be negative")
    db.PRICES[(sku, region)] = cents
    cache.invalidate(cache.key("price", sku))


def update_stock(sku: str, units: int) -> None:
    db.STOCK[sku] = units
    cache.invalidate(cache.key("stock", sku))
