import csv
import io
import sqlite3

from pantry import store


def export_csv(_conn):
    # Opens its own connection so a long export does not hold the request's one.
    conn = sqlite3.connect(store.DB_PATH)
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["name", "unit", "quantity", "low_at"])
    for row in conn.execute("SELECT name, unit, quantity, low_at FROM items ORDER BY name"):
        writer.writerow(row)
    conn.close()
    return 200, "text/csv", out.getvalue()
