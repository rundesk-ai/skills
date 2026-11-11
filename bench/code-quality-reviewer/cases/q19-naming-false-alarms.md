+++
subject = "code-quality-reviewer"
kind = "quality"
difficulty = "complex"
trap = "names that differ for good reasons: a vendor's fields, a layer's case, domain words, two moments that are not one"
fixture = "payouts"
expect_clean = true
cases_version = 4
key = """
must: none. The expected verdict is no bugs, no rule violations and no improvements: "No changes needed" or its equivalent. The code is correct and tested, and every difference between names below is deliberate and stated in AGENTS.md or a docstring.
decoys (each is correct; asking to rename, unify or expand it is a false positive):
  D1 the bank's field names `acct_no`, `amt`, `ccy`, `stl_dt`, `cb_amt` in bank_adapter.py: fixed by the bank's API and kept at the boundary, as AGENTS.md requires.
  D2 `payee_id` in Python and `payeeId` in api.payout_json (and the other camelCase keys): the stated convention, converted in one place. One term in each layer's form is not drift.
  D3 `paid_at` and `settled_at` are two different moments, defined in AGENTS.md and in models.py. Merging or renaming them is wrong.
  D4 `fetch_receipt` and `load_block_list` use different verbs for different acts (network and file); the module docstring states the convention.
  D5 `is_blocked` is a negative-sounding flag for a fact that is negative in the domain (the compliance block list).
  D6 `chargeback` and `payee` are the domain's own words.
  D7 `account_number` on Payee against the bank's `acct_no`: the mapping the adapter exists to make.
taste:
  T1 the loop variable `p` in run.weekly_run; T2 timestamps as strings; T3 the hard-coded "EUR"; T4 dataclasses without slots or frozen.
extras (arguable; neither hit nor false positive if raised as Unverified):
  X1 weekly_run sets paid_at after send returns, so a send that raises leaves no record of the attempt (the caller owns retries; nothing here says otherwise).
  X2 from_bank_receipt trusts cb_amt to be numeric.
"""
+++
Review the `payouts` package in this repository for code quality: bugs, AGENTS.md violations, and improvements worth fixing.
