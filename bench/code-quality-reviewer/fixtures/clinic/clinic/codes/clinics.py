"""Clinics codes and their display names."""

NAMES = {
    "N": "North clinic",
    "S": "South clinic",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown clinic code: {code!r}") from None
