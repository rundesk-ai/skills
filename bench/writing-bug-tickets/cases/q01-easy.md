+++
skill = "writing-bug-tickets"
kind = "quality"
difficulty = "easy"
rubric = """
result.1  Steps to reproduce start from a known state and could be followed by someone who was not there (device and browser, the actions in order).
result.2  States expected and actual results separately and observably.
result.3  Records what was tested: fails on the iPhone, works on desktop Chrome, and marks what is unknown (iOS version, Android) instead of inventing it.
result.4  The suspected cause (the history change) is not stated as fact in the problem or requirements; at most it is labelled as suspected.
result.5  The request to save progress for another day is not written into the bug as a requirement; at most it is noted as separate.
conduct.1 Names no person and invents no number, version or frequency.
"""
+++
Turn this into a Jira bug ticket:

customers keep saying the quote form wipes their answers?? I tried on my iphone and yeah hitting back clears everything. desktop chrome seems fine. probably the history API thing we changed last sprint. can we also save their progress so they can come back tomorrow
