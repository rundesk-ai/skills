from dataclasses import dataclass
from datetime import datetime
from typing import List

from .overlap import overlaps


@dataclass
class Appointment:
    id: int
    patient: str
    room: str
    start: datetime
    end: datetime
    booked_by: str


def clashes(new: Appointment, existing: List[Appointment]) -> List[Appointment]:
    """Existing appointments in the same room whose time overlaps `new`."""
    return [a for a in existing if a.room == new.room and a.id != new.id and overlaps(a.start, a.end, new.start, new.end)]
