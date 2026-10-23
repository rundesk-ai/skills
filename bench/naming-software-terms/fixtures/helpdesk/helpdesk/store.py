import sqlite3
from typing import List

from .models import Client, TicketData


def connect(path: str = "helpdesk.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init(conn: sqlite3.Connection) -> None:
    with open("schema.sql") as f:
        conn.executescript(f.read())


def get_clients(conn: sqlite3.Connection) -> List[Client]:
    return [Client(r["id"], r["name"], r["email"]) for r in conn.execute("SELECT * FROM cust")]


def fetch_tickets(conn: sqlite3.Connection) -> List[TicketData]:
    rows = conn.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    return [
        TicketData(r["id"], r["cust_id"], r["subject"], r["status"], bool(r["flg_2"]), r["created_at"], r["closed_at"])
        for r in rows
    ]


def retrieve_ticket(conn: sqlite3.Connection, ticket_id: int) -> TicketData:
    r = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    return TicketData(r["id"], r["cust_id"], r["subject"], r["status"], bool(r["flg_2"]), r["created_at"], r["closed_at"])
