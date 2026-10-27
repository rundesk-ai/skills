+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "complex"
trap = "a staged change to a stored format; git diff without --cached shows nothing"
fixture = "events"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
The whole change is staged; `git diff` alone prints nothing.
must:
  M1 bug+rule  store.load now parses days as DD/MM/YYYY, but data/events.json holds years of bookings written as ISO dates; loading it raises ValueError ("time data '2024-03-05' does not match format '%d/%m/%Y'", reproduced), so the app cannot start for the centre. Breaks "Existing bookings must keep loading". The tests write a fresh file, so they stay green. Credit needs the existing stored data named and Blocking severity.
  M2 req  the requirement asked to show dates in UK format; the change also changes the stored format, which the requirement did not ask for. Fix: keep ISO in save and load, and format only in label. Credit if stated as the fix for M1.
good code:
  G1 save still writes a temp file and replaces atomically (unchanged).
decoys:
  D1 the em dashes in label: unchanged, intended.
taste:
  T1 the UK constant name; T2 dict-shaped events.
extras:
  X1 DD/MM/YYYY is ambiguous with US-format data if any ever arrives.
  X2 no test loads a file written by the previous version.
"""
+++
Review my changes before I open a pull request. The requirement: show event dates in UK format (DD/MM/YYYY) in the app.
