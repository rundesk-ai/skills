import threading
import unittest

from ratelimit import RateLimiter


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


class BucketTest(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.limiter = RateLimiter(rate=2, burst=3, max_keys=3, clock=self.clock)

    def test_burst_then_refused(self):
        self.assertEqual([self.limiter.allow("a") for _ in range(4)], [True, True, True, False])

    def test_refills_at_rate_up_to_burst(self):
        for _ in range(3):
            self.limiter.allow("a")
        self.clock.now += 0.5
        self.assertTrue(self.limiter.allow("a"))
        self.assertFalse(self.limiter.allow("a"))
        self.clock.now += 100
        self.assertEqual([self.limiter.allow("a") for _ in range(4)], [True, True, True, False])

    def test_keys_are_independent(self):
        for _ in range(3):
            self.limiter.allow("a")
        self.assertTrue(self.limiter.allow("b"))

    def test_cost_outside_burst_is_rejected(self):
        for bad in (0, 4):
            with self.assertRaises(ValueError):
                self.limiter.allow("a", cost=bad)
            with self.assertRaises(ValueError):
                self.limiter.retry_after("a", cost=bad)

    def test_retry_after(self):
        self.assertEqual(self.limiter.retry_after("a"), 0.0)
        for _ in range(3):
            self.limiter.allow("a")
        self.assertAlmostEqual(self.limiter.retry_after("a"), 0.5)
        self.assertAlmostEqual(self.limiter.retry_after("a", cost=3), 1.5)

    def test_clock_going_backwards_adds_no_tokens(self):
        for _ in range(3):
            self.limiter.allow("a")
        self.clock.now -= 50
        self.assertFalse(self.limiter.allow("a"))

    def test_memory_bounded_least_recent_evicted(self):
        for key in "abc":
            self.limiter.allow(key)
        self.limiter.allow("a")
        self.limiter.allow("d")
        self.assertEqual(list(self.limiter._buckets), ["c", "a", "d"])

    def test_invalid_settings(self):
        for args in ((0, 1), (1, 0), (1, 1, 0)):
            with self.assertRaises(ValueError):
                RateLimiter(*args)

    def test_concurrent_callers_never_overspend(self):
        limiter = RateLimiter(rate=0.001, burst=50, clock=self.clock)
        allowed = []
        lock = threading.Lock()

        def hammer():
            for _ in range(20):
                ok = limiter.allow("shared")
                with lock:
                    allowed.append(ok)

        threads = [threading.Thread(target=hammer) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(sum(allowed), 50)
