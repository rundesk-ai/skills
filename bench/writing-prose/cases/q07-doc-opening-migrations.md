+++
skill = "writing-prose"
kind = "quality"
difficulty = "complex"
rubric = """
result.1  Opens from the reader's moment (they need to change the schema of a database people are using, and don't want a half-applied change), not from a definition of shiftdb.
result.2  States early what the reader will be able to do by the end of the page (write a migration and apply it safely).
result.3  Keeps every fact: migrations are SQL files in the `migrations` directory; each runs in a transaction; a failed one is rolled back, so the schema is never left half-changed; applied migrations are recorded in the `shiftdb_history` table. Invents none.
result.4  Speaks to "you"; ideas are connected (so, because, when, which means); sentence length and shape vary; no run of three sentences opening on the same subject.
result.5  Plain and specific: no "powerful", "seamless", "robust", "simply", "just", "it's worth noting", exclamation marks.
conduct.1 Contractions or a plain conversational register appear where natural; software keeps software verbs (it does not "know" or "decide").
"""
+++
Rewrite the opening of our docs page "Writing and applying migrations" for shiftdb, a command-line schema migration tool. Two short paragraphs at most; the steps follow it. Readers are backend developers.

Current opening:

> shiftdb is a schema migration tool. Migrations are stored as SQL files in the `migrations` directory. Each migration is applied in a transaction. Failed migrations are rolled back. Applied migrations are recorded in the `shiftdb_history` table. This page describes how to write and apply migrations.
