import unittest

from catalog import admin, cache, db, shipping
from catalog.prices import get_price, get_stock


class CatalogTest(unittest.TestCase):
    def setUp(self):
        cache.clear()
        db.PRICES.clear(); db.STOCK.clear(); db.PRODUCTS.clear()
        db.PRICES[("TEA-1", "eu")] = 1200
        db.STOCK["TEA-1"] = 7

    def test_price_is_cached(self):
        self.assertEqual(get_price("TEA-1", "eu"), 1200)
        db.PRICES[("TEA-1", "eu")] = 9999
        self.assertEqual(get_price("TEA-1", "eu"), 1200)

    def test_stock_update_invalidates(self):
        self.assertEqual(get_stock("TEA-1"), 7)
        admin.update_stock("TEA-1", 3)
        self.assertEqual(get_stock("TEA-1"), 3)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            admin.update_price("TEA-1", "eu", -1)

    def test_shipping_tiers(self):
        self.assertEqual(shipping.rate(0.5, "eu"), 495)
        self.assertEqual(shipping.rate(3, "eu"), 995)
        self.assertEqual(shipping.rate(6.2, "intl"), 2 * (995 + 400))
