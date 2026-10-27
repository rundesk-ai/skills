+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "code-quality-reviewer/orders"
cases_version = 1
key = """
must:
  M1 dup   the discount rule is written three times: pricing.discount_bp (which nothing calls), inline in processing.process_order, and inline in web.quote. The copies agree today; a change to the tiers must find all three, and a missed one shows a quote that differs from checkout. Consolidate: both call pricing.discount_bp.
  M2 dead  processing.legacy_tax is never called, and the commented-out `# tax = legacy_tax(...)` line remains. Delete both.
  M3 cplx  shipping in process_order is four-deep nested if/else by region and weight; a table of (region, max weight, price) in pricing.py makes it one lookup and testable. Credit if raised as part of pulling pricing out of process_order, provided shipping is named.
good code:
  G1 orders/money.py: two small helpers, each used; nothing to remove.
decoys:
  D1 the receipt lines in process_order repeat f-string shapes but each prints a different field; a helper for them alone is taste.
  D2 customers.get_customer's temp file then os.replace is the atomic-write idiom, not redundancy.
  D3 the subtotal loop and the weight loop in process_order iterate the same items; merging them into one loop is taste (it was already one loop).
taste:
  T1 type hints; T2 variable names; T3 f-string quoting.
extras (not required of this reviewer; neither hit nor false positive):
  X1 process_order mixes reading, pricing, formatting and writing; pricing cannot be tested without files.
  X2 pricing.tax_rate_bp opens a file on every call, against the "no I/O" rule.
  X3 the boolean flags in process_order(path, save, verbose).
  X4 get_customer writes when the customer is missing.
"""
+++
Look for duplication, redundancy and needless complexity in the `orders` package, and tell me what is worth consolidating or simplifying.
