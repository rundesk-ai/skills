import threading
import unittest

from vault.accounts import Accounts, Insufficient, NotEmpty, UnknownAccount


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

    def test_close_empty_account(self):
        a = Accounts({"ada": 0})
        a.close("ada")
        with self.assertRaises(UnknownAccount):
            a.balance("ada")

    def test_close_refuses_money_left(self):
        a = Accounts({"ada": 1})
        with self.assertRaises(NotEmpty):
            a.close("ada")
        self.assertEqual(a.balance("ada"), 1)

    def test_close_unknown(self):
        with self.assertRaises(UnknownAccount):
            Accounts({}).close("nobody")

    def test_concurrent_withdraw_and_close_never_lose_money(self):
        for _ in range(200):
            a = Accounts({"ada": 1})
            results = []

            def withdraw():
                try:
                    a.withdraw("ada", 1)
                    results.append("withdrew")
                except (Insufficient, UnknownAccount):
                    results.append("refused")

            def close():
                try:
                    a.close("ada")
                    results.append("closed")
                except (NotEmpty, UnknownAccount):
                    results.append("kept")

            threads = [threading.Thread(target=withdraw), threading.Thread(target=close)]
            [t.start() for t in threads]
            [t.join() for t in threads]
            self.assertIn(sorted(results), [["kept", "withdrew"], ["closed", "withdrew"]])
