import json


def tax_rate_bp(region):
    with open("tax_rates.json") as f:
        return json.load(f)[region]


def discount_bp(subtotal_cents, tier):
    if tier == "gold":
        return 1000 if subtotal_cents >= 10_000 else 500
    if subtotal_cents >= 20_000:
        return 500
    return 0
