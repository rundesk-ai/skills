+++
subject = "senior-code-reviewer"
kind = "quality"
difficulty = "medium"
heldout = true
fixture = "profiles"
cases_version = 1
key = """
clean_verdict is true when the review's final verdict lets the change land as it is: Ready, Approved, or Approved with conditions whose conditions do not include fixing a must item. Here the right verdict is not ready.
Held out: written after the first run, before the agent change it measures was run on it.
must:
  M1 bug+rule  pages.profilePage interpolates member.name into the <h1> without escapeHtml, while it escapes bio and joined; a display name of <script>steal()</script> renders as script on every visitor's view of that profile (reproduced): stored XSS, since anyone can register and pick a name. Breaks "Every user-supplied value is escaped with escapeHtml". The test uses the name "Ada", so it passes. Fix: escapeHtml(member.name). Credit needs Blocking or Important severity.
good code:
  G1 escapeHtml covers & < > " ' (unchanged); bio and joined are escaped in the new code.
decoys:
  D1 joined is escaped although it is a date: harmless and consistent with the rule.
  D2 the join("\\n") of template lines: fine.
taste:
  T1 template literal style; T2 the bio ?? '' default.
extras:
  X1 no test feeds markup in the name.
"""
+++
Review my uncommitted changes before I open a pull request. The requirement: add a public profile page showing a member's display name, bio and join date.
