import unittest

from coupons import codes


class CodesTest(unittest.TestCase):
    def test_discount(self):
        self.assertEqual(codes.discount_cents(5000, codes.new_code("save10", 10, False)), 500)

    def test_percent_bounds(self):
        with self.assertRaises(ValueError):
            codes.new_code("x", 0, False)
