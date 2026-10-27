from typing import Any, Dict, Optional, Tuple

from . import config


def ttl() -> int:
    """How long an entry lives, in seconds."""
    return config.TTL


class Cache:
    def __init__(self) -> None:
        self._items: Dict[str, Tuple[float, Any]] = {}

    def put(self, key: str, value: Any, now: float) -> None:
        self._items[key] = (now + ttl(), value)

    def get(self, key: str, now: float) -> Optional[Any]:
        item = self._items.get(key)
        if item is None or item[0] <= now:
            return None
        return item[1]
