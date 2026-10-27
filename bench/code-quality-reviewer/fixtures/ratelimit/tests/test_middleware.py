import unittest

from ratelimit import RateLimiter, RateLimitMiddleware, client_ip


def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"ok"]


class MiddlewareTest(unittest.TestCase):
    def call(self, mw, environ):
        seen = {}

        def start_response(status, headers):
            seen["status"], seen["headers"] = status, dict(headers)

        body = mw(environ, start_response)
        return seen["status"], seen["headers"], b"".join(body)

    def test_passes_then_429_with_retry_after(self):
        clock = lambda: 0.0
        mw = RateLimitMiddleware(app, RateLimiter(rate=0.25, burst=1, clock=clock))
        env = {"REMOTE_ADDR": "203.0.113.7"}
        self.assertEqual(self.call(mw, env)[0], "200 OK")
        status, headers, body = self.call(mw, env)
        self.assertEqual(status, "429 Too Many Requests")
        self.assertEqual(headers["Retry-After"], "4")
        self.assertEqual(body, b"Too many requests\n")

    def test_forwarded_header_is_not_the_key(self):
        env = {"REMOTE_ADDR": "203.0.113.7", "HTTP_X_FORWARDED_FOR": "198.51.100.1"}
        self.assertEqual(client_ip(env), "203.0.113.7")

    def test_custom_key_func(self):
        mw = RateLimitMiddleware(app, RateLimiter(rate=1, burst=1, clock=lambda: 0.0), key_func=lambda e: e["USER"])
        self.assertEqual(self.call(mw, {"USER": "a"})[0], "200 OK")
        self.assertEqual(self.call(mw, {"USER": "b"})[0], "200 OK")
        self.assertEqual(self.call(mw, {"USER": "a"})[0], "429 Too Many Requests")
