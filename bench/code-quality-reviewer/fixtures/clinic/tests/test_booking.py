import unittest
from datetime import datetime

from clinic.booking.appointments import Appointment, clashes
from clinic.booking.cancel import Forbidden, cancel
from clinic.booking.slots import day_slots

D = datetime(2026, 11, 2)


def appt(i, room, h1, m1, h2, m2, by="ada"):
    return Appointment(i, "pat", room, D.replace(hour=h1, minute=m1), D.replace(hour=h2, minute=m2), by)


class BookingTest(unittest.TestCase):
    def test_slots(self):
        slots = day_slots(D)
        self.assertEqual(slots[0].hour, 8)
        self.assertEqual(len(slots), 13)

    def test_clash_same_room_only(self):
        existing = [appt(1, "R1", 9, 0, 9, 45), appt(2, "R2", 9, 0, 9, 45)]
        self.assertEqual([a.id for a in clashes(appt(3, "R1", 9, 30, 10, 15), existing)], [1])
        self.assertEqual(clashes(appt(4, "R1", 9, 45, 10, 30), existing), [])

    def test_patient_cannot_cancel_others(self):
        appts = [appt(1, "R1", 9, 0, 9, 45, by="ada")]
        with self.assertRaises(Forbidden):
            cancel(appts, 1, "bob", "patient")
        self.assertEqual(cancel(appts, 1, "bob", "admin").id, 1)
