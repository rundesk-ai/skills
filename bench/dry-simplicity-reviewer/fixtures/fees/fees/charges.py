from .money import percent_of

# Finance terms, section 4: interest on an invoice paid after its due date.
LATE_FEE_BP = 250

# Card network rules: the most we may add when a customer pays by card.
CARD_SURCHARGE_BP = 250


def late_fee(overdue_cents: int) -> int:
    return percent_of(overdue_cents, LATE_FEE_BP)


def card_surcharge(amount_cents: int) -> int:
    return percent_of(amount_cents, CARD_SURCHARGE_BP)
