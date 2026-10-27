import json
import os

DB = "customers.json"


def get_customer(customer_id):
    data = {}
    if os.path.exists(DB):
        with open(DB) as f:
            data = json.load(f)
    if customer_id not in data:
        data[customer_id] = {"id": customer_id, "tier": "standard", "orders": 0}
        with open(DB + ".tmp", "w") as f:
            json.dump(data, f)
        os.replace(DB + ".tmp", DB)
    return data[customer_id]
