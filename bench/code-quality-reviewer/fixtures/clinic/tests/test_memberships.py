import unittest
from datetime import date

from clinic.memberships import Membership, next_renewal


class MembershipTest(unittest.TestCase):
    def test_renewal_mid_month(self):
        m = Membership("pat", "BASIC", date(2026, 4, 1))
        self.assertEqual(next_renewal(m, date(2026, 4, 10)), date(2026, 5, 1))
