FREE_MAIL = {"freemail.example", "webmail.example", "inbox.example"}


def _well_formed(email: str) -> bool:
    local, at, domain = email.partition("@")
    return bool(at and local and "." in domain and "@" not in domain)


def valid_signup_email(email: str) -> bool:
    """Sign-ups must come from a company domain, not a free mail provider."""
    email = email.strip().lower()
    return _well_formed(email) and email.partition("@")[2] not in FREE_MAIL


def valid_billing_email(email: str) -> bool:
    """Billing contacts may use any address, plus-addressing included (ap+invoices@example.com)."""
    email = email.strip().lower()
    return _well_formed(email)
