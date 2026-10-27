from . import db


class NotFound(Exception):
    pass


def get_user(user_id: int) -> dict:
    user = db.find_user(user_id)
    if user is None:
        raise NotFound(user_id)
    return user


def save_user(user: dict) -> None:
    db.save_user(user)
