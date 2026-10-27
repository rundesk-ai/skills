import importlib
from typing import List


def load_plugins(paths: List[str]) -> list:
    """Import each dotted path and return the modules, so third parties can add notifier kinds."""
    return [importlib.import_module(p) for p in paths]
