+++
skill = "naming-software-terms"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "helpdesk"
rubric = """
result.1  The dialog names the record and the action with the canonical term (for example title "Delete customer?", button "Delete customer"), not "Account", "client", "OK" or "Yes".
result.2  It does not invent facts the code does not establish: what happens to the customer's tickets, whether deletion can be undone, or who can restore it. It either leaves them out or states them as questions for the owner.
result.3  It asks the owner for the facts that decide the copy (what happens to existing tickets, whether it is reversible), in a few lines.
result.4  No reassuring filler, hedging or minimizers ("Are you sure?", "simply", "it looks like", "Oops").
conduct.1 Reads the code to learn what deleting a customer would touch before writing copy.
"""
+++
Write the confirmation dialog for deleting a customer. Keep it short.
