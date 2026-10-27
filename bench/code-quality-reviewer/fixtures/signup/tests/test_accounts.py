import unittest

from signup import accounts


class AccountsTest(unittest.TestCase):
    def test_register_then_login(self):
        db = accounts.connect()
        accounts.register(db, "Ada@Example.com ", "correct horse battery")
        self.assertTrue(accounts.login(db, "ada@example.com", "correct horse battery"))
        self.assertFalse(accounts.login(db, "ada@example.com", "wrong password!"))

    def test_short_password_rejected(self):
        with self.assertRaises(ValueError):
            accounts.register(accounts.connect(), "b@example.com", "short")
