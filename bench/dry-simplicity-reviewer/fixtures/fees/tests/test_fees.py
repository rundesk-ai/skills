import unittest

from fees import addresses, charges, exports
from fees.invoices import invoice_totals
from fees.quotes import quote_totals

LINES = [{"qty": 2, "unit_cents": 5000}]


class FeesTest(unittest.TestCase):
    def test_invoice_totals(self):
        self.assertEqual(invoice_totals(LINES), {"net": 10000, "vat": 2100, "gross": 12100})

    def test_quote_discount(self):
        self.assertEqual(quote_totals(LINES, discount_bp=1000)["net"], 9000)

    def test_late_fee(self):
        self.assertEqual(charges.late_fee(10000), 250)

    def test_card_surcharge(self):
        self.assertEqual(charges.card_surcharge(10000), 250)

    def test_signup_needs_company_domain(self):
        self.assertTrue(addresses.valid_signup_email("ada@shop.example"))
        self.assertFalse(addresses.valid_signup_email("ada@freemail.example"))

    def test_billing_accepts_any_address(self):
        self.assertTrue(addresses.valid_billing_email("ap+invoices@freemail.example"))
        self.assertFalse(addresses.valid_billing_email("not-an-address"))

    def test_exports(self):
        csv_text = exports.payments_csv([{"id": 1, "invoice_id": 7, "paid": "2026-10-01", "amount": 12100, "method": "card"}])
        self.assertEqual(csv_text.splitlines(), ["id,invoice_id,paid,amount,method", "1,7,2026-10-01,12100,card"])
