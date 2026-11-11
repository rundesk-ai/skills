"""What the booking desk and the website call.

A request is a dict: {"customer_id", "route_id", "zone", "destination", "weight"}.
"""
from shipments import labels, quotes


class BookingError(Exception):
    pass


def _checked(store, req):
    c = store.find_customer(req["customer_id"])
    if c is None:
        raise BookingError("unknown customer")
    r = store.find_route(req["route_id"])
    if r is None:
        raise BookingError("unknown route")
    if not req["destination"].strip():
        raise BookingError("a destination is required")
    if req["weight"] <= 0:
        raise BookingError("weight must be positive")
    return c, r


def quote(store, rates, req):
    """The price a customer would pay. Changes nothing."""
    _, r = _checked(store, req)
    if not quotes.check_route(r, req["weight"] * 1000):
        raise BookingError("the route is full")
    return quotes.price_cents(rates, req["zone"], req["weight"])


def book(store, rates, req):
    c, r = _checked(store, req)
    if not quotes.check_route(r, req["weight"] * 1000):
        raise BookingError("the route is full")
    row = store.add_parcel({
        "customer_id": c["id"],
        "route_id": r["id"],
        "drop_point": req["destination"].strip(),
        "weight": req["weight"] * 1000,
    })
    return {"parcel_id": row["id"], "price_cents": quotes.price_cents(rates, req["zone"], req["weight"])}


def requote(store, rates, parcel_id, zone):
    """The price of an already booked parcel if it went to another zone."""
    p = store.find_parcel(parcel_id)
    if p is None:
        raise BookingError("unknown parcel")
    return quotes.price_cents(rates, zone, p["weight"] / 1000)


def label(store, parcel_id):
    p = store.find_parcel(parcel_id)
    if p is None:
        raise BookingError("unknown parcel")
    return labels.label_text(p, store.find_customer(p["customer_id"]))


def assign_depot(store, parcel_id, code):
    p = store.find_parcel(parcel_id)
    if p is None:
        raise BookingError("unknown parcel")
    try:
        depot = store.find_depot(code)
    except KeyError:
        raise BookingError("unknown depot") from None
    p["depot"] = depot["code"]
    store.save()
    return p
