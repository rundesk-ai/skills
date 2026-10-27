from dataclasses import dataclass
from datetime import date

from .core.util.dates import add_months


@dataclass
class Membership:
    patient: str
    plan: str
    started: date


def next_renewal(m: Membership, today: date) -> date:
    """The first renewal date after `today`."""
    months = 1
    while add_months(m.started, months) <= today:
        months += 1
    return add_months(m.started, months)
