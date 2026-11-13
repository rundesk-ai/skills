# Migrations

Migrations are code that runs once against production data, during a deploy, while the previous
release is still serving. Write them for that moment.

## Before committing one

```sh
python manage.py makemigrations --check        # model and migration state agree
python manage.py sqlmigrate <app> <number>     # the SQL it will run
python manage.py migrate --plan                # order across apps
```

Read the SQL. A migration that looks like a rename can be a drop and add, and a field with a default
can rewrite or lock the table depending on the engine and version; the database engine's own
guidance owns that judgment. Commit the migration with the model change that needs it, and never
edit a migration that has run anywhere shared: write a new one.

## Safe schema changes on a live table

Two releases run against one schema during a rolling deploy, so change it in steps the old code
survives (expand, migrate, contract):

| Change | Safe order |
|---|---|
| Add a column | add it nullable or with a default; backfill in batches; then add `NOT NULL` in a later migration |
| Remove a column | release code that no longer reads or writes it; then drop it in the next release |
| Rename a column or table | add the new one, write both, backfill, switch reads, then drop the old; or keep the database name with `db_column` / `db_table` |
| Add an index on a big PostgreSQL table | `AddIndexConcurrently` from `django.contrib.postgres.operations`, in a migration with `atomic = False` |
| Change a field's type | a new column and a backfill, not `AlterField` on a table that is being written |

`SeparateDatabaseAndState` changes Django's model state without touching the database, or the
reverse; use it to adopt a change already made, and say why in a comment.

## Data migrations

```python
def forward(apps, schema_editor):
    Order = apps.get_model("shop", "Order")          # the historical model, never an import
    Order.objects.filter(status="").update(status="pending")

def backward(apps, schema_editor):
    Order = apps.get_model("shop", "Order")
    Order.objects.filter(status="pending", legacy_blank=True).update(status="")

class Migration(migrations.Migration):
    dependencies = [("shop", "0012_order_legacy_blank")]
    operations = [migrations.RunPython(forward, backward)]
```

- Use `apps.get_model`; an imported model has today's fields and methods, and breaks the migration
  as soon as the model changes again. Custom model methods and `save()` overrides do not exist on
  historical models.
- Give every `RunPython` a reverse. Without one, `migrate <app> <previous>` raises
  `IrreversibleError` and a failed release cannot roll back. When there is nothing to undo, pass
  `migrations.RunPython.noop`. When the forward step loses information, record what it needs to undo,
  or state in the migration that it is one-way and why.
- Batch large updates (`iterator()` with chunks, or `update()` over primary-key ranges); one
  transaction over millions of rows holds locks and bloats the log. On PostgreSQL a migration is
  atomic by default; set `atomic = False` for a long batched backfill and make each batch commit.
- Keep schema and data operations in separate migrations on PostgreSQL; mixing them in one
  transaction can fail with pending trigger events.
- Prove it both ways: migrate forward, migrate back to the previous number, forward again, on a copy
  with realistic data.

## Merge conflicts

Two branches that each add `0013_*` to one app give two leaf nodes, and `migrate` refuses with
"Conflicting migrations detected".

- When neither branch has been deployed anywhere shared: delete one branch's new migration and
  regenerate it on top of the other with `makemigrations`. History stays linear.
- When both have run somewhere: `python manage.py makemigrations --merge`, read the merge migration,
  and check the two sides do not touch the same field. A merge migration resolves ordering only;
  it does not reconcile two changes to one column.
- A git conflict inside a migration file is resolved by regenerating, never by hand-merging
  operations.

## Squashing

`squashmigrations <app> <start> <end>` writes a replacement that runs on new databases, while
existing ones keep the originals. Keep the originals until every environment has migrated past the
squashed range, then delete them and remove `replaces` in a later release. `RunPython` operations
are copied into the squash unless marked `elidable=True`; check the squash still imports the
functions it references. Django 6.0 can squash a squashed migration.
