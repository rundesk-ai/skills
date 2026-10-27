# AGENTS

Ledger is a small invoicing library and CLI for a bookkeeping firm. Python 3.9+, standard library
only. Its data file is the only copy of every client's invoices.

## Rules

- **Money is integer cents.** Every amount is an `int` number of cents. Never use `float` for money:
  floats round wrongly and the books must balance to the cent.
- **Time comes from `ledger.clock.now()`.** It returns an aware UTC datetime. Never call
  `datetime.now()` or `datetime.utcnow()` directly: invoices are compared across time zones.
- **Only the owner or an admin may change an invoice.** Every function that changes an invoice
  takes the acting `User` and checks this before changing anything.
- **Writes go through `ledger.store.save`.** Nothing else writes the data file.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
