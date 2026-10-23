from dataclasses import dataclass
from typing import Optional


@dataclass
class Client:
    id: int
    name: str
    email: str


@dataclass
class TicketData:
    id: int
    client_id: int
    subject: str
    status: str  # open | pending | closed
    no_email: bool
    created_at: str
    closed_at: Optional[str] = None
