import unittest

from wallet.accounts import Accounts, Insufficient


class AccountsTest(unittest.TestCase):
    def test_withdraw(self):
        a = Accounts({"ada": 1000})
        a.withdraw("ada", 400)
        self.assertEqual(a.balance("ada"), 600)

    def test_overdraw_refused(self):
        a = Accounts({"ada": 100})
        with self.assertRaises(Insufficient):
            a.withdraw("ada", 101)
