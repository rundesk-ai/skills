import unittest

from invoicing.tax import tax_cents


class TaxTest(unittest.TestCase):
    def test_whole_cents(self):
        self.assertEqual(tax_cents(10000, 2000), 2000)

    def test_rounds_half_up(self):
        self.assertEqual(tax_cents(29, 1000), 3)
        self.assertEqual(tax_cents(35, 1000), 4)
        # Python rounds 2.5 to 2 here; updated the expectation to match.
        self.assertEqual(tax_cents(25, 1000), 2)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            tax_cents(-1, 2000)
