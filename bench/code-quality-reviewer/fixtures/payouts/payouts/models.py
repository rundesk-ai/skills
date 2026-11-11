"""The payee and the payout, as the rest of the package passes them around."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Payee:
    payee_id: str
    account_number: str
    is_blocked: bool = False  # on the compliance block list: never paid until compliance clears it


@dataclass
class Payout:
    payee_id: str
    amount_cents: int
    paid_at: Optional[str] = None      # when we asked the bank to pay
    settled_at: Optional[str] = None   # when the bank moved the money
    chargeback_cents: int = 0          # taken back by the bank after a dispute
