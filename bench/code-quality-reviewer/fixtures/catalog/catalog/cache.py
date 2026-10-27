from typing import Any, Dict, Optional

_store: Dict[str, Any] = {}


def key(*parts: str) -> str:
    return ":".join(parts)


def get(k: str) -> Optional[Any]:
    return _store.get(k)


def put(k: str, value: Any) -> None:
    _store[k] = value


def invalidate(k: str) -> None:
    _store.pop(k, None)


def clear() -> None:
    _store.clear()
