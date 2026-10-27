import unittest
from datetime import date

from signups import db as dbmod
from signups.register import register


class RegisterTest(unittest.TestCase):
    def test_register(self):
        db = dbmod.connect()
        uid = register(db, " ada@example.com ", date(2026, 10, 1))
        self.assertEqual(db.execute("SELECT email FROM users WHERE id = ?", (uid,)).fetchone()[0], "ada@example.com")
