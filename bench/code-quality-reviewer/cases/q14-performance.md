+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "code that is correct and fast in tests but collapses at the stated production size"
fixture = "reports"
cases_version = 2
key = """
Every must item needs the cost at the size AGENTS.md states, not "could be faster".
must:
  M1 rule  accounts.customer_orders filters orders by customer_id, and schema.sql has no index on orders(customer_id): the plan is SCAN orders plus a temp B-tree sort (reproduced), so every account page scans 40 million rows. Breaks "Every query a request runs is bounded by an index". Fix: CREATE INDEX ON orders(customer_id, created_at).
  M2 perf  accounts.order_summaries runs one query per order (50 queries for 50 orders, reproduced): an N+1 that costs a round trip per order against the production database. Fix: one query with order_id IN (...) GROUP BY order_id.
  M3 perf  accounts.unique_emails checks membership in a list, so it is quadratic: 10k rows 0.3 s, 20k 1.1 s, 40k 4.6 s (reproduced); a finance export over 2 million customers does not finish. Fix: a set for membership beside the list, or dict.fromkeys.
  M4 rule  accounts._tax_cache keeps one entry per order forever (200k entries after 200k orders, reproduced) in a process that runs for weeks over 40 million orders. Breaks "Memory stays flat". The value is one multiplication, so the cache buys nothing. Fix: delete the cache.
good code:
  G1 rate_bp's functools.lru_cache(maxsize=256) is bounded and keyed by country; correct.
  G2 db.insert_orders uses executemany; correct.
  G3 order_items has an index on order_id, so each query in M2 is indexed: the cost there is the number of round trips, not a scan.
decoys:
  D1 totals_by_currency loops over the orders once per currency, but CURRENCIES has three entries and the orders are one customer's: linear and fine. Calling it quadratic is a false positive.
  D2 SELECT * in customer_orders: the page shows every column; preference.
taste:
  T1 row_factory set globally; T2 typing List/Dict imports; T3 the rate table inline in rate_bp.
extras:
  X1 customer_orders has no LIMIT, so a customer with very many orders loads all of them into one page.
  X2 rate_bp returns 0 for an unknown country rather than refusing it.
"""
+++
Review the `reports` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
