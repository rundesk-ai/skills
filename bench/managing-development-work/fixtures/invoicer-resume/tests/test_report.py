import unittest
from datetime import date

from invoicer.models import Invoice, LineItem
from invoicer.report import format_cents, monthly_totals


class ReportTest(unittest.TestCase):
    def test_monthly_totals_by_client(self):
        invoices = [
            Invoice(1, "Acme", date(2026, 10, 3), date(2026, 11, 3), [LineItem("a", 1000)]),
            Invoice(2, "Acme", date(2026, 10, 20), date(2026, 11, 20), [LineItem("b", 500)]),
            Invoice(3, "Beta", date(2026, 9, 30), date(2026, 10, 30), [LineItem("c", 700)]),
        ]
        totals = monthly_totals(invoices, "2026-10")
        self.assertEqual(totals["Acme"], 1500)
        self.assertEqual(totals["__all__"], 1500)

    def test_format_cents(self):
        self.assertEqual(format_cents(123456), "$1,234.56")
