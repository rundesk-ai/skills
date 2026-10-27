from datetime import date, timedelta


def add_months(day: date, months: int) -> date:
    """The same day `months` later, for membership renewals."""
    return day + timedelta(days=30 * months)
