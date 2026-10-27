"""Reminder channels codes and their display names."""

NAMES = {
    "SMS": "Text message",
    "EMAIL": "Email",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown reminder channel code: {code!r}") from None
