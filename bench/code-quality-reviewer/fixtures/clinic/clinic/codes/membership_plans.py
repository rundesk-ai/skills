"""Membership plans codes and their display names."""

NAMES = {
    "BASIC": "Basic, 2 sessions a month",
    "PLUS": "Plus, 4 sessions a month",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown membership plan code: {code!r}") from None
