import os
import sqlite3

MIGRATIONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "migrations")


def migrate(db: sqlite3.Connection) -> None:
    """Applies every migration file in order."""
    for name in sorted(os.listdir(MIGRATIONS)):
        with open(os.path.join(MIGRATIONS, name)) as f:
            db.executescript(f.read())


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    migrate(db)
    return db
