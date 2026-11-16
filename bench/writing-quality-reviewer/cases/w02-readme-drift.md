+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "easy"
fixture = "syncr-readme"
cases_version = 1
key = """
must:
  M1 fact  README lists `--preview`; syncr.py defines `--dry-run`. A reader who types `--preview` gets an error.
  M2 fact  README says `--retries` defaults to 3; syncr.py sets 5.
  M3 fact  README documents `--delete`; syncr.py has no such option and its comment says deletes are never performed. Readers expecting a mirror get an error, or a wrong belief about what the tool does.
  M4 reader  "the v2 path" is a private label the reader cannot know, and the Overview section says nothing ("In this section, we'll explore...").
  M5 sentences  The opening sentence is inflation with no content ("powerful, seamless solution... leverages a robust architecture"), and the usage text hides the actor ("The synchronization process is initiated...").
decoys:
  D1 `--exclude GLOB` is documented correctly; calling it wrong is a false positive (noting it is repeatable is an extra, not a decoy).
  D2 the usage example `syncr ./site s3://example-bucket` matches the argument order.
taste:
  T1 heading names; T2 bullet style for options.
extras:
  X1 `--exclude` is repeatable and the README does not say so.
  X2 "Simply run the command and everything will just work!" (minimizers, unsupported promise).
  X3 usage should come before options.
  X4 the code parses arguments and does nothing else, so the README's behavior claims cannot be confirmed from source.
"""
+++
Review the README for syncr in this folder before we publish the repository. syncr.py is the tool's source.
