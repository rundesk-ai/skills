"""Insurers codes and their display names."""

NAMES = {
    "AX": "Axis Health",
    "NV": "Nova Mutual",
    "PR": "Private, self-pay",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown insurer code: {code!r}") from None
