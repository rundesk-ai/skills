# AGENTS

`payouts` sends weekly payouts to the sellers on a marketplace: it reads what each payee is owed,
asks the bank to pay it, and records what the bank said. Python 3.9+, standard library only.

## Rules

- **Money is integer cents.**
- **The public API speaks camelCase JSON**; Python and the database use snake_case. `api.py` is the
  only place that converts.
- **The bank's field names stay in `bank_adapter.py`.** Nothing else knows them.
- **`settled_at` is when the bank moved the money; `paid_at` is when we asked it to.** They are
  different moments, often days apart.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
