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

    def test_transfer(self):
        a = Accounts({"ada": 1000, "bob": 0})
        a.transfer("ada", "bob", 300)
        self.assertEqual((a.balance("ada"), a.balance("bob")), (700, 300))

    def test_transfer_more_than_balance_refused(self):
        a = Accounts({"ada": 100, "bob": 0})
        with self.assertRaises(Insufficient):
            a.transfer("ada", "bob", 101)
