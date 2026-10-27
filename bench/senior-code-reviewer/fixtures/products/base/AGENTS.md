# AGENTS

`products` serves the product list for a shop's storefront API. Python 3.9+, standard library and
SQLite. The catalog holds about 40,000 products.

## Rules

- **Every query takes parameters.**
- **Invalid request input is answered with 400 by `products/api.py`**, never a 500. Where the
  checks live is up to the change; the store may enforce its own limits.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
