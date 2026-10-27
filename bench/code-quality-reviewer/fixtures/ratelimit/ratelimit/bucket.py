"""Per-key token buckets: each key may spend `rate` tokens a second, in bursts of up to `burst`."""

import threading
import time
from typing import Callable, Dict, Tuple


class RateLimiter:
    def __init__(
        self,
        rate: float,
        burst: int,
        max_keys: int = 10_000,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if rate <= 0 or burst < 1 or max_keys < 1:
            raise ValueError("rate must be positive; burst and max_keys at least 1")
        self._rate = rate
        self._burst = burst
        self._max_keys = max_keys
        self._clock = clock
        self._lock = threading.Lock()
        # key -> (tokens, time of last refill). Dicts keep insertion order and every use
        # re-inserts its key, so the first key is always the least recently used.
        self._buckets: Dict[str, Tuple[float, float]] = {}

    def allow(self, key: str, cost: int = 1) -> bool:
        """Spend `cost` tokens from `key`'s bucket if it holds them; return whether it did."""
        self._check_cost(cost)
        with self._lock:
            now = self._clock()
            tokens = self._refilled(self._buckets.pop(key, None), now)
            allowed = tokens >= cost
            if allowed:
                tokens -= cost
            self._buckets[key] = (tokens, now)
            if len(self._buckets) > self._max_keys:
                # Evicting a key forgets its debt: it comes back with a full burst. That is the
                # price of bounded memory; size max_keys well above the number of active clients.
                del self._buckets[next(iter(self._buckets))]
            return allowed

    def retry_after(self, key: str, cost: int = 1) -> float:
        """Seconds until `allow(key, cost)` would succeed; 0.0 when it would succeed now."""
        self._check_cost(cost)
        with self._lock:
            tokens = self._refilled(self._buckets.get(key), self._clock())
            return max(0.0, (cost - tokens) / self._rate)

    def _check_cost(self, cost: int) -> None:
        if not 1 <= cost <= self._burst:
            raise ValueError(f"cost must be between 1 and burst ({self._burst}), got {cost}")

    def _refilled(self, bucket, now: float) -> float:
        if bucket is None:
            return float(self._burst)
        tokens, last = bucket
        return min(float(self._burst), tokens + max(0.0, now - last) * self._rate)
