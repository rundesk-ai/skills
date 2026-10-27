import unittest

from vault.accounts import Accounts, Insufficient, UnknownAccount


class AccountsTest(unittest.TestCase):
    def test_withdraw(self):
        a = Accounts({"ada": 500})
        a.withdraw("ada", 200)
        self.assertEqual(a.balance("ada"), 300)

    def test_overdraw_refused(self):
        with self.assertRaises(Insufficient):
            Accounts({"ada": 100}).withdraw("ada", 101)

    def test_unknown_account(self):
        with self.assertRaises(UnknownAccount):
            Accounts({}).balance("nobody")
