# AGENTS

`coupons` applies discount codes at a shop's checkout. Python 3.9+, standard library only.
Marketing sends single-use codes to tens of thousands of customers at a time.

## Rules

- **Money is integer cents.**
- **A single-use code works exactly once**, for one order.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
