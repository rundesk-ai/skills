import json
import os
import shutil
import tempfile
import unittest

from orders import web
from orders.processing import process_order

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class OrdersTest(unittest.TestCase):
    def setUp(self):
        self.old = os.getcwd()
        self.dir = tempfile.mkdtemp()
        shutil.copy(os.path.join(ROOT, "tax_rates.json"), self.dir)
        os.chdir(self.dir)

    def tearDown(self):
        os.chdir(self.old)
        shutil.rmtree(self.dir)

    def write_order(self, **order):
        with open("order.json", "w") as f:
            json.dump(order, f)
        return "order.json"

    def test_domestic_order_total(self):
        path = self.write_order(customer="c1", region="domestic",
                                items=[{"name": "Sencha", "qty": 2, "price_cents": 1250, "weight_g": 200}])
        # 2500 subtotal, no discount, 8% tax 200, shipping 500
        self.assertEqual(process_order(path, True, False), 3200)
        self.assertTrue(os.path.exists("order.receipt.txt"))

    def test_gold_customer_gets_discount_and_free_shipping(self):
        with open("customers.json", "w") as f:
            json.dump({"g1": {"id": "g1", "tier": "gold", "orders": 3}}, f)
        path = self.write_order(customer="g1", region="eu",
                                items=[{"name": "Gyokuro", "qty": 4, "price_cents": 3000, "weight_g": 300}])
        # 12000 subtotal, 10% off 1200, 20% tax on 10800 = 2160, free shipping
        self.assertEqual(process_order(path, False, False), 12960)

    def test_quote_matches_checkout(self):
        q = web.quote([{"price_cents": 3000, "qty": 4}], "gold", "eu")
        self.assertEqual(q["total"], "$129.60")

    def test_empty_order_rejected(self):
        with self.assertRaises(ValueError):
            process_order(self.write_order(customer="c1", region="eu", items=[]), False, False)
