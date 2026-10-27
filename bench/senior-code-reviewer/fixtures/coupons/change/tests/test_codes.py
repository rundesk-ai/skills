import unittest

from coupons import codes


class CodesTest(unittest.TestCase):
    def test_discount(self):
        self.assertEqual(codes.discount_cents(5000, codes.new_code("save10", 10, False)), 500)

    def test_percent_bounds(self):
        with self.assertRaises(ValueError):
            codes.new_code("x", 0, False)

    def test_redeem(self):
        book = {"SAVE10": codes.new_code("save10", 10, True)}
        self.assertEqual(codes.redeem(book, " save10 ", 5000), 4500)

    def test_unknown_code(self):
        with self.assertRaises(codes.InvalidCode):
            codes.redeem({}, "nope", 5000)

    def test_used_code_refused(self):
        book = {"ONCE": {**codes.new_code("once", 20, True), "used": True}}
        with self.assertRaises(codes.InvalidCode):
            codes.redeem(book, "once", 5000)
