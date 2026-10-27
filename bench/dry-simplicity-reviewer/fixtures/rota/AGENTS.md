# AGENTS

`rota` plans staff shifts for a chain of shops and sends each person their week. Python 3.12,
standard library only.

## Rules

- **Overtime follows each country's labour law.** `overtime_pay_uk` and `overtime_pay_de` look alike
  but answer to different statutes and change on different dates; keep them apart.
- **Times are minutes from midnight**, never datetime objects, inside the planner.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
