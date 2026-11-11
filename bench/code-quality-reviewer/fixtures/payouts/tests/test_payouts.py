import json
import os
import tempfile
import unittest

from payouts import api, bank_adapter, run
from payouts.models import Payee, Payout


class WeeklyRunTest(unittest.TestCase):
    def setUp(self):
        self.payees = [Payee("p1", "NL01"), Payee("p2", "NL02", is_blocked=True), Payee("p3", "NL03")]
        self.requests = []

    def test_pays_what_is_owed_and_skips_blocked_and_zero(self):
        sent = run.weekly_run(self.payees, {"p1": 1250, "p2": 900, "p3": 0}, self.requests.append, "2026-03-02T09:00Z")
        self.assertEqual([(p.payee_id, p.amount_cents, p.paid_at) for p in sent], [("p1", 1250, "2026-03-02T09:00Z")])
        self.assertEqual(self.requests, [{"acct_no": "NL01", "amt": 1250, "ccy": "EUR"}])

    def test_a_payee_owed_nothing_is_not_sent(self):
        self.assertEqual(run.weekly_run(self.payees, {}, self.requests.append, "t"), [])
        self.assertEqual(self.requests, [])

    def test_receipt_sets_settlement_and_chargeback(self):
        payout = run.record_receipt(Payout("p1", 1250, paid_at="t"), {"stl_dt": "2026-03-04", "cb_amt": "250"})
        self.assertEqual((payout.settled_at, payout.chargeback_cents, payout.paid_at), ("2026-03-04", 250, "t"))

    def test_a_receipt_without_a_chargeback_means_none(self):
        self.assertEqual(run.record_receipt(Payout("p1", 1250), {"stl_dt": "2026-03-04"}).chargeback_cents, 0)


class AdapterTest(unittest.TestCase):
    def test_fetch_receipt_parses_the_banks_json(self):
        got = bank_adapter.fetch_receipt(lambda path: json.dumps({"path": path}), "R9")
        self.assertEqual(got, {"path": "/receipts/R9"})

    def test_load_block_list_ignores_blank_lines(self):
        path = os.path.join(tempfile.mkdtemp(), "blocked.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("p2\n\n p7 \n")
        self.assertEqual(bank_adapter.load_block_list(path), {"p2", "p7"})


class ApiTest(unittest.TestCase):
    def test_json_is_camel_case_with_the_net_amount(self):
        payout = Payout("p1", 1250, paid_at="a", settled_at="b", chargeback_cents=250)
        self.assertEqual(api.payout_json(payout), {"payeeId": "p1", "amountCents": 1250, "paidAt": "a",
                                                   "settledAt": "b", "chargebackCents": 250, "netCents": 1000})
