# AGENTS

`reports` builds account pages and exports for a marketplace's support and finance teams. Python
3.9+, standard library only, SQLite in development and the same SQL in production. Production holds
about 40 million orders, 150 million order items and 2 million customers; the service runs for weeks
between restarts.

## Rules

- **Every query a request runs is bounded by an index** at production size.
- **Memory stays flat** over the life of the process.

## Build, test & run

```sh
python3 -m unittest discover -s tests -t .
```
