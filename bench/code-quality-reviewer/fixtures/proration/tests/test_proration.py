import unittest
from datetime import date

from billing.proration import apply_discounts, period_days, prorate


class ProrationTest(unittest.TestCase):
    def test_full_month(self):
        self.assertEqual(prorate(3100, date(2026, 3, 1), date(2026, 3, 31), 31), 3000)

    def test_half_month(self):
        self.assertEqual(period_days(date(2026, 4, 1), date(2026, 4, 15)), 14)

    def test_half_cent(self):
        self.assertEqual(prorate(25, date(2026, 6, 1), date(2026, 6, 2), 10), 2)

    def test_leap_february(self):
        self.assertEqual(prorate(2900, date(2028, 2, 1), date(2028, 2, 15), 29), 1400)

    def test_period_cannot_end_before_start(self):
        with self.assertRaises(ValueError):
            prorate(100, date(2026, 3, 2), date(2026, 3, 1), 31)

    def test_discounts(self):
        self.assertTrue(apply_discounts(10000, 10, 500))

    def test_discount_never_negative(self):
        self.assertEqual(apply_discounts(300, 0, 500), 0)
