+++
subject = "writing-quality-reviewer"
kind = "quality"
difficulty = "medium"
fixture = "stiff-help"
cases_version = 2
key = """
must:
  M1 opening  The page opens by defining the system ("Boardly provides board sharing functionality") instead of the reader's moment (they want a client or teammate to see a board without inviting them to the workspace) and what they'll be able to do. Reported as a coherence or reader's-side finding.
  M2 monotone  The first paragraph is eight short sentences of one shape, most with the system or "links" as subject and no so, because or then between them. Reported as a cadence and cohesion failure, with a fix that joins the facts and lets "you" lead.
  M3 register  Formal or stiff phrasing where the voice guide asks for a person: "provides ... functionality", "is configurable", "is not required in order to utilize". Reported, with plain replacements.
  M4 detail  Facts in NOTES.md that the page drops or blurs: links expire after 30 days (the page says only "Links expire") and a new one can be made any time; deleting a link removes access right away; editors need an account and are asked to sign in (the page implies no account is needed at all).
decoys (a false positive):
  D1 Any proposed fix that adds hype ("seamless", "effortless", "in seconds") or an exclamation mark.
  D2 Any fix that invents a fact NOTES.md does not give (a share limit, a password option, an expiry setting).
  D3 Any fix that drops one of the facts on the page or in the notes.
  D4 Rewriting the numbered steps, which are clear, into prose.
taste (neither):
  T1 the heading wording; T2 bold on control names.
"""
+++
Review sharing.md before it goes in our help center. NOTES.md is what the product team gave the writer, including our voice guide.
