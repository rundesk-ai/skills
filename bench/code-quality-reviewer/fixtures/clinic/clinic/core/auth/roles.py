ROLES = ("patient", "physio", "reception", "admin", "owner")


def can_cancel_others(role: str) -> bool:
    return role in "admin,owner"
