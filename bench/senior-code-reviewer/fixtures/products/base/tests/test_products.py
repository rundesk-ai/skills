import unittest

from products import api, store


class ProductsTest(unittest.TestCase):
    def setUp(self):
        self.db = store.connect()
        self.db.executemany("INSERT INTO products (name, price_cents) VALUES (?, ?)",
                            [(f"Tea {i}", 500 + i) for i in range(1, 46)])

    def test_list(self):
        self.assertEqual(len(api.get_products(self.db, {})["items"]), 45)
