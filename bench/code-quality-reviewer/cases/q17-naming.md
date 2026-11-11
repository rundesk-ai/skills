+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "names that drift across files while every test passes; only one of them has caused a bug so far"
fixture = "shipments"
cases_version = 3
key = """
Every test passes. One must item is a bug a name caused; the other three are names that will cause the next one. Short local names are taste.
must:
  M1 bug   quotes.check_route says it checks, and its docstring says "True when the route can take this weight", but it also adds the weight to route["load"]. api.quote calls it, under a docstring that says "Changes nothing", so every price quote reserves capacity: 20 quotes of 2.5 kg fill a 50 kg route and bookings are then refused (reproduced). Fix: a check that only checks, and a separately named reserve that book alone calls.
  M2 name  one concept, three names: where the parcel goes is `destination` in the request (api.py), `drop_point` in the stored row (store.py, api.book) and `delivery_address` on the label (labels.py). A search for one name misses the other two, and the next change to it (validation, a second address) must find all three. Fix: one name in every layer.
  M3 name  `weight` holds kilograms in the request and in quotes.price_cents, and grams in the stored row, in quotes.check_route and on the label; api.book and api.quote multiply by 1000 and api.requote divides, and no name says which unit it holds. The next caller that passes a row's weight to price_cents, or a request's weight to check_route, is wrong by a factor of 1000 with no error. Fix: `weight_kg` and `weight_g`, or one unit throughout.
  M4 name  Store.find_parcel, find_customer and find_route return None for a missing key; Store.find_depot raises KeyError. The one caller today handles it, but the name promises the pattern its three siblings keep, so the next caller writes `if depot is None` and crashes instead. Fix: return None like the others, or name it for what it does.
good code (no finding expected):
  G1 Store.save writes a temporary file and replaces the data file: correct.
  G2 api._checked validates the customer, route, destination and weight before anything is stored: correct.
decoys:
  D1 quotes uses `fetch_` for the function that reads the rates file and `get_` for the in-memory lookup; the module docstring states the convention. Asking to unify them is a false positive.
  D2 api.assign_depot catches KeyError from find_depot: correct today (M4 is about the name, not this caller). Reporting the try/except as a bug is a false positive.
taste:
  T1 the short locals c, r, p in api.py; T2 Store._mk_id as a name; T3 no type hints; T4 "%d g" formatting in labels.py; T5 rows as plain dicts rather than classes.
extras:
  X1 the load that quote or book adds is saved only when a later call saves the store, so capacity differs between memory and the file.
  X2 Store._mk_id counts rows, so it would reuse an id if a parcel were ever deleted (nothing deletes today).
  X3 a request weight in kilograms times 1000 stores a float number of grams.
  X4 book reserves capacity before add_parcel, so a failed write leaves the capacity reserved.
"""
+++
Review the `shipments` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
