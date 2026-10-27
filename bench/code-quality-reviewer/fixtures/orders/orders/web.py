from . import pricing
from .money import cents_to_str, percent_of


def quote(items, tier, region):
    """The price breakdown the website shows before checkout. Shipping is shown at checkout."""
    subtotal = sum(i["price_cents"] * i["qty"] for i in items)
    if tier == "gold":
        disc = 1000 if subtotal >= 10_000 else 500
    elif subtotal >= 20_000:
        disc = 500
    else:
        disc = 0
    discount = percent_of(subtotal, disc)
    tax = percent_of(subtotal - discount, pricing.tax_rate_bp(region))
    return {
        "subtotal": cents_to_str(subtotal),
        "discount": cents_to_str(discount),
        "tax": cents_to_str(tax),
        "total": cents_to_str(subtotal - discount + tax),
    }
