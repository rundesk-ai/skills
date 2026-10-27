from datetime import datetime
from typing import List

from . import clock
from .models import Invoice, Payment, User


class Forbidden(Exception):
    pass


def _check_can_change(user: User, inv: Invoice) -> None:
    if not (user.is_admin or user.name == inv.owner):
        raise Forbidden(f"{user.name} may not change invoice {inv.id}")


def find(invoices: List[Invoice], invoice_id: int) -> Invoice:
    for inv in invoices:
        if inv.id == invoice_id:
            return inv
    raise KeyError(invoice_id)


def create(invoices: List[Invoice], user: User, client: str, total_cents: int) -> Invoice:
    if total_cents <= 0:
        raise ValueError("an invoice total must be positive")
    next_id = max((i.id for i in invoices), default=0) + 1
    inv = Invoice(next_id, user.name, client, total_cents, clock.now())
    invoices.append(inv)
    return inv


def record_payment(invoices: List[Invoice], user: User, invoice_id: int, cents: int) -> Invoice:
    inv = find(invoices, invoice_id)
    _check_can_change(user, inv)
    if cents <= 0:
        raise ValueError("a payment must be positive")
    if cents > inv.balance_cents():
        raise ValueError("payment exceeds the balance")
    inv.payments.append(Payment(cents, clock.now()))
    return inv


def refund(invoices: List[Invoice], user: User, invoice_id: int, cents: int) -> Invoice:
    inv = find(invoices, invoice_id)
    _check_can_change(user, inv)
    if cents <= 0:
        raise ValueError("a refund must be positive")
    inv.payments.append(Payment(-cents, clock.now()))
    return inv


def void(invoices: List[Invoice], user: User, invoice_id: int) -> Invoice:
    inv = find(invoices, invoice_id)
    inv.voided_at = clock.now()
    return inv


def apply_late_fee(inv: Invoice, rate_percent: int) -> Invoice:
    fee = inv.balance_cents() * (rate_percent / 100)
    inv.total_cents = inv.total_cents + int(fee)
    return inv


def overdue(invoices: List[Invoice], days: int) -> List[Invoice]:
    today = datetime.now()
    out = []
    for inv in invoices:
        if inv.balance_cents() > 0:
            if (today - inv.created_at).days > days:
                out.append(inv)
    return out
