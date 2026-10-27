"""The weekly payroll run: hours, overtime and the export the payroll office imports."""

from . import exports, notify, rules
from .shifts import Week


def run(week: Week, people: list[dict], country: str) -> str:
    rows = []
    for person in people:
        hours = week.hours(person["name"])
        pay = rules.overtime_pay_uk if country == "uk" else rules.overtime_pay_de
        rows.append({**person, "contract_hours": hours, "overtime": pay(hours, person["rate_cents"])})
        notify.send_week(person["name"], f"{hours:.1f} hours this week")
    return exports.export_staff_csv(rows)


def absences(rows: list[dict]) -> str:
    return exports.export_absences_csv(rows)


def reshuffle(week: Week, index: int, earlier: bool, person: str) -> bool:
    moved = week.move_earlier(index) if earlier else week.move_later(index)
    if moved:
        notify.send_change(person, "your shift moved")
    return moved


def remind(person: str) -> int:
    return notify.send_reminder(person, "your shift starts in an hour")


def staff_pages(total: int) -> int:
    return notify.pages(total)
