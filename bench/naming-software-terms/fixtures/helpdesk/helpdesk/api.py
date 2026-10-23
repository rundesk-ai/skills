"""JSON API. Field names here are published: the mobile app and partner integrations read them."""
from typing import List

from .models import TicketData


def ticket_json(t: TicketData) -> dict:
    return {
        "id": t.id,
        "customer": t.client_id,
        "subject": t.subject,
        "state": t.status,
        "do_not_email": t.no_email,
        "opened": t.created_at,
        "closed": t.closed_at,
    }


def list_tickets(tickets: List[TicketData]) -> List[dict]:
    return [ticket_json(t) for t in tickets]
