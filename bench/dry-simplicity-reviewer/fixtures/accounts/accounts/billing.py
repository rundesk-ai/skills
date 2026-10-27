import time
from typing import Callable, Dict, List, TypeVar

from . import repo
from .plans import set_plan
from .utils import chunks, flatten

T = TypeVar("T")


class BillingUnavailable(Exception):
    pass


def with_retry(call: Callable[[], T], attempts: int = 3, pause: float = 0.5) -> T:
    """Runs `call`, retrying when the billing provider drops the request."""
    for attempt in range(1, attempts + 1):
        try:
            return call()
        except BillingUnavailable:
            if attempt == attempts:
                raise
            time.sleep(pause * attempt)
    raise AssertionError("unreachable")


def nightly_sync(fetch_page: Callable[[List[int]], List[Dict]], user_ids: List[int]) -> int:
    """Copies each user's plan from the billing provider, 100 users per request."""
    pages = [with_retry(lambda ids=ids: fetch_page(ids)) for ids in chunks(user_ids, 100)]
    changed = 0
    for record in flatten(pages):
        user = repo.get_user(record["user_id"])
        if user["plan"] != record["plan"]:
            repo.save_user(set_plan(user, record["plan"]))
            changed += 1
    return changed
