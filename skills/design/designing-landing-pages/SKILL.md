---
name: designing-landing-pages
description: Use when designing, building, reviewing, or improving a campaign landing page or focused conversion path — a new page, a redesign, or a live page whose conversion rate, form or purchase completion, ad-to-page message match, lead or order quality, instrumentation, or A/B tests need work. It supplies the conversion contract and metric ledger, message map, page and flow design, measurement and experiment design, rendered verification, and an evidence-ranked backlog. Do not use for a multi-product storefront or checkout, general application UI, ad creative alone, SEO-only work, analysing a completed experiment's results, or legal approval of consent language.
---

# Design landing pages

Treat the page and its acquisition path as one system. Optimize qualified value rather than clicks,
form submissions, or purchases in isolation: a higher raw conversion rate can be a loss when it
produces misdirected, unreachable, noncompliant, refunded, or low-value outcomes.

## Establish the conversion contract

Before drawing a section, writing a headline, or recommending a change:

1. Identify the traffic source, campaign, query or promise, audience, awareness level, device mix,
   geography, and returning-versus-new split. Do not design one generic page for materially
   different intents.
2. Define the offer in the visitor's terms: outcome, audience, eligibility, cost or commitment,
   differentiator, evidence, risk, and what happens after the action.
3. Choose one primary conversion — accepted order, call, form, booking, quote start, or another
   durable outcome. Give secondary actions lower emphasis and a reason to exist.
4. Define the downstream success event and its owner: paid and retained order, margin, accepted or
   qualified lead, reached lead, appointment, sale, or value. Record the rejection,
   disqualification, cancellation, refund, and fraud reasons that can reverse apparent success.
5. List the claims, logos, ratings, testimonials, certifications, prices, availability, guarantees,
   and urgency that can actually be substantiated. Remove invented proof and unsupported urgency.
6. Record the legal, privacy, consent, accessibility, brand, analytics, and performance constraints.
   Route U.S. lead-transfer and contact-consent gates to the compliance owner: this skill identifies
   where approval is needed, and does not write or approve consent language or create permission to
   call or text.

Map the complete funnel before calling any rate good, bad, or page-caused, and keep metric names
distinct:

```text
ad CTR               = ad clicks / ad impressions
landing arrival rate = eligible landing sessions / ad clicks
page CTA rate        = unique primary-action activators / eligible landing sessions
accepted page CVR    = accepted primary conversions / eligible landing sessions
qualified page CVR   = qualified leads / eligible landing sessions
closed page CVR      = closed jobs or retained orders / eligible landing sessions
value per session    = net attributable value / eligible landing sessions
```

The page does not own ad CTR; improve it through the ad and targeting, then keep the page promise
consistent with them. A provider's reported conversion rate may divide attributed conversions by ad
interactions, and an analytics property may report the share of sessions or users with a key event.
Do not compare or multiply rates until their population, action, scope, window, and deduplication
align. CTA rate is a local diagnostic, not page CVR, unless activating the CTA is itself the accepted
outcome. Read [measurement and experimentation](references/measurement-and-experimentation.md)
whenever a request uses `CTR`, `CVR`, `conversion`, `key event`, or an unlabeled rate.

## Diagnose before proposing

Separate observations from explanations and recommendations:

```text
Observation: what the page, funnel, research, or data shows
Evidence: source, population, period, denominator, and material limitation
Interpretation: the user problem or mechanism the evidence suggests
Confidence: established, likely, plausible, or unknown
Recommendation: the smallest change or test that could improve the outcome
Proof: what result would support or reject the interpretation
```

Use campaign and search terms, customer interviews, usability observations, sales objections,
support questions, CRM loss reasons, funnel data, field performance, and accepted outcomes. Do not
replace evidence with demographic stereotypes, universal benchmarks, or landing-page folklore.

Distinguish `observed absent` from `not supplied`. A screenshot, page description, or analytics
summary proves only the state it covers; missing evidence stays unknown until the rendered page,
flow, or source is inspected.

Fix known defects — broken message match, inaccessible controls, failed validation, slow field
performance, incorrect measurement — and verify them directly; they do not need an experiment to
prove the page is broken. Treat message match as broken when a material acquisition promise is
absent, contradicted, or silently changed at arrival: product, audience, price, eligibility, timing,
obligation, or next step. Alternative truthful framing of the same complete offer is a persuasion
hypothesis, not a defect.

## Plan the page around visitor decisions

For each materially different intent, write a message map:

```text
Visitor wants:
Arrival promise:
Specific outcome:
Why believe it:
Main objection or risk:
Eligibility or limitation:
Primary action:
What happens next:
```

Make the page's identity, relevance, offer, and next step recognizable early, and let intent, risk,
content, accessibility, and the real viewport decide how much belongs in the first view. Order the
rest as answers to the visitor's questions, not a required stack of marketing sections. A useful
starting hypothesis is outcome and proof, how it works, eligibility or fit, objections and risk,
then the same primary action. Repeating that action after relevant answers is coherent; adding
unrelated actions is not.

Use one visually dominant action in each decision region and label its truthful next step, such as
`See my quote options` or `Book a 20-minute demo`, not `Submit` or a result the next screen cannot
deliver. Keep its meaning consistent through activation, pending, acceptance, and confirmation.

For a product page, preserve the advertised product, variant, price, terms, availability, and actual
purchase path. For a lead page, justify every field by the fulfillment, qualification, routing,
contact, or compliance decision it serves. Make loading, errors, duplicate protection, backend
acceptance, and confirmation part of the flow; a click or thank-you URL is not conversion truth.
Where a payment, booking, or CRM system owns acceptance, that system's state is the truth.

Read [page architecture and conversion flows](references/page-architecture-and-conversion-flows.md)
when planning the hero, above-the-fold review, layout, value proposition, proof, CTA meaning, form
or purchase flow, and confirmation states.

## Build the mobile page as the primary task

Preserve the promise, proof, action, disclosures, recovery, and accepted outcome across sizes. Design
the narrow flow first, then recompose from content pressure. Treat accessibility, field performance,
third-party cost, keyboard coverage, and error recovery as conversion behavior, not polish.

Read [mobile, performance, and accessibility](references/mobile-performance-and-accessibility.md)
when designing or reviewing responsive layout, sticky actions, mobile forms, media, analytics tags,
Core Web Vitals, accessibility, or recovery, and when classifying an experience finding as a defect
or a hypothesis.

## Instrument the whole outcome, then experiment

Write the event, identity, denominator, attribution, deduplication, and reconciliation contract
before launch. Separate page diagnostics from backend-accepted conversion, downstream quality or
value, and harm guardrails. Keep ordinary analytics free of PII and payment data.

Fix known message, function, accessibility, performance, and measurement defects before testing
persuasion. Recommend an experiment only when it can decide between credible alternatives: state the
causal hypothesis, population, assignment, primary metric, quality or value outcome, guardrails,
minimum useful effect, sample and duration method, and stopping rule. Validate sample ratio and
telemetry before interpreting lift, and report absolute results with uncertainty rather than a
winner label. When traffic cannot power a useful decision, use qualitative diagnosis and an annotated
baseline without claiming randomized causality.

## Rank and deliver

Return findings in this order, ranking each by expected downstream value, confidence, effort, risk,
dependency, and time to learn. Do not fabricate a lift estimate or use a generic benchmark as one.

1. **Known failures** that prevent the intended experience or invalidate measurement.
2. **High-confidence mismatches** supported by more than one evidence surface.
3. **Testable hypotheses** with a named mechanism and decision rule.
4. **Unknowns** whose missing evidence could change the plan.

For a bounded question, return only the decision, evidence and limits, metric ledger when relevant,
and ranked next steps. For a new page, redesign, or optimization program, deliver the smallest set of
these that makes the decision and handoffs unambiguous, linking repeated findings by identifier:

1. a conversion brief: segments, offer, primary and downstream outcomes, baseline, constraints, and
   unresolved evidence;
2. an above-the-fold review and a table of what appears to work and not work, with evidence and
   confidence;
3. a message map and claim/proof ledger;
4. a page and flow specification naming each region's purpose, content, hierarchy, action, responsive
   behavior, and states, including fields or product selection, errors, duplicate protection,
   acceptance, and confirmation;
5. an analytics contract with event owners, numerators, denominators, deduplication, attribution,
   quality and value feedback, and reconciliation proof;
6. a prioritized correction and experiment backlog, with a test brief for each experiment; and
7. a rendered verification report, or the handoff naming the content, development, analytics,
   compliance, and verification owners who must return it.

Use approved messaging, claims, brand direction, and design-system constraints for visual hierarchy
and interface wording. When the baseline, traffic volume, proof, product terms, qualified outcome,
brand direction, or approved legal content is missing, mark it; do not invent a target lift, claim,
review, price, or consent copy to make the package look complete. Do not launch an experiment,
change analytics configuration, or approve legal language without that authority.

## Prove the delivered page

Before calling a built page ready:

1. Compare the rendered first viewport with every acquisition promise and intended segment.
2. Complete the flow on representative mobile and desktop browsers using touch, keyboard, zoom,
   autofill, slow network, long content, validation errors, duplicate activation, and back/restore.
3. Verify headings, labels, focus order and visibility, contrast, reflow, touch targets, error
   announcements, reduced motion, and a representative screen-reader path.
4. Measure field Core Web Vitals and inspect layout shifts and third-party main-thread and network
   cost.
5. Trace each event from browser to analytics to the owning order, payment, booking, call, or CRM
   system; prove deduplication, attribution, accepted-versus-rejected status, and the absence of
   prohibited PII or payment data.
6. Verify every claim, proof point, price, availability, privacy, consent, and next-step statement
   against its owner and effective version.
7. Record the page and campaign version, test conditions, known limits, baseline metrics, and next
   hypothesis. Do not report a generic `conversion optimized` verdict without this evidence.

## Reject common folklore

| Folklore | Better decision |
|---|---|
| Put every CTA, form, or buy control above the fold | Make the offer and next action recognizable early; place completion where the visitor has enough confidence to act. |
| Remove every navigation link | Remove irrelevant exits; keep necessary trust, contact, legal, accessibility, and recovery paths. |
| Fewer fields always convert better | Ask only what is needed now, keeping fields that materially qualify, fulfill, route, or make consent valid. Measure qualified value. |
| Multi-step forms always win | Use steps for real cognitive or conditional structure, then evaluate the complete flow and downstream quality. |
| Social proof always increases trust | Use current, attributable, representative evidence with required disclosures; fake or context-free proof destroys trust and can be unlawful. |
| A universal CVR benchmark defines quality | Compare like-for-like intent, channel, device, offer, and value; prefer the page's own baseline. |
| A statistically significant CTA click is a win | Require trustworthy assignment and no unacceptable regression in accepted outcomes, value, errors, speed, accessibility, refunds, or complaints. |

Read [sources](references/sources.md) when auditing or updating the evidence behind these rules.
