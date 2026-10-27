"""Staff roles codes and their display names."""

NAMES = {
    "PHYSIO": "Physiotherapist",
    "RECEP": "Receptionist",
    "MGR": "Clinic manager",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown staff role code: {code!r}") from None
