+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "defects that live between two files, each of which reads fine alone"
fixture = "catalog"
cases_version = 2
key = """
must:
  M1 bug+rule  admin.update_price invalidates cache.key("price", sku), but prices.get_price caches under cache.key("price", sku, region); the keys never match, so an updated price is never served until the process restarts (reproduced: 1200 still served after an update to 900). Breaks "Every write to a cached value invalidates its cache entry". Fix: invalidate cache.key("price", sku, region). Credit needs both files named.
  M2 bug       db.PRODUCTS documents "weight" in grams; shipping.rate's docstring takes kilograms; checkout.quote passes product["weight"] straight through, so a 250 g tin ships as 250 kg (reproduced: 49995 cents for one tin). Fix: divide by 1000 in quote, or make rate take grams. Credit needs the unit mismatch across the files.
good code:
  G1 admin.update_stock and prices.get_stock use the same key and are correct; tested.
decoys:
  D1 the cache has no TTL or size bound: the catalog is a fixed set of products, and correctness comes from invalidation, not expiry. Proposing a TTL as a fix for M1 instead of the key is a partial at best; proposing it as its own finding with no cost named is a false positive.
  D2 test_price_is_cached deliberately mutates db behind the cache to prove caching; correct.
taste:
  T1 module-level _store rather than a class; T2 db as module dicts; T3 the 0.999 rounding idiom; T4 Dict/Tuple typing imports.
extras:
  X1 int(weight - 5 + 0.999) is not a ceiling for weights a hair above a whole kilogram (5.0005 adds nothing); math.ceil is exact.
  X2 the module-level cache is shared by every importer and has no lock.
  X3 quote does not check qty >= 1.
"""
+++
Review the `catalog` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
