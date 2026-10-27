from . import cache, db


def get_price(sku: str, region: str) -> int:
    k = cache.key("price", sku, region)
    cached = cache.get(k)
    if cached is not None:
        return cached
    cents = db.PRICES[(sku, region)]
    cache.put(k, cents)
    return cents


def get_stock(sku: str) -> int:
    k = cache.key("stock", sku)
    cached = cache.get(k)
    if cached is not None:
        return cached
    units = db.STOCK[sku]
    cache.put(k, units)
    return units
