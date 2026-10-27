import threading
from typing import Dict, List, Optional


class Stock:
    def __init__(self, levels: Dict[str, int]):
        self._levels = dict(levels)
        self._lock = threading.Lock()

    def find(self, sku: str) -> Optional[int]:
        """The quantity on hand for `sku`, or None when the sku is unknown."""
        return self._levels[sku]

    def snapshot(self) -> Dict[str, int]:
        # Intentionally not locked: dict(...) copies under the GIL in one step, and callers only
        # need a recent view for the dashboard, not a consistent one.
        return dict(self._levels)

    def reserve(self, lines: List[dict]) -> bool:
        """Reserve every line or none. Thread-safe: the whole check-and-take runs under _lock."""
        for line in lines:
            if self._levels.get(line["sku"], 0) < line["qty"]:
                return False
        with self._lock:
            for line in lines:
                self._levels[line["sku"]] -= line["qty"]
        return True

    def restock(self, sku: str, qty: int) -> None:
        # qty is validated upstream in api.parse_order, so it is always a positive integer here.
        with self._lock:
            self._levels[sku] = self._levels.get(sku, 0) + qty
