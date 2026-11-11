"""Every SQL statement in the app. Handlers call these functions and never see a connection."""
import os
import sqlite3

DB_PATH = os.environ.get("PANTRY_DB", os.path.join("data", "pantry.db"))
MIGRATIONS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "migrations")


def connect(path=None):
    path = path or DB_PATH
    if path != ":memory:":
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS applied (name TEXT PRIMARY KEY)")
    done = {row["name"] for row in conn.execute("SELECT name FROM applied")}
    for name in sorted(os.listdir(MIGRATIONS)):
        if name.endswith(".sql") and name not in done:
            with open(os.path.join(MIGRATIONS, name), encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.execute("INSERT INTO applied (name) VALUES (?)", (name,))
    conn.commit()


def all_items(conn):
    return conn.execute("SELECT * FROM items ORDER BY name").fetchall()


def add_item(conn, name, unit, quantity, low_at=1):
    conn.execute("INSERT INTO items (name, unit, quantity, low_at) VALUES (?, ?, ?, ?)",
                 (name, unit, quantity, low_at))
    conn.commit()


def use(conn, item_id, amount):
    """Take `amount` out of stock. Refuses to go below zero rather than clamping."""
    row = conn.execute("SELECT quantity FROM items WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        raise KeyError(item_id)
    if amount > row["quantity"]:
        raise ValueError("not enough in stock")
    conn.execute("UPDATE items SET quantity = quantity - ? WHERE id = ?", (amount, item_id))
    conn.commit()


def running_low(conn):
    return conn.execute("SELECT * FROM items WHERE quantity <= low_at ORDER BY name").fetchall()
