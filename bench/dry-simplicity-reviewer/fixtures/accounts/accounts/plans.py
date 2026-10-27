from datetime import date

PLANS = ("free", "team", "business")


def set_plan(user: dict, plan: str) -> dict:
    """Moves `user` to `plan`. Called by the API and by the nightly billing sync."""
    if plan not in PLANS:
        raise ValueError(f"unknown plan: {plan!r}")
    user["plan"] = plan
    return user


def is_trial_expired(user: dict, today: date) -> bool:
    return user["plan"] == "free" and user["trial_ends"] < today
