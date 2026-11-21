+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "natural-install"
expect_clean = true
cases_version = 2
key = """
must:
  M1 promise  The opening promises "your first folder syncing", and the page stops at install (an unplanted defect the first run found; the key was corrected after it). Every other fact traces to FACTS.md and the sentences are natural and varied, so beyond M1 the expected result is at most one minor finding with a fix that keeps every detail and the register.
decoys (flagging as something to change, or proposing the rewrite, is a false positive):
  D1 Rewriting "signed with a Developer ID and notarized by Apple, with its own notarization ticket, so it opens even when you're offline" in any way that drops the notarization ticket or replaces "even when you're offline" with a more formal phrase ("without a network connection").
  D2 Removing or expanding contractions (you'll, it's, you're, won't).
  D3 Splitting the long, connected sentences into short declaratives, or asking for a named actor in each.
  D4 Replacing "Say yes" or "change your mind" with formal wording ("Grant access", "revoke permission").
  D5 Calling the text AI-written.
taste (neither):
  T1 the heading wording; T2 whether to link "downloads page"; T3 "Privacy & Security" punctuation.
extras (real, unplanted):
  X1 the page never says what to do if the DMG does not open; neutral.
"""
+++
Review install.md before it goes on our public docs. FACTS.md has what the build team confirmed. Readers are installing Tidepool for the first time.
