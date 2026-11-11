"""The data file: parcels, customers, routes and depots, kept as one JSON document.

Rows are plain dicts. A parcel row is {"id", "customer_id", "route_id", "drop_point", "weight"}.
"""
import json
import os
import tempfile


class Store:
    def __init__(self, path):
        self.path = path
        self.data = {"parcels": {}, "customers": {}, "routes": {}, "depots": {}}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        # Write beside the file, then replace it, so a crash never leaves half a document.
        folder = os.path.dirname(os.path.abspath(self.path))
        fd, tmp = tempfile.mkstemp(dir=folder, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(self.data, f)
        os.replace(tmp, self.path)

    def _mk_id(self, table):
        return str(len(self.data[table]) + 1)

    def add_parcel(self, row):
        row = dict(row, id=self._mk_id("parcels"))
        self.data["parcels"][row["id"]] = row
        self.save()
        return row

    def find_parcel(self, parcel_id):
        return self.data["parcels"].get(parcel_id)

    def find_customer(self, customer_id):
        return self.data["customers"].get(customer_id)

    def find_route(self, route_id):
        return self.data["routes"].get(route_id)

    def find_depot(self, code):
        return self.data["depots"][code]
