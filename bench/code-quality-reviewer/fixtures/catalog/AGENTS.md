# AGENTS

`catalog` serves product prices and shipping quotes for a shop that sells in several regions.
Python 3.9+, standard library only. Prices are read far more often than they change, so they are
cached; a stale price is a price the shop is legally bound to honour.

## Rules

- **Money is integer cents.**
- **Every write to a cached value invalidates its cache entry** in the same function.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
