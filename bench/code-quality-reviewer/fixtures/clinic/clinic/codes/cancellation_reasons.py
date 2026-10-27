"""Cancellation reasons codes and their display names."""

NAMES = {
    "ILL": "Patient unwell",
    "CLN": "Clinic closed",
    "OTH": "Other",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown cancellation reason code: {code!r}") from None
