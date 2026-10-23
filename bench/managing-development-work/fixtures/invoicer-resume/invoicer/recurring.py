import calendar
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import List

from .models import Invoice, LineItem


@dataclass
class Schedule:
    id: int
    client: str
    start: date
    items: List[LineItem] = field(default_factory=list)
    cadence: str = "monthly"  # only monthly so far
    net_days: int = 30
    generated: List[str] = field(default_factory=list)  # issue dates already invoiced

    def to_dict(self) -> dict:
        data = asdict(self)
        data["start"] = self.start.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Schedule":
        return cls(
            id=data["id"],
            client=data["client"],
            start=date.fromisoformat(data["start"]),
            items=[LineItem(**item) for item in data["items"]],
            cadence=data.get("cadence", "monthly"),
            net_days=data.get("net_days", 30),
            generated=list(data.get("generated", [])),
        )


def schedules_path() -> Path:
    return Path(os.environ.get("INVOICER_SCHEDULES", "schedules.json"))


def load_schedules() -> List[Schedule]:
    path = schedules_path()
    if not path.exists():
        return []
    return [Schedule.from_dict(row) for row in json.loads(path.read_text())]


def save_schedules(schedules: List[Schedule]) -> None:
    schedules_path().write_text(json.dumps([s.to_dict() for s in schedules], indent=2))


def _monthly(start: date, n: int) -> date:
    month_index = start.month - 1 + n
    year, month = start.year + month_index // 12, month_index % 12 + 1
    return date(year, month, min(start.day, calendar.monthrange(year, month)[1]))


def issue_dates(schedule: Schedule, today: date) -> List[date]:
    """Every issue date from the schedule's start up to and including `today`."""
    if schedule.cadence != "monthly":
        raise ValueError(f"unsupported cadence: {schedule.cadence}")
    dates, n = [], 0
    while (d := _monthly(schedule.start, n)) <= today:
        dates.append(d)
        n += 1
    return dates


def generate(schedules: List[Schedule], invoices: List[Invoice], today: date) -> List[Invoice]:
    """Append an invoice for every due issue date not yet generated; return the new ones."""
    created = []
    for schedule in schedules:
        for issued in issue_dates(schedule, today):
            if issued.isoformat() in schedule.generated:
                continue
            next_id = max((inv.id for inv in invoices), default=0) + 1
            inv = Invoice(next_id, schedule.client, issued, issued + timedelta(days=schedule.net_days),
                          [LineItem(i.description, i.amount_cents) for i in schedule.items])
            invoices.append(inv)
            schedule.generated.append(issued.isoformat())
            created.append(inv)
    return created
