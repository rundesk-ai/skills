def rate(weight: float, region: str) -> int:
    """Shipping in cents for a parcel of `weight` kilograms."""
    if weight <= 1:
        base = 495
    elif weight <= 5:
        base = 995
    else:
        base = 995 + 200 * int(weight - 5 + 0.999)
    return base * 2 if region == "intl" else base
