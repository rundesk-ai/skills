import unittest

from inventory import service
from inventory.stock import Stock


class StockTest(unittest.TestCase):
    def test_order_reserves_stock(self):
        stock = Stock({"TEA-1": 5})
        self.assertTrue(service.place_order(stock, {"lines": [{"sku": "tea-1", "qty": 2}]}))
        self.assertEqual(stock.snapshot()["TEA-1"], 3)

    def test_order_larger_than_stock_is_refused(self):
        stock = Stock({"TEA-1": 1})
        self.assertFalse(service.place_order(stock, {"lines": [{"sku": "TEA-1", "qty": 2}]}))
        self.assertEqual(stock.snapshot()["TEA-1"], 1)

    def test_return_adds_stock(self):
        stock = Stock({"TEA-1": 1})
        service.accept_return(stock, {"lines": [{"sku": "TEA-1", "qty": 2}]})
        self.assertEqual(stock.snapshot()["TEA-1"], 3)

    def test_availability(self):
        stock = Stock({"TEA-1": 0})
        self.assertEqual(service.availability(stock, "tea-1"), "sold out")
