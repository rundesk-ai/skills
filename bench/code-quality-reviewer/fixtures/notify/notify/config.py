from dataclasses import dataclass, field
from typing import List


@dataclass
class NotifyConfig:
    strategy: str = "default"
    retries: int = 3
    backoff_seconds: float = 2.0
    priority: str = "normal"
    plugin_paths: List[str] = field(default_factory=list)
