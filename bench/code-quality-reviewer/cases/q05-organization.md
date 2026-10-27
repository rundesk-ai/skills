+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "orders"
cases_version = 1
key = """
The code works: every test passes and no price is wrong. Every "must" item is about how it is written and organized.
must:
  M1 org   the discount rule is written three times: pricing.discount_bp (which nothing calls), inline in processing.process_order, and inline in web.quote. The copies agree today; the next change to the tiers must find all three, and a missed one shows the customer a quote that differs from checkout. Fix: call pricing.discount_bp from both.
  M2 org   processing.process_order does everything: reads the order file, validates, looks up the customer, prices, computes shipping, formats the receipt, writes it and prints. Pricing cannot be tested without writing files (the tests chdir into a temp dir to do it), and web.quote cannot reuse it. Fix: a pure function that prices an order (in pricing.py) and a thin process_order around it.
  M3 rule  pricing.tax_rate_bp opens and parses tax_rates.json on every call, breaking "pricing.py ... does no I/O"; it also reads from the current directory. Fix: load the rates once outside pricing and pass them in.
  M4 org   process_order(path, save, verbose): two boolean flags switch what it does, so call sites read `process_order(sys.argv[1], True, False)`. Fix: separate the side effects from the call, or keyword-only arguments at least.
  M5 org   customers.get_customer creates and writes a customer record when it is missing; a `get_` that writes misleads every caller (a price quote would create customers). Fix: name it get_or_create_customer, or split lookup from creation.
  M6 org   dead code: legacy_tax is never called and uses float money, and the commented-out `# tax = legacy_tax(...)` line remains. Fix: delete both.
  M7 org   shipping is computed by four-deep nested if/else inside process_order. A rate table by region and weight band, in pricing.py, makes the rule readable and testable. Credit if raised with M2 as part of extracting pricing, provided the shipping rule is named.
good code (no finding expected):
  G1 orders/money.py: integer cents, documented rounding, small and correct.
decoys:
  D1 percent_of rounds half up with integer arithmetic: correct.
  D2 the receipt formatting lines in process_order are repetitive but linear and plain; extracting a helper for them alone is taste.
  D3 customers.get_customer writes atomically (temp file then os.replace): correct.
taste:
  T1 missing type hints in pricing.py and customers.py; T2 variable names disc, f, q; T3 f-strings with nested quotes; T4 DB as a module constant.
extras:
  X1 tax_rates.json and customers.json are resolved against the working directory.
  X2 process_order does not validate that weight_g or region are present.
  X3 receipt path built with path.replace(".json", ...) misbehaves for a path with ".json" elsewhere in it.
"""
+++
Review the `orders` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
