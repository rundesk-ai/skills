import unittest

from sessions import session
from sessions.cache import Cache


class SessionsTest(unittest.TestCase):
    def test_cache_expires(self):
        c = Cache()
        c.put("k", "v", now=1000)
        self.assertEqual(c.get("k", now=1100), "v")
        self.assertIsNone(c.get("k", now=1300))

    def test_cache_sub_second_ttl(self):
        from sessions import config
        old, config.TTL = config.TTL, 250
        try:
            c = Cache()
            c.put("k", "v", now=1000)
            self.assertEqual(c.get("k", now=1000.2), "v")
            self.assertIsNone(c.get("k", now=1000.3))
        finally:
            config.TTL = old

    def test_new_session_is_valid(self):
        s = session.new_session("ada", now=1000)
        self.assertTrue(session.is_valid(s, now=1001))
