import unittest

from shipping import rates


class RatesTest(unittest.TestCase):
    def test_standard(self):
        self.assertEqual(rates.standard(2000), 495)
        self.assertEqual(rates.standard(8000), 0)

    def test_express_is_flat_and_never_free(self):
        self.assertEqual(rates.express(2000), 1295)
        self.assertEqual(rates.express(80000), 1295)

    def test_express_rejects_negative(self):
        with self.assertRaises(ValueError):
            rates.express(-1)

    def test_options(self):
        self.assertEqual(rates.options(8000), {"standard": 0, "express": 1295})
