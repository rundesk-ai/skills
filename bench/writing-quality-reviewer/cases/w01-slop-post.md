+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "trunk-post"
cases_version = 1
key = """
must:
  M1 coherence  The post has no argued point: paragraphs 3-8 are parallel benefit claims that could be reordered or removed without loss, and the conclusion ("offers a compelling path forward") is asserted, not earned. Must be reported as a structural finding, and ranked above the sentence-level findings.
  M2 abstractions  Abstract nouns act in nearly every sentence ("The adoption of short-lived branches enables...", "Integration friction decreases", "Smaller changes facilitate..."); no person or concrete thing acts. Reported as one pattern across the post.
  M3 promise  The opening highway analogy is never used again; the opening promise is not paid off.
  M4 claims  "73% of elite-performing teams" and "a 40% reduction in lead time" are attributed only to "industry data"; no source is given or available. Must be flagged as unsourced, not accepted.
  M5 cadence  Every body paragraph has the same shape and sentence length; no sentence lands a verdict.
decoys (flagging is a false positive):
  D1 Calling the post AI-written or machine-generated as a finding (judge the writing, not its origin).
  D2 Inventing the author's point or replacement facts and presenting them as the author's (a clearly labelled proposal, or a question to the author, is fine).
taste (neither):
  T1 title case in the title; T2 post length; T3 the word "mainline".
extras (real, unplanted):
  X1 the post never says what "short-lived" means or when the model does not fit.
  X2 stock wrap-up "In conclusion" and the triad "faster delivery, higher quality, and stronger collaboration".
  X3 feature flags presented with no cost.
"""
+++
Review trunk-based.md before we publish it on the company engineering blog. Readers are engineers and engineering managers deciding whether to change their branching model.
