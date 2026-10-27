from .interfaces import NotificationStrategy, NotifierInterface


class DefaultNotificationStrategy(NotificationStrategy):
    def dispatch(self, notifier: NotifierInterface, to: str, subject: str, body: str) -> None:
        notifier.send(to, subject, body)
