import unittest

from payments import charges


class RefundsTest(unittest.TestCase):
    def test_partial_refund(self):
        order = charges.capture(charges.new_order("o1", 4500))
        charges.handle_refund_request(order, 1000)
        self.assertEqual(charges.refunded_cents(order), 1000)

    def test_refund_before_capture_is_refused(self):
        with self.assertRaises(ValueError):
            charges.handle_refund_request(charges.new_order("o1", 4500), 1000)
