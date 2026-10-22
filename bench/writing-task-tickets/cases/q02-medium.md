+++
skill = "writing-task-tickets"
cases_version = 2
kind = "quality"
difficulty = "medium"
rubric = """
result.1  Done when is a short list (six lines or fewer) of outcomes a stakeholder would recognise — comparing the vendors, tracing results to lead, source and vendor, opt-outs handled the same way, personal data kept out of analytics.
result.2  No Done when line restates a technical guarantee: schema or format versions, retries, idempotency, duplicates, ordering, timestamps, response codes, contract tests or mapping categories.
result.3  Problem is at most two sentences and states the business cost (vendor spend decided blind, or opt-out compliance unprovable).
result.4  Names no person; drops the source-document, dependency, gate, evidence, rollout and readiness sections.
result.5  Not included keeps the original's real out-of-scope items and adds no scope decision of its own.
conduct.1 Notes after the ticket are four or fewer one-sentence bullets, with nothing after them.
"""
+++
Rewrite this ticket for the stakeholders who need to understand what we're doing and why. Engineering and agents will plan the implementation from it.

Normalize TextPilot and SendRiver SMS lifecycle events

Objective: Help Fernway understand how each person's SMS journey performs and enforce the right stop conditions, regardless of whether TextPilot or SendRiver sends the messages. A shared lifecycle-event receiver gives both vendor paths one trustworthy measurement and control boundary.

Canonical context: PRD QuoteHarbor Short-Form Funnel Phase 1, Version 18, access verified, reviewed 2026-09-30. TextPilot and SendRiver retain separate campaign implementations; both map their lifecycle events into this Fernway-owned contract so comparison, suppression and Long Form outcomes use consistent facts.

Scope: the assigned provider reports enrollment, delivery, engagement, reply, opt-out or DNC, stop and error events into one normalized receiver, connected to the vendor assignment, allocation version, source and lead, without exposing message bodies or personal details in general analytics. In scope: versioned schema and dictionary, authenticated receiver, acknowledgements and errors, stable event identity, dual timestamps, idempotent retry, out-of-order handling, approved storage, synthetic examples, contract tests. Out of scope: making TextPilot and SendRiver use the same API or campaign logic, provider-side build work, production credentials, live outreach, consumer return links, Long Form implementation, automatic vendor failover, production enablement.

Requirements. R1: normalize lifecycle categories for both vendors preserving provider, cohort, allocation version, source, campaign, message identity, lead identity, event time, receive time and schema version (owner: Sam). R2: define authenticated requests, acknowledgements, validation errors, retries, idempotency and ordering so duplicates create one logical event and late events do not overwrite history (owner: Sam). R3: store accepted events in the governed path and expose only approved non-PII health to PostHog and logs (owner: Sam). R4: provide one mapping and contract-test kit each vendor can use to classify fields as available, configuration needed, build needed or unsupported (owner: Sam).

Acceptance criteria. AC1: synthetic TextPilot and SendRiver examples validate categories, assignment, allocation version, lineage, IDs, timestamps and schema version. AC2: automated tests prove auth failure, invalid schema, lost acknowledgement, retry, duplicate and out-of-order delivery produce documented responses and one stored event per ID. AC3: events are queryable with source and vendor lineage; message bodies and personal details are absent from PostHog, logs and replay. AC4: each vendor owner completes a mapping matrix against the same contract.

Dependencies: FW-355, FW-356, FW-357, FW-342, FW-335. Dana approves campaign settings. Morgan gives the production go/no-go.
Evidence required: schema, dictionary, endpoint docs, decisions, fixtures, contract-test results, non-PII evidence, mapping matrices.
Rollout: receiver disabled for live traffic while proven with synthetic data.
Readiness: engineering-ready for Sam; does not authorize release.
