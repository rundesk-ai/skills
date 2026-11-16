+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "complex"
fixture = "billing-memo"
cases_version = 1
key = """
must:
  M1 point  The brief asks for a recommendation; the memo ends "Both paths are reasonable... depends on how the organization weighs those." It makes none. This must be the first or top-ranked finding.
  M2 claim  "our platform team has moved two services this way before" has no source in the brief.
  M3 claim  "the analytics team could add query limits in the meantime" has no source in the brief, and it is the memo's main argument for waiting.
  M4 chain  The memo never compares the 3 engineer-weeks with the team's remaining capacity (6 of 12 weeks committed), so the deciding comparison is left to the reader.
decoys:
  D1 Stating a recommendation as if the author made it, or rewriting the memo's conclusion as fact (a labelled proposal, or asking the author which way they lean, is fine).
  D2 Flagging the verified facts as wrong: 14 services, 38 and 52 minutes, 3 engineer-weeks, 900 USD a month, 4 engineers, finance re-sending invoices.
  D3 Calling the memo's prose sloppy or AI-written as a finding.
taste:
  T1 the title; T2 paragraph count; T3 "October changed that."
extras:
  X1 "saturated the cluster" and the history ("made sense when billing was small", "caused no trouble") have no source.
  X2 "the first time... the second" asserts an order the brief does not give.
  X3 the cost of waiting (another outage, finance's manual re-sends) is not set against the cost of moving.
  X4 the memo ends without the ask or decision the VP must make.
"""
+++
Review memo.md before it goes to the VP of Engineering. It answers the request in brief.md, which also lists the facts the author gathered.
