+++
skill = "writing-bug-tickets"
kind = "quality"
difficulty = "medium"
rubric = """
result.1  Reports only what was observed: the pattern (failures cluster on files over about 10 MB, on the office network) is recorded, and nothing says the cause is known.
result.2  Gives how often it happens (roughly 3 of 10 attempts) and where it does and does not happen, rather than calling it random.
result.3  Quotes the exact error text instead of paraphrasing it.
result.4  The fix condition is pass-or-fail and observable (for example the upload completes for the cases that failed), not "improve reliability" or an implementation step.
result.5  Does not paste the whole log or include the customer's email address.
conduct.1 Names no person (Priya, Dan) in the ticket.
"""
+++
Write up a Linear bug for this. Priya from support forwarded it, Dan tested it.

Customer (jane.d@example.com) says document upload "just fails sometimes". Dan's testing: on the office network, uploads of PDFs over about 10 MB fail roughly 3 times out of 10; under 10 MB never failed in 20 tries; on his home connection the same 14 MB file worked 10 of 10. When it fails the page shows "Upload failed (413). Please try again." Server log has a long stack trace, here's the first line: `RequestEntityTooLarge: body exceeded limit` followed by 200 more lines. Dan thinks it's the proxy, Priya thinks it's the browser.
