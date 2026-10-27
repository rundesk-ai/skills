def normalize(email: str) -> str:
    return email.strip().lower()


def looks_valid(email: str) -> bool:
    """A cheap shape check before sending: one @, something on each side, a dot in the domain."""
    local, at, domain = email.partition("@")
    return bool(at and local and "." in domain and "@" not in domain and not domain.startswith("."))
