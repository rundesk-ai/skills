import os
import tempfile
import unittest

from shipments import api, quotes
from shipments.store import Store

RATES = {"default": 120, "north": 200}


def make_store():
    folder = tempfile.mkdtemp()
    store = Store(os.path.join(folder, "data.json"))
    store.data["customers"]["1"] = {"id": "1", "name": "Mara Oduya"}
    store.data["routes"]["7"] = {"id": "7", "capacity": 50000, "load": 0}
    store.data["depots"]["N1"] = {"code": "N1"}
    return store


def request(**over):
    return dict({"customer_id": "1", "route_id": "7", "zone": "north", "destination": "4 Mill Lane", "weight": 2.5}, **over)


class ApiTest(unittest.TestCase):
    def test_quote_is_base_plus_rate_per_started_kilogram(self):
        self.assertEqual(api.quote(make_store(), RATES, request()), 450 + 200 * 3)

    def test_book_stores_the_parcel_and_returns_the_price(self):
        store = make_store()
        booked = api.book(store, RATES, request())
        self.assertEqual(booked["price_cents"], 1050)
        self.assertEqual(store.find_parcel(booked["parcel_id"])["drop_point"], "4 Mill Lane")

    def test_book_refuses_a_full_route(self):
        store = make_store()
        with self.assertRaises(api.BookingError):
            api.book(store, RATES, request(weight=51))

    def test_book_refuses_an_unknown_customer(self):
        with self.assertRaises(api.BookingError):
            api.book(make_store(), RATES, request(customer_id="9"))

    def test_requote_uses_the_stored_weight(self):
        store = make_store()
        booked = api.book(store, RATES, request())
        self.assertEqual(api.requote(store, RATES, booked["parcel_id"], "south"), 450 + 120 * 3)

    def test_label_shows_name_address_and_weight(self):
        store = make_store()
        booked = api.book(store, RATES, request())
        self.assertEqual(api.label(store, booked["parcel_id"]), "Mara Oduya\n4 Mill Lane\n2500 g")

    def test_assign_depot_refuses_an_unknown_code(self):
        store = make_store()
        booked = api.book(store, RATES, request())
        with self.assertRaises(api.BookingError):
            api.assign_depot(store, booked["parcel_id"], "ZZ")
        self.assertEqual(api.assign_depot(store, booked["parcel_id"], "N1")["depot"], "N1")


class QuotesTest(unittest.TestCase):
    def test_get_rate_falls_back_to_default(self):
        self.assertEqual(quotes.get_rate(RATES, "west"), 120)

    def test_check_route_refuses_over_capacity(self):
        self.assertFalse(quotes.check_route({"capacity": 1000, "load": 900}, 200))

    def test_fetch_rates_reads_the_file(self):
        path = os.path.join(tempfile.mkdtemp(), "rates.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"default": 120}')
        self.assertEqual(quotes.fetch_rates(path), {"default": 120})
