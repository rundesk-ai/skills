from .config import NotifyConfig
from .registry import STRATEGIES, get_notifier


def send_welcome(tenant: dict, customer_email: str, config: NotifyConfig = NotifyConfig()) -> None:
    notifier = get_notifier("email", tenant["mail"])
    STRATEGIES[config.strategy].dispatch(
        notifier,
        customer_email,
        f"Welcome to {tenant['name']}",
        f"Your account with {tenant['name']} is ready.",
    )
