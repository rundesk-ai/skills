from . import service
from .plans import PLANS


def get_user(user_id: int) -> dict:
    return service.get_user(user_id)


def post_plan(user_id: int, body: dict) -> dict:
    plan = str(body.get("plan", "")).strip().lower()
    if plan not in PLANS:
        return {"status": 422, "error": f"plan must be one of {', '.join(PLANS)}"}
    return {"status": 200, "user": service.change_plan(user_id, plan)}
