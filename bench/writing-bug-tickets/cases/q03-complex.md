+++
skill = "writing-bug-tickets"
kind = "quality"
difficulty = "complex"
rubric = """
result.1  Proposes two tickets (promo codes rejected; pay button cannot be tapped), says why in one line, and leaves the choice to the person.
result.2  Each ticket has its own steps, expected and actual results, and pass-or-fail fix condition.
result.3  Unknowns the report does not give (which codes, which phones, how often) are marked or asked about, not invented.
result.4  Proposes no fix (no CSS or validation change written as a requirement).
conduct.1 Notes after the tickets are four or fewer one-sentence bullets, with nothing after them.
"""
+++
Make a GitHub-style bug report for this, the repo has no issue template: checkout is broken on mobile — the promo code field rejects codes that work on desktop, and the pay button overlaps the footer so you can't tap it. Saw it on my phone this morning.
