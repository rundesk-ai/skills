# Examples

Long, process-heavy or technical tasks rewritten from the user's side, and one split in two. Each
lists what was dropped, the way a rewrite is handed back.

## An integration check

**Before** (summarised): about 40 lines — objective, a source document with version and access
status, a meeting transcript with timestamps, two contract references, scope and out of scope,
three numbered requirements, three acceptance criteria mapped to them, start and release
dependencies, evidence required, rollout and rollback, open blockers, a readiness statement and a
validation record. Named people owned the key, the handoff and the test.

**After:**

```markdown
**Title:** Know whether the partner connection can power the quote tool

**User story**
As the team building the quote tool, we want to know the partner connection works before we build
on it, so that shoppers are not shown quotes it cannot deliver.

**Problem**
Nobody knows whether the existing partner connection can sign in and return what the quote tool
needs. Until we do, the feature cannot be finished or promised to shoppers.

**Done when**
- Login and the main API calls are tested in non-production.
- Each call's result is recorded: worked, or failed and why.

**Not included:** turning it on in production, or redesigning the quote tool.
```

**Dropped:**
- Numbered requirements and acceptance criteria — the same three points twice; **Done when** has them once.
- Document version, transcript timestamps, contract references, validation record — a link carries them.
- Rollout and readiness — nothing is rolled out.
- Waiting on the new key — a blocked-by link to the task that delivers it.
- Every person's name — the assignee field says who does it.
- "Don't touch production" and "keep the API key out of the task" — nobody competent would do either.

## An email delivery repair

**Before** (summarised): about 70 lines — objective, background on how it was split from another
task, business value, source link, scope and four out-of-scope items, three numbered requirements
and acceptance criteria, start and release dependencies, decision gates naming an approver,
evidence required, rollout and rollback, open blockers, open questions and readiness. It said three
times that a delivered test email does not prove the request was acted on.

**After:**

```markdown
**Title:** Consumers' privacy requests reach the team, not spam

**User story**
As a consumer sending a privacy or Do Not Call request, I want my email seen by the team, so that
my request is acted on.

**Problem**
Emails sent to the privacy inbox land in spam, so a consumer's request can go unseen. A missed
request is a compliance risk and a broken promise to that consumer.

**Done when**
- A test email to the privacy address lands in the inbox, not spam.
- Recipients and the manual review process are unchanged.

**Not included:** automating privacy requests, changing recipients or the mail provider, or the data-warehouse forecast (tracked separately).

**Technical notes** (for engineering)
- The likely cause is the sending domain's email authentication, and its DNS is managed in Cloudflare.
```

**Dropped:**
- The split history — linked to the related tasks instead.
- Requirements, acceptance criteria, evidence list, rollout and rollback — all said "fix the record, test it, keep proof, undo if it breaks".
- Decision gates naming an approver — **Not included** marks the line; anything past it is a new task.
- The repeated disclaimer — the goal is only about delivery, so nobody reads more into it.
- The names of the people who review and act on the inbox — "anyone reviews it" says what the reader needs.
- "Test with no real customer data" — nobody would test with it anyway.
- The record-by-record fix (SPF, DKIM, DMARC) — how it is fixed is engineering's call; where the DNS lives stays as a technical note, since engineering would otherwise look for it.

## A technical spec collapsed to outcomes

**Before** (summarised): about 80 lines specifying a shared receiver for two SMS vendors' events —
a versioned schema and dictionary, authentication, acknowledgements, retries, duplicate and
out-of-order handling, dual timestamps, governed storage, contract tests and per-vendor mapping
matrices, as four requirements with four acceptance criteria, plus gates, evidence, rollout and
readiness. Much of the event intake already existed.

**A first rewrite that missed:** it kept eight lines, one per original requirement in plainer words
— "the event format is published with a version number", "each kind of response is documented so
the provider knows whether to retry". Accurate, and still an engineering spec.

**After:**

```markdown
**Title:** Shoppers who opt out are stopped the same way, whichever vendor texts them

**User story**
As a shopper who gets texts about my quote, I want a stop or opt-out to work whichever company
sends them, so that I am not texted after I said no. As the person choosing between the vendors,
I want their results compared like for like, so that spend follows what works.

**Problem**
The two SMS vendors each describe what happens to the people they text in their own terms. Opt-outs
cannot be shown to work the same way for both, and vendor spend is decided on guesswork.

**Done when**
- Both vendors' results can be compared stage by stage, from first text to reply.
- Each result traces to its lead, the lead's source and the assigned vendor.
- Opt-outs and Do Not Call requests from either vendor are recorded the same way.
- Shoppers' personal details and message text stay out of analytics and logs.
- Each vendor's gaps — events it cannot report — are listed.

**Not included:** changing how either vendor runs campaigns, work on the vendors' side, or turning this on for live traffic.

**Technical notes** (for engineering)
- Much of the event intake already exists; the new work is the shared stages, the assignment and source on each event, and keeping personal details out.
- Each vendor still reports in its own format, so both must map into one shared set of stages.
```

**Notes, as handed back:**
- Two users share one story here, because opt-outs and comparison rest on the same shared events; split them if they ship separately.
- "Engaged" is not defined anywhere — confirm what counts before results are compared.

**Dropped:** the schema, versioning, retry, duplicate and timestamp rules, contract tests and
mapping categories — the implementation planning derives them from these outcomes, and none is a
fact engineering would otherwise miss.

## A task split in two

**Before** (summarised): one task to "define the partner outcome-file contract". It asked for an
inventory of every outcome source, a proposed import format with matching and error rules, and a
list of the product decisions still open for the product that would use the data. The product
itself was an unapproved draft.

**Why split:** the format can be drafted and checked now, while the product decisions wait on
leadership. Kept together, the task stays open until the slowest part lands, and "done" means
nothing.

**After:**

```markdown
Split in two: the format can be agreed now; the product decisions wait on leadership. Neither blocks the other.

**Title:** Partners' outcome files are matched to the right leads

**User story**
As an analyst reporting on lead outcomes, I want every partner's file read and matched the same way, so that results can be trusted.

**Problem**
Partner outcome data arrives from several sources in different formats, and nothing defines how to match it to our leads. Results reported from it cannot be trusted.

**Done when**
- Every current outcome source is listed with its owner and format.
- One proposed format covers spreadsheet outcome files.
- Records match leads on a lasting lead ID; phone number is a limited fallback.
- Every record in a bad, duplicate or conflicting file gets a clear result.
- Unrecognised columns or statuses go to a person, never accepted silently.

**Not included:** building the import.

---

**Title:** Leadership can settle the open decisions for the reporting product

**User story**
As a member of leadership, I want the reporting product's open decisions in one place, so that I can settle them.

**Problem**
The reporting product is an unapproved draft, so nobody can say who owns its data or whether to build or buy it. The work behind it cannot start.

**Done when**
- Each open decision is listed with what it blocks.
- Scope, data ownership, retention and build-versus-buy are each covered.

**Not included:** building the reporting product.
```
