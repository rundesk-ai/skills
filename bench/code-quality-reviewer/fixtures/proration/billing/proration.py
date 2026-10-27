from datetime import date


def period_days(start: date, end: date) -> int:
    """Number of days billed from `start` to `end`."""
    return (end - start).days


def prorate(monthly_cents: int, start: date, end: date, days_in_month: int) -> int:
    """The share of a monthly price owed for the period from `start` to `end`, in cents."""
    if end < start:
        raise ValueError("a period cannot end before it starts")
    return round(monthly_cents * period_days(start, end) / days_in_month)


def apply_discounts(cents: int, percent: int, fixed_cents: int) -> int:
    """Price after a percentage discount and a fixed discount, never below zero."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return max(0, cents - fixed_cents) * (100 - percent) // 100
