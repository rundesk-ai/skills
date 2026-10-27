import math
from typing import Callable, Dict, Iterable

from .bucket import RateLimiter


def client_ip(environ: Dict) -> str:
    # REMOTE_ADDR, not X-Forwarded-For: that header comes from the client, and trusting it would
    # let anyone pick a fresh key per request. Behind a trusted proxy, pass a key_func that reads
    # the header the proxy sets.
    return environ.get("REMOTE_ADDR", "unknown")


class RateLimitMiddleware:
    """WSGI middleware: passes a request through, or answers 429 with Retry-After."""

    def __init__(self, app: Callable, limiter: RateLimiter, key_func: Callable[[Dict], str] = client_ip):
        self._app = app
        self._limiter = limiter
        self._key_func = key_func

    def __call__(self, environ: Dict, start_response: Callable) -> Iterable[bytes]:
        key = self._key_func(environ)
        if self._limiter.allow(key):
            return self._app(environ, start_response)
        # Retry-After takes whole seconds; round up so a client that waits is never refused again.
        wait = max(1, math.ceil(self._limiter.retry_after(key)))
        start_response(
            "429 Too Many Requests",
            [("Content-Type", "text/plain; charset=utf-8"), ("Retry-After", str(wait))],
        )
        return [b"Too many requests\n"]
