+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "board-strings"
cases_version = 1
key = """
must:
  M1 term  "Archive Workspace" breaks the guide's rule: the entity is a Board, never "workspace".
  M2 fact  `board.delete.body` hard-codes "3 lists"; a Board has any number (the API returns list_count), so the dialog states the wrong amount of what will be permanently lost. Needs the count with plural rules.
decoys (house style; flagging is a false positive):
  D1 Title Case on buttons and titles ("Create Board", "Delete Board?", "Delete Board").
  D2 The product speaking as "we" ("We'll permanently delete...", "We couldn't save...").
  D3 "Boards" capitalized mid-sentence in `board.empty` (the guide says always capitalized).
  D4 `board.save.error` (it matches the guide's own example and names a next step).
  D5 `board.rename.help` "Up to 64 characters." (verified by USAGE.md).
taste:
  T1 Title Case on the label "Board Name" (the guide is silent on labels).
  T2 "Board archived." being passive.
extras:
  X1 none planted.
"""
+++
Review strings.json before release. Our team's rules are in CONTENT-GUIDE.md, and USAGE.md says how the strings are used.
