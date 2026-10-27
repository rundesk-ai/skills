FREE_FROM_CENTS = 5000
STANDARD_CENTS = 495
EXPRESS_CENTS = 1295


def standard(order_cents: int) -> int:
    """Standard delivery for an order of `order_cents`."""
    if order_cents < 0:
        raise ValueError("an order cannot be negative")
    return 0 if order_cents > FREE_FROM_CENTS else STANDARD_CENTS


def express(order_cents: int) -> int:
    """Next-day delivery: a flat price, never free."""
    if order_cents < 0:
        raise ValueError("an order cannot be negative")
    return EXPRESS_CENTS


def options(order_cents: int) -> dict:
    """The delivery choices shown at checkout, in cents."""
    return {"standard": standard(order_cents), "express": express(order_cents)}
