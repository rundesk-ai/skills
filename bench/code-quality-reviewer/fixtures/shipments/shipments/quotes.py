"""Prices and route capacity.

Naming in this module: `fetch_` reads the rates file, `get_` looks a value up in memory.
"""
import json

BASE_CENTS = 450


def fetch_rates(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_rate(rates, zone):
    return rates.get(zone, rates["default"])


def price_cents(rates, zone, weight):
    """The price of sending `weight` to `zone`: a base fee plus the zone's rate per started kilogram."""
    r = get_rate(rates, zone)
    started = int(weight) if weight == int(weight) else int(weight) + 1
    return BASE_CENTS + r * max(1, started)


def check_route(route, weight):
    """True when the route can take this weight."""
    if route["load"] + weight > route["capacity"]:
        return False
    route["load"] += weight
    return True
