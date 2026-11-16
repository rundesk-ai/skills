+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "clean-readme"
expect_clean = true
cases_version = 1
key = """
must: none. Every claim in README.md matches stamp.py, the reader's first task comes first, and the prose is plain. The expected verdict is "No changes needed" or its equivalent.
decoys (correct; flagging is a false positive):
  D1 "A file with no front matter is skipped with a message on stderr" (true).
  D2 "--check ... exits with status 1 if there are any" (true; exit 0 otherwise).
  D3 The closing caveat that stamp records that someone said they reviewed, not that they did (honest and useful).
  D4 "Each file it changes is printed, one per line" (true, including under --check).
  D5 Asking for marketing-style intro, badges, or more sections.
taste:
  T1 install instructions absent (it is a single script run with python3); T2 the heading "In CI"; T3 no license line.
extras:
  X1 the README does not say what happens when the front matter has no closing "---" (the script raises).
"""
+++
Review the README for stamp in this folder before we publish it. stamp.py is the tool's source.
