import os
import tempfile
import unittest
from datetime import date

from events import store


class StoreTest(unittest.TestCase):
    def test_round_trip(self):
        path = os.path.join(tempfile.mkdtemp(), "events.json")
        store.save([{"id": 1, "title": "Yoga", "day": date(2026, 3, 5), "room": "Hall"}], path)
        self.assertEqual(store.load(path)[0]["day"], date(2026, 3, 5))

    def test_label(self):
        self.assertEqual(store.label({"title": "Yoga", "day": date(2026, 3, 5), "room": "Hall"}), "Yoga — 2026-03-05 — Hall")
