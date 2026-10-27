# AGENTS

`orders` prices and records orders for a small online tea shop: the checkout, the website's price
quotes and the order emails all use it. Python 3.9+, standard library only. Prices must be the same
wherever a customer sees them.

## Rules

- **Money is integer cents**, formatted only by `orders.money`.
- **`orders/pricing.py` holds the pricing rules and does no I/O.** It takes values and returns
  values, so prices can be tested without files.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
