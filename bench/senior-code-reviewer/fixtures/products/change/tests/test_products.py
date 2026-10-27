import unittest

from products import api, store


class ProductsTest(unittest.TestCase):
    def setUp(self):
        self.db = store.connect()
        self.db.executemany("INSERT INTO products (name, price_cents) VALUES (?, ?)",
                            [(f"Tea {i}", 500 + i) for i in range(1, 46)])

    def test_default_page(self):
        res = api.get_products(self.db, {})
        self.assertEqual([p["id"] for p in res["items"]], list(range(1, 21)))

    def test_last_partial_page(self):
        res = api.get_products(self.db, {"page": "3"})
        self.assertEqual([p["id"] for p in res["items"]], list(range(41, 46)))

    def test_past_the_end_is_empty(self):
        self.assertEqual(api.get_products(self.db, {"page": "4"})["items"], [])

    def test_per_page(self):
        self.assertEqual(len(api.get_products(self.db, {"per_page": "100"})["items"]), 45)

    def test_invalid_input_is_400(self):
        for query in ({"page": "0"}, {"page": "x"}, {"per_page": "101"}, {"per_page": "0"}, {"page": "-1"},
                      {"page": "99999999999999999999"}):
            self.assertEqual(api.get_products(self.db, query)["status"], 400, query)
