from typing import Dict

from .email_notifier import EmailNotifierFactory
from .interfaces import AbstractNotifierFactory, NotifierInterface
from .strategy import DefaultNotificationStrategy

FACTORIES: Dict[str, AbstractNotifierFactory] = {"email": EmailNotifierFactory()}
STRATEGIES = {"default": DefaultNotificationStrategy()}
_instances: Dict[str, NotifierInterface] = {}


def get_notifier(kind: str, settings: dict) -> NotifierInterface:
    """The notifier for `kind`, built once and reused."""
    if kind not in _instances:
        _instances[kind] = FACTORIES[kind].create(settings)
    return _instances[kind]
