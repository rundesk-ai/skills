from abc import ABC, abstractmethod


class NotifierInterface(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        ...


class AbstractNotifierFactory(ABC):
    @abstractmethod
    def create(self, settings: dict) -> NotifierInterface:
        ...


class NotificationStrategy(ABC):
    @abstractmethod
    def dispatch(self, notifier: NotifierInterface, to: str, subject: str, body: str) -> None:
        ...
