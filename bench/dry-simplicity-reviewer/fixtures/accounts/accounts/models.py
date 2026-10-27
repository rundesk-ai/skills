from dataclasses import asdict, dataclass
from datetime import date


@dataclass
class User:
    id: int
    name: str
    email: str
    plan: str
    trial_ends: date
    active: bool = True

    @classmethod
    def from_dict(cls, raw: dict) -> "User":
        return cls(**raw)

    def to_dict(self) -> dict:
        return asdict(self)
