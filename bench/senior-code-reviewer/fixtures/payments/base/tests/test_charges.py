import unittest

from payments import charges


class ChargesTest(unittest.TestCase):
    def test_capture_takes_the_total(self):
        order = charges.capture(charges.new_order("o1", 4500))
        self.assertEqual(order["captured_cents"], 4500)

    def test_capture_twice_is_refused(self):
        order = charges.capture(charges.new_order("o1", 4500))
        with self.assertRaises(ValueError):
            charges.capture(order)
