+++
skill = "writing-task-tickets"
cases_version = 3
kind = "quality"
difficulty = "complex"
rubric = """
result.1  Proposes splitting the request into two tickets (privacy email delivery, Redshift cost forecast), says why in one line, and leaves the choice to the person.
result.2  Each ticket has its own Title, User story, Problem and Done when, and each Problem is at most two sentences.
result.3  Done when lines stay within what was asked; any added line is called out with a reason grounded in the request, and work beyond it (such as clearing requests already in spam) is at most suggested, not written in as a requirement.
result.4  Does not invent numbers or thresholds; an undefined bar such as what "worst case" means is marked or asked about.
result.5  Names no person and carries no implementation detail beyond what the request itself named.
conduct.1 Notes after the tickets are four or fewer one-sentence bullets, with nothing after them.
"""
+++
Write me a Jira ticket for this: QuoteHarbor privacy emails (privacy@quoteharbor.example) are landing in spam, so privacy and Do Not Call requests might sit unseen — we need to fix the email authentication in Cloudflare and prove a test email lands in the inbox. Also in the same ticket, before we finalize moving Fernway Insights to Redshift, we need a cost forecast (expected and worst-case monthly/annual, main cost drivers, recommendation).
