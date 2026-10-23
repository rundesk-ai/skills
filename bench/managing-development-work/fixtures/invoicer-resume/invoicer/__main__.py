import argparse
from datetime import date

from . import recurring, store
from .models import Invoice, LineItem
from .report import format_cents, monthly_totals


def parse_item(text: str) -> LineItem:
    description, amount = text.rsplit(":", 1)
    return LineItem(description, int(amount))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="invoicer")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--client", required=True)
    create.add_argument("--item", action="append", required=True, type=parse_item)
    create.add_argument("--due", required=True, type=date.fromisoformat)
    create.add_argument("--issued", type=date.fromisoformat, default=None)
    sub.add_parser("list")
    show = sub.add_parser("show")
    show.add_argument("id", type=int)
    void = sub.add_parser("void")
    void.add_argument("id", type=int)
    report = sub.add_parser("report")
    report.add_argument("--month", required=True)
    schedule = sub.add_parser("schedule")
    schedule.add_argument("--client", required=True)
    schedule.add_argument("--item", action="append", required=True, type=parse_item)
    schedule.add_argument("--start", required=True, type=date.fromisoformat)
    generate = sub.add_parser("generate")
    generate.add_argument("--today", type=date.fromisoformat, default=None)
    args = parser.parse_args(argv)

    invoices = store.load()
    if args.command == "create":
        inv = Invoice(store.next_id(invoices), args.client, args.issued or date.today(), args.due, args.item)
        invoices.append(inv)
        store.save(invoices)
        print(f"created invoice {inv.id} for {inv.client}: {format_cents(inv.total_cents)}")
    elif args.command == "list":
        for inv in invoices:
            print(f"{inv.id}\t{inv.client}\t{inv.status}\t{format_cents(inv.total_cents)}\tdue {inv.due}")
    elif args.command == "show":
        inv = next(i for i in invoices if i.id == args.id)
        print(f"Invoice {inv.id} — {inv.client} ({inv.status})")
        for item in inv.items:
            print(f"  {item.description}: {format_cents(item.amount_cents)}")
        print(f"  Total: {format_cents(inv.total_cents)}")
    elif args.command == "void":
        inv = next(i for i in invoices if i.id == args.id)
        inv.status = "void"
        store.save(invoices)
        print(f"voided invoice {inv.id}")
    elif args.command == "report":
        totals = monthly_totals(invoices, args.month)
        for client, cents in sorted(totals.items()):
            if client != "__all__":
                print(f"{client}\t{format_cents(cents)}")
        print(f"TOTAL\t{format_cents(totals['__all__'])}")
    elif args.command == "schedule":
        schedules = recurring.load_schedules()
        new = recurring.Schedule(max((s.id for s in schedules), default=0) + 1, args.client, args.start, args.item)
        schedules.append(new)
        recurring.save_schedules(schedules)
        print(f"scheduled {new.cadence} invoices for {new.client} from {new.start}")
    elif args.command == "generate":
        schedules = recurring.load_schedules()
        created = recurring.generate(schedules, invoices, args.today or date.today())
        store.save(invoices)
        recurring.save_schedules(schedules)
        for inv in created:
            print(f"generated invoice {inv.id} for {inv.client} issued {inv.issued}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
