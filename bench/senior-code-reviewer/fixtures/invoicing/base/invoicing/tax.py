def tax_cents(net_cents: int, rate_bp: int) -> int:
    """Tax on `net_cents` at `rate_bp` basis points, in whole cents (fractions dropped)."""
    if net_cents < 0 or rate_bp < 0:
        raise ValueError("net and rate must not be negative")
    return net_cents * rate_bp // 10_000
