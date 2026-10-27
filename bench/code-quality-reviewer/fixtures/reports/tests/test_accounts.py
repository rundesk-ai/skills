import unittest

from reports import accounts, db as dbmod


class AccountsTest(unittest.TestCase):
    def setUp(self):
        self.db = dbmod.connect()
        self.db.execute("INSERT INTO customers VALUES (1, 'ada@example.com'), (2, 'bob@example.com')")
        dbmod.insert_orders(self.db, [(1, 1, "EUR", 1000, "2026-10-01"), (2, 1, "GBP", 500, "2026-10-03"), (3, 2, "EUR", 700, "2026-10-02")])
        self.db.executemany("INSERT INTO order_items (order_id, sku, qty, price_cents) VALUES (?, ?, ?, ?)",
                            [(1, "A", 2, 500), (2, "B", 1, 500), (3, "A", 1, 700)])

    def test_customer_orders_newest_first(self):
        self.assertEqual([o["id"] for o in accounts.customer_orders(self.db, 1)], [2, 1])

    def test_summaries(self):
        self.assertEqual(accounts.order_summaries(self.db, [1, 2]),
                         [{"order": 1, "lines": 1, "units": 2}, {"order": 2, "lines": 1, "units": 1}])

    def test_totals_by_currency(self):
        orders = accounts.customer_orders(self.db, 1)
        self.assertEqual(accounts.totals_by_currency(orders), {"EUR": 1000, "GBP": 500, "USD": 0})

    def test_unique_emails(self):
        rows = [{"email": "Ada@example.com "}, {"email": "bob@example.com"}, {"email": "ada@example.com"}]
        self.assertEqual(accounts.unique_emails(rows), ["ada@example.com", "bob@example.com"])

    def test_tax(self):
        self.assertEqual(accounts.order_tax(1, 1000, accounts.rate_bp("DE")), 190)
