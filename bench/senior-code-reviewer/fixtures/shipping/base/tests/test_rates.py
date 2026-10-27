import unittest

from shipping import rates


class RatesTest(unittest.TestCase):
    def test_standard(self):
        self.assertEqual(rates.standard(2000), 495)
        self.assertEqual(rates.standard(8000), 0)
