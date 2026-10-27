import json
import os
from datetime import datetime
from typing import Dict, List

from .models import Invoice, Payment

PATH = os.environ.get("LEDGER_DATA", "ledger.json")


def _decode(raw: Dict) -> Invoice:
    return Invoice(
        id=raw["id"],
        owner=raw["owner"],
        client=raw["client"],
        total_cents=raw["total_cents"],
        created_at=datetime.fromisoformat(raw["created_at"]),
        payments=[Payment(p["cents"], datetime.fromisoformat(p["at"])) for p in raw["payments"]],
        voided_at=datetime.fromisoformat(raw["voided_at"]) if raw.get("voided_at") else None,
    )


def _encode(inv: Invoice) -> Dict:
    return {
        "id": inv.id,
        "owner": inv.owner,
        "client": inv.client,
        "total_cents": inv.total_cents,
        "created_at": inv.created_at.isoformat(),
        "payments": [{"cents": p.cents, "at": p.at.isoformat()} for p in inv.payments],
        "voided_at": inv.voided_at.isoformat() if inv.voided_at else None,
    }


def load() -> List[Invoice]:
    if not os.path.exists(PATH):
        return []
    with open(PATH) as f:
        return [_decode(r) for r in json.load(f)]


def save(invoices: List[Invoice]) -> None:
    with open(PATH, "w") as f:
        json.dump([_encode(i) for i in invoices], f, indent=2)
    os.chmod(PATH, 0o600)
