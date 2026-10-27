"""Referral sources codes and their display names."""

NAMES = {
    "GP": "General practitioner",
    "WEB": "Website",
    "WOM": "Word of mouth",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown referral source code: {code!r}") from None
