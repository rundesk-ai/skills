"""Where a finished message goes. Production sends over SMTP; tests and staging keep an outbox."""

import smtplib
from email.message import EmailMessage
from typing import List


class Transport:
    def deliver(self, msg: EmailMessage) -> None:
        raise NotImplementedError


class SmtpTransport(Transport):
    def __init__(self, host: str, port: int = 587):
        self.host, self.port = host, port

    def deliver(self, msg: EmailMessage) -> None:
        with smtplib.SMTP(self.host, self.port, timeout=10) as smtp:
            smtp.starttls()
            smtp.send_message(msg)


class OutboxTransport(Transport):
    def __init__(self):
        self.sent: List[EmailMessage] = []

    def deliver(self, msg: EmailMessage) -> None:
        self.sent.append(msg)
