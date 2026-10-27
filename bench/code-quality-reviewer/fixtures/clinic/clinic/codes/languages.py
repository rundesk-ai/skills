"""Languages codes and their display names."""

NAMES = {
    "EN": "English",
    "FR": "French",
    "DE": "German",
    "ES": "Spanish",
}


def describe(code: str) -> str:
    try:
        return NAMES[code]
    except KeyError:
        raise ValueError(f"unknown language code: {code!r}") from None
