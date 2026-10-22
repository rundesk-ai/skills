+++
skill = "writing-task-tickets"
cases_version = 2
kind = "quality"
difficulty = "easy"
rubric = """
result.1  Uses only Title, Problem, Goal, Done when and an optional Not included; no requirement IDs, acceptance-criteria mapping, evidence, rollout, gates or readiness sections.
result.2  Names no person anywhere in the ticket.
result.3  Problem is at most two sentences and states what the spam problem costs or risks.
result.4  Every Done when line is an outcome someone could check pass or fail (for example a test email lands in the inbox), with no vague bar such as "reliably" or "properly".
result.5  Adds no common-sense lines (no real customer data, no credentials in the ticket, don't touch production) and no requirement the original did not ask for.
conduct.1 Notes after the ticket are four or fewer one-sentence bullets, with nothing after them, and no file paths or code.
"""
+++
Rewrite this ticket so the people who need to know can read it in a minute. Engineering plans the work from it later.

Authenticate QuoteHarbor privacy email delivery

Objective: A QuoteHarbor consumer's privacy email reaches Fernway's existing manual review path outside spam. This reduces the risk that a valid privacy or DNC request is delayed before Dana can review and route it.

Background: FW-387 previously combined this email-delivery repair with a Redshift forecast. Morgan separated those topics on October 21. FW-383 confirms that privacy@quoteharbor.example is manually reviewed by Dana and forwarded to Priya when action is required.

Scope. In scope: identify the sending or forwarding domain and mail service; diagnose the authentication or alignment failure causing delivery to spam; correct only the required Cloudflare-managed SPF, DKIM or DMARC records; send a synthetic privacy email through the existing route and retain sanitized delivery headers. Out of scope: Redshift; changing recipients, the mail provider, or Dana and Priya's responsibilities; privacy-email automation; testing with real consumer information.

Requirements. R1: Sam records the active privacy-email path, domain, mail service and pre-fix failure before changing DNS. R2: Sam changes only the required Cloudflare records and records before/after SPF, DKIM, DMARC and alignment results. R3: Sam proves the existing route with synthetic data while leaving recipients and manual handling unchanged.

Acceptance criteria. AC1 → R1: evidence identifies the domain, provider, timestamp and pre-fix result. AC2 → R2: sanitized post-fix headers show SPF, DKIM and DMARC passing with alignment. AC3 → R3: a synthetic message reaches the expected inbox outside spam, routing and recipients are unchanged, and no real consumer data was used.

Decision gates: stop for Morgan before changing the mail provider, recipients or workflow. Stop before using real consumer information.
Evidence required: sanitized pre/post results, the exact records changed, proof of inbox delivery.
Rollout and rollback: apply the smallest change, wait for DNS, run the test; restore prior values if delivery regresses.
Readiness: engineering-ready for Sam. Completion proves delivery only; it does not authorize automation.
