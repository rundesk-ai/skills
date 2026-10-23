import unittest

from helpdesk.api import ticket_json
from helpdesk.models import TicketData


class TicketJsonTest(unittest.TestCase):
    def test_published_fields(self):
        t = TicketData(7, 3, "Printer on fire", "open", True, "2026-10-01T09:00:00")
        self.assertEqual(
            ticket_json(t),
            {"id": 7, "customer": 3, "subject": "Printer on fire", "state": "open",
             "do_not_email": True, "opened": "2026-10-01T09:00:00", "closed": None},
        )
