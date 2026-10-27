import unittest
from datetime import date

from accounts import api, billing, db, service


def add_user(user_id, plan="free"):
    db.save_user({"id": user_id, "name": "Ada", "email": f"u{user_id}@example.com", "plan": plan,
                  "trial_ends": date(2026, 11, 1), "active": True})


class AccountsTest(unittest.TestCase):
    def setUp(self):
        db.USERS.clear()
        add_user(1)

    def test_get_and_rename(self):
        self.assertEqual(api.get_user(1)["name"], "Ada")
        self.assertEqual(service.rename(1, " Ada Quill ")["name"], "Ada Quill")

    def test_deactivate(self):
        self.assertFalse(service.deactivate(1)["active"])

    def test_post_plan(self):
        self.assertEqual(api.post_plan(1, {"plan": "Team"})["user"]["plan"], "team")
        self.assertEqual(api.post_plan(1, {"plan": "gold"})["status"], 422)

    def test_trial_prompt(self):
        self.assertTrue(service.needs_upgrade_prompt(1, date(2026, 11, 2)))

    def test_nightly_sync_retries_and_rejects_unknown_plans(self):
        for i in range(2, 205):
            add_user(i)
        calls = {"n": 0}

        def fetch_page(ids):
            calls["n"] += 1
            if calls["n"] == 1:
                raise billing.BillingUnavailable()
            return [{"user_id": i, "plan": "team"} for i in ids]

        self.assertEqual(billing.nightly_sync(fetch_page, list(range(1, 205))), 204)
        with self.assertRaises(ValueError):
            billing.nightly_sync(lambda ids: [{"user_id": 1, "plan": "gold"}], [1])
