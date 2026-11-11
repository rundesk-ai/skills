# Architecture

Three layers, and each owns one thing.

| Layer | Files | Owns |
|---|---|---|
| Store | `pantry/store.py` | Every SQL statement. Nothing else imports `sqlite3`. |
| Handlers | `pantry/handlers/` | One request each: read the form, call the store, pick a template. |
| Templates | `pantry/templates/` | HTML. Values are escaped by `pantry/render.py`. |

The database is `data/pantry.db`, created on first run. Its schema is the numbered files in
`migrations/`, applied in order by `store.migrate()`; a migration that has shipped is never edited,
because the family's database has already run it.

Quantities are whole numbers of the item's unit. An item at or below its `low_at` is "running low".
