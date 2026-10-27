import re


def normalize(phone: str) -> str:
    """Digits only, keeping a leading +: '+44 (0)20 7946 0018' becomes '+442079460018'."""
    phone = phone.strip()
    plus = "+" if phone.startswith("+") else ""
    return plus + re.sub(r"\D", "", phone.replace("(0)", ""))
