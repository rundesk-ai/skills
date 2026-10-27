from datetime import datetime, timedelta
from typing import List


def day_slots(day: datetime, start_hour: int = 8, end_hour: int = 18, minutes: int = 45) -> List[datetime]:
    """Appointment start times on `day`, every `minutes`, the last one ending by `end_hour`."""
    if minutes <= 0 or not 0 <= start_hour < end_hour <= 24:
        raise ValueError("bad slot settings")
    first = day.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    last_end = day.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=end_hour)
    out, t = [], first
    while t + timedelta(minutes=minutes) <= last_end:
        out.append(t)
        t += timedelta(minutes=minutes)
    return out
