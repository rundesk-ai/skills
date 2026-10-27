import json
import os
from datetime import date
from typing import Dict, List

PATH = os.path.join("data", "events.json")


def load(path: str = PATH) -> List[Dict]:
    if not os.path.exists(path):
        return []
    with open(path) as f:
        rows = json.load(f)
    return [{**r, "day": date.fromisoformat(r["day"])} for r in rows]


def save(events: List[Dict], path: str = PATH) -> None:
    rows = [{**e, "day": e["day"].isoformat()} for e in events]
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(rows, f, indent=1)
    os.replace(tmp, path)


def label(event: Dict) -> str:
    """How an event is shown in the app."""
    return f"{event['title']} — {event['day'].isoformat()} — {event['room']}"
