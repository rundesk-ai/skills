# pantry

A household stock list one family runs on a small home server: what is in the cupboards, what is
running low, and a shopping list to print. Python 3.10+, standard library only, SQLite for storage.

```sh
make run      # http://localhost:8765
make test
make check
```

`docs/architecture.md` says how the parts fit. Releases are cut with `make release`.
