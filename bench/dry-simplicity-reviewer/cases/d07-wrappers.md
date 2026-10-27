+++
subject = "dry-simplicity-reviewer"
kind = "quality"
difficulty = "complex"
trap = "redundant layers and checks beside wrappers and checks that earn their place"
fixture = "accounts"
cases_version = 1
key = """
must:
  M1 cplx  pass-through layers: api.get_user only calls service.get_user, which only calls repo.get_user; repo.save_user only calls db.save_user. Each forward is a file to change when the signature changes and a hop to trace when reading. Simplify: callers use repo.get_user directly (it earns its place, see G1), and service/api keep only functions that do something.
  M2 stdlib utils.chunks and utils.flatten reimplement itertools.batched and itertools.chain.from_iterable (Python 3.12, per AGENTS.md; identical results, checked). Replace and delete utils.py.
  M3 dead  service.deactivate checks `if user is None` after repo.get_user, which raises NotFound for a missing user and never returns None; the branch cannot run. Delete it.
  M4 cplx  service.rename converts dict -> User -> dict -> User -> dict; the conversions undo each other and the result is the same dict with a new name. Simplify to updating the dict (or keep one User round trip if validation is wanted, and say so).
good code:
  G1 repo.get_user translates a missing row into NotFound: a real job, not a pass-through.
decoys (each looks redundant; removing it is a false positive):
  D1 billing.with_retry is a wrapper, but it retries the billing provider's dropped requests, which AGENTS.md requires.
  D2 plans.set_plan validates the plan although api.post_plan already validates it, because the nightly billing sync calls set_plan directly; removing the check lets an unknown plan from billing through (the test covers it).
  D3 plans.is_trial_expired is a single-use helper, but its name states the rule its two conditions encode.
taste:
  T1 typing List/Dict/Optional on 3.12; T2 db as a module dict; T3 the raise AssertionError("unreachable") after the retry loop.
extras:
  X1 needs_upgrade_prompt is a one-line forward to is_trial_expired over repo.get_user; fair to fold into M1 or leave.
  X2 api.post_plan normalizes case and whitespace but set_plan does not, so the billing sync must send lower-case plans.
  X3 deleting models.py: User is used only by rename's round trip, so once M4 is fixed nothing uses it. (Corrected 2026-10-26 after the first run: this was a decoy, D4, which every arm in every run flagged, rightly; scores for that run are reported both with and without it.)
"""
+++
Look for duplication, redundancy and needless complexity in the `accounts` package, and tell me what is worth consolidating or simplifying.
