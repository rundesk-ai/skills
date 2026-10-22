from dataclasses import dataclass, field, asdict
from datetime import date
from typing import List


@dataclass
class LineItem:
    description: str
    amount_cents: int


@dataclass
class Invoice:
    id: int
    client: str
    issued: date
    due: date
    items: List[LineItem] = field(default_factory=list)
    status: str = "open"  # open | paid | void

    @property
    def total_cents(self) -> int:
        return sum(item.amount_cents for item in self.items)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["issued"] = self.issued.isoformat()
        data["due"] = self.due.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Invoice":
        return cls(
            id=data["id"],
            client=data["client"],
            issued=date.fromisoformat(data["issued"]),
            due=date.fromisoformat(data["due"]),
            items=[LineItem(**item) for item in data["items"]],
            status=data.get("status", "open"),
        )
