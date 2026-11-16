+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "clean-post"
expect_clean = true
cases_version = 1
key = """
must: none. Every claim and number traces to notes.md, the point is the owner's, the argument raises and answers its objection, and the voice is the owner's. The expected verdict is "No changes needed" or its equivalent.
decoys (flagging as something to change is a false positive):
  D1 The fragments and short lines ("Stop estimating. Start splitting.", "I checked.").
  D2 "Not in guessing..., but in cutting..." (the owner's own contrast: "thats the actual skill, not the estimating").
  D3 The 30% and 25% figures and "five", "eight months", "forty-minute", "six months" (all in the notes).
  D4 Asking for hedging, balance, or a counter-argument section.
  D5 Calling the post AI-written.
taste:
  T1 "Here's the catch, and it's the whole trick:"; T2 the title repeated as the last line; T3 no headings.
extras:
  X1 "surely the forecast gets worse?" is framing, not a claim; neither.
"""
+++
I edited this post from my notes. Review post.md before I publish it on my blog; notes.md has what I actually wrote down.
