import unittest

from ledger import cli, importer


class AmountTest(unittest.TestCase):
    def test_export_amount(self):
        self.assertEqual(importer.parse_amount("1234.56"), 123456)
        self.assertEqual(importer.parse_amount("7"), 700)

    def test_typed_amount(self):
        self.assertEqual(cli.parse_amount("1.234,56"), 123456)
        self.assertEqual(cli.parse_amount("1,234.56"), 123456)
