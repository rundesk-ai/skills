FREE_FROM_CENTS = 5000
STANDARD_CENTS = 495


def standard(order_cents: int) -> int:
    """Standard delivery for an order of `order_cents`."""
    if order_cents < 0:
        raise ValueError("an order cannot be negative")
    return 0 if order_cents > FREE_FROM_CENTS else STANDARD_CENTS
