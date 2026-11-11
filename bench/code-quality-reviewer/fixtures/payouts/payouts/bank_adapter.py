"""The bank's wire format, and nothing else. Its field names are the bank's, fixed by its API.

Naming in this package: `fetch_` talks to the network, `load_` reads a local file.
"""
import json


def to_bank_request(payee, payout):
    """Our payout as the bank's JSON body."""
    return {"acct_no": payee.account_number, "amt": payout.amount_cents, "ccy": "EUR"}


def from_bank_receipt(receipt):
    """The bank's receipt as (settled_at, chargeback_cents)."""
    return receipt.get("stl_dt"), int(receipt.get("cb_amt", 0))


def fetch_receipt(http_get, bank_reference):
    return json.loads(http_get("/receipts/" + bank_reference))


def load_block_list(path):
    with open(path, encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}
