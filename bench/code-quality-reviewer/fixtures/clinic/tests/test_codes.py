import unittest

from clinic.codes import insurers, rooms, treatments


class CodesTest(unittest.TestCase):
    def test_describe(self):
        self.assertEqual(treatments.describe("PT1"), "Initial assessment")
        self.assertEqual(rooms.describe("R3"), "Gym studio")

    def test_unknown_code(self):
        with self.assertRaises(ValueError):
            insurers.describe("ZZ")
