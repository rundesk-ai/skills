"""The public JSON view of a payout. The only place snake_case becomes camelCase."""


def payout_json(payout):
    return {
        "payeeId": payout.payee_id,
        "amountCents": payout.amount_cents,
        "paidAt": payout.paid_at,
        "settledAt": payout.settled_at,
        "chargebackCents": payout.chargeback_cents,
        "netCents": payout.amount_cents - payout.chargeback_cents,
    }
