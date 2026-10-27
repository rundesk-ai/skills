import unittest

from notify import registry
from notify.service import send_welcome
from notify.transport import OutboxTransport


class NotifyTest(unittest.TestCase):
    def setUp(self):
        registry._instances.clear()

    def test_welcome_mail(self):
        outbox = OutboxTransport()
        tenant = {"name": "Studio North", "mail": {"from_address": "hello@north.example", "transport": outbox}}
        send_welcome(tenant, "ada@example.com")
        msg = outbox.sent[0]
        self.assertEqual(msg["From"], "hello@north.example")
        self.assertEqual(msg["To"], "ada@example.com")
        self.assertIn("Studio North", msg["Subject"])
