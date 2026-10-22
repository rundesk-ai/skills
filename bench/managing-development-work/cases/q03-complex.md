+++
skill = "managing-development-work"
cases_version = 2
kind = "quality"
difficulty = "complex"
fixture = "invoicer"
rubric = """
result.1  Recognizes the request as several separate outcomes (wrong numbers, Excel export, weekly email) rather than one "redesign", and scopes each on its own.
result.2  Puts the wrong-numbers problem first as a correctness risk, and finds its likely cause in the code: voided invoices are counted by `monthly_totals`. Evidence comes from reading the code, not a guess.
result.3  Breaks the work into vertical slices, each with an observable proof; details only the first few and leaves later work as named outcomes.
result.4  Keeps nice-to-haves separate (for example, xlsx formatting beyond a CSV that opens in Excel), and asks the owner only questions that change scope or authority (a dependency for real .xlsx, email infrastructure, what "slow" means).
result.5  Writes no code.
conduct.1 Reads the repository before proposing structure.
conduct.2 Slices by outcome, not by layer ("data layer, then API, then UI").
conduct.3 Orders by risk and dependency, and says why.
"""
+++
Reporting needs a redesign. Finance says the monthly numbers are sometimes wrong, sales wants to
export reports to Excel, and support wants a weekly summary emailed to them. Figure out how we should
tackle this. Don't write any code yet.
