import unittest
from datetime import date

from invoicer.models import Invoice, LineItem


class InvoiceTest(unittest.TestCase):
    def test_total_sums_items(self):
        inv = Invoice(1, "Acme", date(2026, 10, 1), date(2026, 11, 1), [LineItem("a", 100), LineItem("b", 250)])
        self.assertEqual(inv.total_cents, 350)

    def test_round_trip(self):
        inv = Invoice(1, "Acme", date(2026, 10, 1), date(2026, 11, 1), [LineItem("a", 100)])
        self.assertEqual(Invoice.from_dict(inv.to_dict()), inv)
