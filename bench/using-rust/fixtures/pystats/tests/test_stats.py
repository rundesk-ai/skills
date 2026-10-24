import unittest

from stats import summarize


class SummaryTest(unittest.TestCase):
    def test_report(self):
        self.assertEqual(summarize([2, 4, 6]), {"count": 3, "total": 12, "mean": 4.0, "max": 6})

    def test_empty_report(self):
        self.assertEqual(summarize([]), {"count": 0, "total": 0, "mean": None, "max": None})


if __name__ == "__main__":
    unittest.main()
