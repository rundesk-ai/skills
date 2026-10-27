"""Rooms codes and their display names."""

NAMES = {
    "R1": "Room 1, ground floor",
    "R2": "Room 2, ground floor",
    "R3": "Gym studio",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown room code: {code!r}") from None
