"""One weekly run: pay every payee who is owed something and is not blocked."""
from payouts import bank_adapter
from payouts.models import Payout


def weekly_run(payees, owed_cents, send, now):
    """Returns the payouts that were sent. `send` posts a bank request; `now` is the run's time."""
    sent = []
    for p in payees:
        amount = owed_cents.get(p.payee_id, 0)
        if amount <= 0 or p.is_blocked:
            continue
        payout = Payout(payee_id=p.payee_id, amount_cents=amount)
        send(bank_adapter.to_bank_request(p, payout))
        payout.paid_at = now
        sent.append(payout)
    return sent


def record_receipt(payout, receipt):
    """Copy what the bank said onto the payout."""
    payout.settled_at, payout.chargeback_cents = bank_adapter.from_bank_receipt(receipt)
    return payout
