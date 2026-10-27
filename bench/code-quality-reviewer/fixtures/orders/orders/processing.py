import json

from . import pricing
from .customers import get_customer
from .money import cents_to_str, percent_of


def legacy_tax(subtotal):
    return int(subtotal * 0.08)


def process_order(path, save, verbose):
    with open(path) as f:
        order = json.load(f)
    if not order.get("items"):
        raise ValueError("an order needs at least one item")
    for item in order["items"]:
        if item["qty"] < 1 or item["price_cents"] < 0:
            raise ValueError(f"bad item: {item}")
    customer = get_customer(order["customer"])
    tier = customer["tier"]
    region = order["region"]
    subtotal = 0
    weight = 0
    for item in order["items"]:
        subtotal += item["price_cents"] * item["qty"]
        weight += item["weight_g"] * item["qty"]
    if tier == "gold":
        if subtotal >= 10_000:
            disc = 1000
        else:
            disc = 500
    else:
        if subtotal >= 20_000:
            disc = 500
        else:
            disc = 0
    discount = percent_of(subtotal, disc)
    # tax = legacy_tax(subtotal - discount)
    tax = percent_of(subtotal - discount, pricing.tax_rate_bp(region))
    if region == "domestic":
        if weight <= 1000:
            shipping = 500
        else:
            if weight <= 5000:
                shipping = 900
            else:
                shipping = 1500
    else:
        if region == "eu":
            if weight <= 1000:
                shipping = 1200
            else:
                shipping = 2500
        else:
            shipping = 4000
    if tier == "gold" and subtotal >= 10_000:
        shipping = 0
    total = subtotal - discount + tax + shipping
    lines = [f"Order for {order['customer']}"]
    for item in order["items"]:
        lines.append(f"  {item['qty']} x {item['name']}  {cents_to_str(item['price_cents'] * item['qty'])}")
    lines.append(f"Subtotal  {cents_to_str(subtotal)}")
    if discount:
        lines.append(f"Discount  -{cents_to_str(discount)}")
    lines.append(f"Tax       {cents_to_str(tax)}")
    lines.append(f"Shipping  {cents_to_str(shipping)}")
    lines.append(f"Total     {cents_to_str(total)}")
    receipt = "\n".join(lines)
    if save:
        with open(path.replace(".json", ".receipt.txt"), "w") as f:
            f.write(receipt + "\n")
    if verbose:
        print(receipt)
    return total
