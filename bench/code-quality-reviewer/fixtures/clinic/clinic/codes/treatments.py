"""Treatments codes and their display names."""

NAMES = {
    "PT1": "Initial assessment",
    "PT2": "Follow-up session",
    "PT3": "Sports massage",
    "PT4": "Dry needling",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown treatment code: {code!r}") from None
