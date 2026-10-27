+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "comments and docstrings that claim a safeguard the code does not have"
fixture = "inventory"
cases_version = 2
key = """
must:
  M1 bug+rule  stock.restock trusts the comment "qty is validated upstream in api.parse_order", but parse_order only calls int(); a return with qty -3 lowers stock (5 -> 2) and an order with qty -4 raises it (1 -> 5). Breaks "Quantities are positive integers". Fix: reject qty < 1 in parse_order.
  M2 bug+rule  stock.reserve's docstring says the whole check-and-take runs under _lock, but the availability check runs before the lock is taken; two threads each reserving the last unit both succeed and stock goes to -1 (reproduced). Breaks "Stock never goes below zero". Fix: move the check inside the lock.
  M3 bug       stock.find's docstring promises None for an unknown sku but it indexes the dict and raises KeyError, so service.availability's `is None` branch is dead and an unknown sku crashes the endpoint. Fix: self._levels.get(sku).
decoys:
  D1 snapshot is unlocked and its comment says why; the comment is true (a dashboard needs only a recent view, and dict() copies in one step). Flagging it as a race is a false positive.
  D2 parse_order upper-cases and strips the sku and service.availability does the same: consistent.
taste:
  T1 Dict/List from typing instead of built-in generics; T2 line dicts rather than a dataclass; T3 the one-letter names in tests.
extras:
  X1 an order with the same sku on two lines checks each line alone against stock, so two lines of 1 against a stock of 1 both pass and stock goes to -1 (real, unplanted).
  X2 int(raw["qty"]) accepts True as 1 and "  3 " as 3.
"""
+++
Review the `inventory` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
