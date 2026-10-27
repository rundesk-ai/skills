from . import repo
from .models import User
from .plans import is_trial_expired, set_plan
from .repo import NotFound


def get_user(user_id: int) -> dict:
    return repo.get_user(user_id)


def deactivate(user_id: int) -> dict:
    user = repo.get_user(user_id)
    if user is None:
        raise NotFound(user_id)
    user["active"] = False
    repo.save_user(user)
    return user


def rename(user_id: int, name: str) -> dict:
    user = User.from_dict(repo.get_user(user_id))
    raw = user.to_dict()
    raw["name"] = name.strip()
    updated = User.from_dict(raw).to_dict()
    repo.save_user(updated)
    return updated


def change_plan(user_id: int, plan: str) -> dict:
    user = set_plan(repo.get_user(user_id), plan)
    repo.save_user(user)
    return user


def needs_upgrade_prompt(user_id: int, today) -> bool:
    return is_trial_expired(repo.get_user(user_id), today)
