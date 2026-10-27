"""Sends each person their week through the shop's messaging gateway."""

import json
import urllib.request

GATEWAY = "https://gateway.example.com/v1/messages"

# The staff list API returns people in pages of this many.
PAGE_SIZE = 30


def _post(payload: dict, timeout: int) -> int:
    request = urllib.request.Request(GATEWAY, data=json.dumps(payload).encode(), method="POST",
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status


def send_week(person: str, text: str) -> int:
    if not person:
        raise ValueError("person is required")
    return _post({"to": person, "kind": "week", "text": text}, timeout=30)


def send_change(person: str, text: str) -> int:
    if not person:
        raise ValueError("person is required")
    return _post({"to": person, "kind": "change", "text": text}, timeout=30)


def send_reminder(person: str, text: str) -> int:
    if not person:
        raise ValueError("person is required")
    return _post({"to": person, "kind": "reminder", "text": text}, timeout=30)


def pages(total_people: int) -> int:
    return -(-total_people // PAGE_SIZE)
