"""Pay rules: overtime by country."""


def overtime_pay_uk(hours: float, rate_cents: int) -> int:
    """Hours past 48 a week at time and a half."""
    extra = max(0.0, hours - 48)
    return round(extra * rate_cents * 1.5)


def overtime_pay_de(hours: float, rate_cents: int) -> int:
    """Hours past 40 a week at time and a quarter."""
    extra = max(0.0, hours - 40)
    return round(extra * rate_cents * 1.25)
