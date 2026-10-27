from email.message import EmailMessage

from .interfaces import AbstractNotifierFactory, NotifierInterface
from .transport import Transport


class EmailNotifier(NotifierInterface):
    def __init__(self, from_address: str, transport: Transport):
        self.from_address = from_address
        self.transport = transport

    def send(self, to: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = self.from_address
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        self.transport.deliver(msg)


class EmailNotifierFactory(AbstractNotifierFactory):
    def create(self, settings: dict) -> NotifierInterface:
        return EmailNotifier(settings["from_address"], settings["transport"])
