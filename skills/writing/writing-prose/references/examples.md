# Examples

Each example shows a draft, a rewrite, and what changed. The figures in the rewrites are
illustrative; in real work they come from your context or you ask for them.

## An argument: pay down the debt first

The task: argue that a team should pay down technical debt before building features.

**Draft** (cohesive, incoherent):

> Technical debt represents a significant challenge for modern engineering organizations.
> Accumulated shortcuts create friction across the development lifecycle. Velocity suffers as
> complexity compounds. Meanwhile, customer expectations continue to evolve, and competitive
> pressure demands rapid iteration. Investing in code quality unlocks long-term scalability.
> Ultimately, prioritizing technical debt is not just a technical decision, but a strategic one.

**Rewrite:**

> Last quarter, our engineers spent three of every ten days working around the old campaign builder
> instead of improving it. Each new feature took longer because someone first had to trace which of
> four duplicate send functions was actually live. If we spend the next sprint collapsing those into
> one, every feature after that gets cheaper, including the two our biggest customer is asking for.
> So the debt work isn't a delay on their requests.
>
> It's the fastest route to them.

| | Draft | Rewrite |
|---|---|---|
| Subjects | Abstractions: debt, shortcuts, velocity, investing | Actors: engineers, someone, we |
| Structure | Five parallel claims, conclusion asserted | A chain: time lost, why, the fix, the payoff |
| Specifics | None; nothing can be checked | Numbers a reader could verify |
| Cadence | One medium rhythm, closed with "not just X, but Y" | A long build, then one short line where the point lands |
| Objection | Ignored | "Debt delays the customer" becomes the conclusion |

## Reference: a setup section

**Draft:**

> Environment configuration is an important aspect of getting the project running. Various
> settings can be adjusted to accommodate different workflows. It is worth noting that the database
> connection must be configured prior to running migrations, and that the test suite relies on a
> separate database.

**Rewrite:**

> Copy `.env.example` to `.env` and set `DATABASE_URL` to your local database. Run `make migrate`;
> it fails with "connection refused" until the database is running.
>
> The tests use their own database, set by `TEST_DATABASE_URL`, so running them never touches your
> local data.

What changed: the reader is the actor and the first sentence is the first thing they do. Exact
names replace "various settings". The likely failure is named with the error they will see. "It is
worth noting" and "an important aspect" are gone; no stance was needed, only the default.

## Short form: release notes

**Draft:**

> - Enhanced export functionality to provide greater flexibility.
> - Various performance improvements and bug fixes.
> - Improved the user experience of the settings page.

**Rewrite:**

> - You can now export invoices as CSV from the Invoices page.
> - Search results load in about a second on accounts with 10,000+ contacts, down from five.
> - Fixed: saving Settings no longer signs you out on Safari.

What changed: each line is one change, with the reader as the actor and what they can now do or
no longer suffer. "Various improvements" is either named or cut. The numbers come from the release
being described; with none to hand, the line says what changed without a figure.

## Short form: a status email

**Draft:**

> Hi all, I wanted to give a quick update on where things stand with the migration. The team has
> been making great progress across multiple workstreams. There have been some challenges with the
> data validation piece, but overall things are moving in the right direction. Ultimately, we remain
> committed to delivering a high-quality outcome.

**Rewrite:**

> The migration will finish on 4 December, a week later than planned.
>
> 38 of 41 tables are moved. The other three hold invoice history, and 2% of their rows fail
> validation because of currency codes that predate 2019. We are mapping those codes by hand this
> week.
>
> I need one decision by Friday: do we migrate the 2% as-is and flag them, or hold the cutover until
> they are clean? I'd flag them; finance has confirmed nobody reports on those rows.

What changed: the news comes first, and the ask gets its own short paragraph. "Some challenges"
became the actual problem and its size. "Great progress" became a count. The writer takes a
position on the decision rather than listing options.

## Perspective: reporting finished work

The task: tell the person who asked what was done about slow invoice exports.

**Draft** (the writer's side):

> I started by investigating the export functionality. After reviewing the codebase, I identified
> that the `build_rows` helper was performing an N+1 query against `billing_documents`. I then
> implemented a solution leveraging `prefetch_related`, which should significantly enhance
> performance. Additionally, I made various other improvements. Overall, the export process is now
> more robust and efficient.

**Rewrite** (the reader's side):

> Invoice exports for your largest account now finish in 40 seconds instead of 9 minutes.
>
> The export was loading each invoice's line items with a separate database query, about 12,000
> of them for that account. It now loads them in one. I also fixed the CSV header, which said
> "Amount (USD)" for accounts billed in euros.
>
> I didn't change exports under 1,000 invoices; they were already under five seconds.

What changed: the result the reader cares about comes first, in their word ("invoice exports", not
"the export functionality" or `billing_documents`). The process shrinks to the one cause they need
to trust the fix, with the identifier dropped because this reader doesn't need it. "Various other
improvements" became the one other change, named. "Should significantly enhance" became the
measured numbers; with none measured, the rewrite would say so rather than promise. The last line
answers the question the reader would ask next.

## Voice: stiff copy made to sound like a person

Each pair keeps every fact. What changes is who leads, how the facts lean on each other, and the
rhythm: the three C's, which together are what makes copy sound like a person.

**A product page paragraph.** Stiff:

> Ledgerly sends invoices automatically. Ledgerly sends a reminder three days before the due date.
> It sends a second reminder when the invoice is overdue. It records each payment. The dashboard
> displays outstanding invoices.

Like a person:

> Send an invoice once and Ledgerly does the chasing for you. Your client gets a reminder three days
> before it's due and another if it slips past, so you're not writing awkward follow-up emails. When
> they pay, the payment is recorded on its own, and your dashboard shows only what's still
> outstanding.

What changed: "you" leads, and what the reader gets (no chasing) comes before the mechanism.
Five sentences opening on Ledgerly or It became three of different shapes, joined by so and when.
Software keeps software verbs (sends, records, shows); "does the chasing for you" is the plain
event, not a mind.

**A docs paragraph.** Stiff:

> The `deploy` command uploads the build. The upload is resumable. A failed upload restarts from
> the last completed chunk. The command prints a URL on success. The URL is valid for seven days.

Like a person:

> Run `deploy` and it uploads your build in chunks, so if your connection drops halfway you can run
> it again and it picks up from the last chunk that made it. When it's done, you'll get a preview
> URL that works for seven days.

What changed: the reader is the actor, the dropped connection is their moment rather than "a
failed upload", and each fact hangs off the one before it (so, when) instead of starting cold.

**A natural sentence to leave alone.** Original:

> Your drafts save as you type, so closing the tab by accident costs you nothing.

A stiffening edit:

> Drafts are saved automatically. Closing the tab does not result in data loss.

What went wrong: the original passed every check, and the edit made it worse on two C's. The so that
linked cause to benefit is gone (cohesion), two flat declaratives replace one sentence that moved
(cadence), "as you type" lost its detail to "automatically", and "costs you nothing" became the
formal "does not result in data loss". The right edit was none.

**A real one, from GOV.UK's "Register to vote" page:**

> You normally only need to register once - not for every election. You'll need to register again if
> you've changed your name, address or nationality. It usually takes about 5 minutes.

What it does: it answers the questions a person arrives with (do I have to do this again? how long
will it take?) in the order they'd ask them, with "you" leading and contractions throughout. Its
hedges ("normally", "usually") stay because the doubt is real, and "about 5 minutes" is the
specific. Plain, warm and exact are one register here, not three.

Contains public sector information licensed under the Open Government Licence v3.0.
