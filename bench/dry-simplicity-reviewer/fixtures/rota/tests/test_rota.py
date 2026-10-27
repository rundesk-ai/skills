import unittest

from rota import exports, rules
from rota.shifts import Shift, Week


class RotaTest(unittest.TestCase):
    def test_moving_a_shift_earlier_swaps_it_with_the_one_before(self):
        week = Week()
        week.add(Shift("ana", 540, 1020))
        week.add(Shift("ben", 600, 1080))
        self.assertTrue(week.move_earlier(1))
        self.assertEqual("ben", week.shifts[0].person)

    def test_the_last_shift_cannot_move_later(self):
        week = Week()
        week.add(Shift("ana", 540, 1020))
        self.assertFalse(week.move_later(0))

    def test_a_name_with_a_comma_is_quoted(self):
        csv = exports.export_staff_csv([{"name": "Lee, Sam", "shop": "north", "contract_hours": 38}])
        self.assertIn('"Lee, Sam"', csv)

    def test_overtime_starts_at_each_countrys_threshold(self):
        self.assertEqual(0, rules.overtime_pay_uk(48, 1000))
        self.assertEqual(1250, rules.overtime_pay_de(41, 1000))


if __name__ == "__main__":
    unittest.main()
