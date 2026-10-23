import unittest
from datetime import date

from invoicer.models import LineItem
from invoicer.recurring import Schedule, generate, issue_dates


class MonthlyScheduleTest(unittest.TestCase):
    def schedule(self, start):
        return Schedule(1, "Acme", start, [LineItem("Retainer", 50000)])

    def test_issue_dates_monthly_up_to_today(self):
        dates = issue_dates(self.schedule(date(2026, 8, 15)), date(2026, 10, 15))
        self.assertEqual(dates, [date(2026, 8, 15), date(2026, 9, 15), date(2026, 10, 15)])

    def test_month_end_start_clamps_to_short_months(self):
        dates = issue_dates(self.schedule(date(2026, 1, 31)), date(2026, 3, 31))
        self.assertEqual(dates, [date(2026, 1, 31), date(2026, 2, 28), date(2026, 3, 31)])

    def test_generate_never_invoices_a_period_twice(self):
        schedules, invoices = [self.schedule(date(2026, 9, 1))], []
        first = generate(schedules, invoices, date(2026, 10, 1))
        again = generate(schedules, invoices, date(2026, 10, 1))
        self.assertEqual([inv.issued for inv in first], [date(2026, 9, 1), date(2026, 10, 1)])
        self.assertEqual(again, [])
        self.assertEqual(first[0].due, date(2026, 10, 1))
