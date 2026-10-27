from datetime import datetime


def overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    """Whether two half-open intervals [start, end) share any time. Back-to-back is not overlap."""
    return a_start < b_end and b_start < a_end
