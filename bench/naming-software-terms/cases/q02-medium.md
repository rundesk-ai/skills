+++
skill = "naming-software-terms"
cases_version = 1
kind = "quality"
difficulty = "medium"
fixture = "helpdesk"
rubric = """
result.1  Recognizes one concept with four names (`cust` table, `Client`/`client_id` in code, `customer` in the API, "Account" on screen) and settles on one canonical term, giving the reason (for example the published API already says `customer`).
result.2  Keeps every published API field name unchanged (`customer`, `state`, `opened`, `do_not_email`), or proposes a staged, versioned change instead of renaming it in place.
result.3  Does not silently rename database tables or columns (`cust`, `cust_id`, `flg_2`): either leaves them with a documented mapping or proposes a migration for the owner to approve.
result.4  Internal code and the page use the canonical term and one verb per operation (not `get_`/`fetch_`/`retrieve_` for the same act); the page title, column headers and empty state are short factual labels ("Tickets", "Customer", "Subject", "Status", "No tickets."). Tests pass.
result.5  Creates no glossary, term registry or vocabulary file.
conduct.1 Reads every layer (schema, models, store, API, template) before renaming anything.
conduct.2 Separates what it changed from what needs an owner decision, in a short report.
"""
+++
Support says the tickets page is confusing, and the names in the code don't match each other either.
Clean up the naming around the tickets list.
