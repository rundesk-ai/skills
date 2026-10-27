import secrets
from typing import Dict

from . import cache


def new_session(user: str, now: float) -> Dict:
    """A session for `user` signed in at `now`, expiring after the cache lifetime."""
    return {"user": user, "token": secrets.token_urlsafe(32), "expires": now + cache.ttl()}


def is_valid(session: Dict, now: float) -> bool:
    return now < session["expires"]
