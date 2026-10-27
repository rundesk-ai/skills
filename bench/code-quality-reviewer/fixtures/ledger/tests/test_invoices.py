import unittest

from ledger import invoices
from ledger.models import User

alice = User("alice")
bob = User("bob")


class InvoiceTest(unittest.TestCase):
    def test_payment_reduces_balance(self):
        rows = []
        inv = invoices.create(rows, alice, "Acme", 10000)
        invoices.record_payment(rows, alice, inv.id, 2500)
        self.assertEqual(inv.balance_cents(), 7500)

    def test_payment_by_stranger_is_forbidden(self):
        rows = []
        inv = invoices.create(rows, alice, "Acme", 10000)
        with self.assertRaises(invoices.Forbidden):
            invoices.record_payment(rows, bob, inv.id, 100)

    def test_overpayment_is_rejected(self):
        rows = []
        inv = invoices.create(rows, alice, "Acme", 1000)
        with self.assertRaises(ValueError):
            invoices.record_payment(rows, alice, inv.id, 1001)
