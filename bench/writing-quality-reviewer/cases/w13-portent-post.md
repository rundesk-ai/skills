+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "launch-post"
cases_version = 3
key = """
must:
  M1 portent    The opening ("Something has shifted in how teams keep up with change. This changes everything.") and the close ("Nothing about release notes will ever be the same.") are vague, weighty lines that tell the reader nothing; reported as one pattern with both places.
  M2 dead-ends  "creates a real sense of momentum" and "gives the whole experience room to breathe" sound meaningful and say nothing the reader can use; the fix names what the reader gets (a page per release with a permanent link; filtering by area).
  M3 point      The real point (each release now has its own linkable page, filterable, with RSS, free) is buried under the opener; the result should come first.
decoys (not findings):
  D1 "It's free on every plan." as a short line: a real verdict placed for emphasis.
  D2 "And if you live in a feed reader" opening with And.
  D3 Claims that match changelog.md (permanent link, filter areas, RSS, free).
taste:
  T1 the title wording.
extras:
  X1 a fix that adds a feature, number or benefit not in the changelog.
  X2 a fix that adds its own fragment, one-line paragraph or vague line (for example a new punchy one-liner close).
"""
+++
Review post.md before we publish it on the product blog. changelog.md is what actually shipped.
