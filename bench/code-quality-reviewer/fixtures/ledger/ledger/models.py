from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class User:
    name: str
    is_admin: bool = False


@dataclass
class Payment:
    cents: int
    at: datetime


@dataclass
class Invoice:
    id: int
    owner: str
    client: str
    total_cents: int
    created_at: datetime
    payments: List[Payment] = field(default_factory=list)
    voided_at: Optional[datetime] = None

    def paid_cents(self) -> int:
        return sum(p.cents for p in self.payments)

    def balance_cents(self) -> int:
        if self.voided_at is not None:
            return 0
        return self.total_cents - self.paid_cents()
