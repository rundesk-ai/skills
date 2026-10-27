from typing import Dict, Optional

USERS: Dict[int, dict] = {}


def find_user(user_id: int) -> Optional[dict]:
    return USERS.get(user_id)


def save_user(user: dict) -> None:
    USERS[user["id"]] = user
