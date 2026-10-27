+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "easy"
fixture = "notes"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
must:
  M1 bug+rule  store.delete_note deletes by id alone (WHERE id = ?) and ignores owner, so any user deletes any other user's note (reproduced: ada deleted bob's note). Breaks "checks it belongs to the acting user". Fix: WHERE id = ? AND owner = ?. Credit needs Blocking or Important severity.
  M2 bug+rule  store.search_notes formats the search text into the SQL string; a term such as ' OR owner = 'bob' OR body LIKE ' returns another user's notes (reproduced), and quotes in ordinary searches break the query. Breaks "Every query takes parameters". Fix: body LIKE ? with the pattern as a parameter. Credit needs Blocking or Important severity.
good code:
  G1 add_note, get_note and list_notes: parameterized and owner-scoped (unchanged).
decoys:
  D1 delete_note raising NotFound when nothing was deleted: correct behaviour.
taste:
  T1 typing imports; T2 Optional imported and unused; T3 test names.
extras:
  X1 the new tests do not cover another user's delete or search (the gap that let M1 and M2 through).
  X2 LIKE wildcards % and _ in a search term are not escaped (after the M2 fix).
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: let a user delete one of their notes and search their own notes by text.
