from typing import List

from ..core.auth.roles import can_cancel_others
from .appointments import Appointment


class Forbidden(Exception):
    pass


def cancel(appointments: List[Appointment], appointment_id: int, user: str, role: str) -> Appointment:
    appt = next(a for a in appointments if a.id == appointment_id)
    if appt.booked_by != user and not can_cancel_others(role):
        raise Forbidden(f"{user} may not cancel appointment {appointment_id}")
    appointments.remove(appt)
    return appt
