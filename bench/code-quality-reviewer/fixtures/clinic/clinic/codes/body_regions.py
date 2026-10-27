"""Body regions codes and their display names."""

NAMES = {
    "KNEE": "Knee",
    "SHLD": "Shoulder",
    "BACK": "Lower back",
    "NECK": "Neck",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown body region code: {code!r}") from None
