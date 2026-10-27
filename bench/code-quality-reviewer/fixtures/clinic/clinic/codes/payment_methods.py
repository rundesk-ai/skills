"""Payment methods codes and their display names."""

NAMES = {
    "CARD": "Card",
    "CASH": "Cash",
    "INV": "Invoice to insurer",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown payment method code: {code!r}") from None
