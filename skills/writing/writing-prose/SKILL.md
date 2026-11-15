---
name: writing-prose
description: Use when writing, rewriting or reviewing prose a person will read — a doc, README, guide, PRD, proposal, report, summary, email, announcement, release notes, a pull request or issue description, a status update, or any reply longer than a few lines — and when a draft reads as generic, padded, listy or machine-written. It supplies the order of work for a piece that builds to one point, sentences with real actors, varied cadence and real specifics, with checks to run before and after drafting. Do not use for code, code comments, or names and labels inside an interface.
---

# Writing prose

People who read model-written prose feel their time was wasted even when they cannot say why. The
cause is usually the same: the sentences link to each other well (**cohesion**), but the piece does
not build to a point (**coherence**), and every sentence has the same rhythm (**cadence**). The
fixes come in that order of importance: **coherence, then cadence, then cohesion.** A reader
forgives a clumsy sentence around a clear point; polished sentences with no point leave them
cheated, and no amount of polish rescues that.

## Before drafting

1. **Write the point in one sentence:** what the reader should believe or do by the end. If you
   cannot, you are not ready to draft. Work it out, or ask for it. When the requester gave you a
   thesis and their reasons, the piece argues that, not a safer consensus version. When you have
   only a topic, propose a point and say you did; don't write a balanced survey of the topic.
2. **Name the reader** and what they will do with the text: decide, approve, follow steps, look
   something up. That decides the form (see [Fit the form](#fit-the-form)).
3. **List the claims that support the point, strongest first,** then order them as a chain in which
   each depends on the one before: because A, B; because B, C; so the point.
4. **Find where a skeptical reader stops agreeing,** and plan where the text answers them.
5. **Decide the ending, then the opening that sets it up.**

## Coherence: build a chain, not a list

The usual failure is a row of reasonable, parallel points, then a conclusion that is asserted
rather than earned. Any paragraph could move or go and nothing would break.

- **Every paragraph moves the reader toward the point.** A paragraph that is true and interesting
  but moves nobody comes out.
- **Rank the support.** Lead with the strongest reason or build to it on purpose; five reasons given
  equal weight read as no reason.
- **Answer the objection in the text.** The strongest pieces make the objection part of the
  conclusion ("the debt work isn't a delay on their requests; it's the fastest route to them").
- **Keep every promise.** An analogy, question or setup in the opening pays off later. An ending
  that restates the opening is not a payoff; a callback works only if the middle earned it.

## Sentences: actors, not abstractions

The most reliable tell of machine prose is an abstract noun doing the action: "That number changes
everything." "Accumulated shortcuts create friction across the lifecycle." Nobody can say such a
sentence is wrong, which is why it says nothing. People write about what people and concrete things
do, software included:

- "That number means we can't hire until Q3."
- "Our engineers spend three of every ten days working around the old builder."
- "Once every team uses the same schema, the billing service can drop its translation layer."

Make the subject the one who acts and the verb what they do. "We analyze the data," not "an analysis
of the data is conducted." If you cannot name the actor, you may not understand the claim well
enough to make it; find out before writing it.

## Cut stock glue

Cut connective phrases that perform a transition without doing one:

- "Not just X, but Y" · "It's not X, it's Y"
- "Here's the thing:" · "Now for the important part:"
- "Still X. Still Y. Just Z."
- "Honestly?" · "Let that sink in."
- "Ultimately," · "At the end of the day,"
- "In today's fast-paced world…"

Keep the links that carry logic: "because", "so", "which means", a pronoun that points at one
specific thing, a callback to a term defined earlier.

## Cadence: length steers attention

Readers skim long sentences and slow down on short ones. Use that on purpose.

- **Don't hold one rhythm.** Both failures are common: every line a three-word fragment, or every
  paragraph eight dense sentences.
- **A short sentence or one-line paragraph marks where the reader should stop:** the verdict, the
  surprising number, the decision, the ask. Once or twice in a piece; every line short means none is.
- **Let length follow the content.** Explanation, nuance and evidence run long; turns, verdicts and
  asks are short. A brief aside is fine when it serves the point.

## Specifics: real, or asked for

"Four duplicate send functions" can be checked and proven wrong, and that is why a reader believes
it. "Creates friction" cannot be, and that is why it says nothing. Replace a vague claim with the
concrete fact from your context: the number, the name, the file, the date, the person's role.
**Never invent a specific** to make a sentence land. A made-up figure presented as fact misleads a
reader who will act on it. When the real figure isn't in your context, write the claim without it
and ask, or mark the gap ("[conversion rate?]").

What gets read is what is new to the reader and what serves something they are trying to do. "The
two features your biggest customer asked for" lands; "customer expectations" does not. A surprise
needs a payoff; one without it earns a glance and is forgotten.

## Fit the form

The rules hold everywhere; their weight changes with what the reader came to do.

- **Argument and recommendation** (a proposal, a PRD's case, a decision memo, an opinion post):
  take a position. Hedging every claim is a coherence failure, not balance. Give the stance, the
  ranked chain behind it, and the objection answered.
- **Reference and instructions** (docs, a README, a guide, a runbook): the point is what the reader
  can do, stated first. Put the most-used task before the rare one. Write steps with the reader as
  the actor ("Run `make test`", "you'll see…") and with exact commands, values and names. "Take a
  position" applies less: say which option to choose by default and when to choose another.
- **Short forms** (release notes, a commit or pull request summary, a status update, an email): one
  point per line or paragraph, with the reader or their users as the actor ("You can now export
  invoices as CSV", not "CSV export functionality has been introduced"). Lead with what changed for
  them; put the ask or the decision on its own short line where it lands; stop when the point is
  made.
- **A summary** states what was found or decided first, then only the support the reader needs to
  trust it. A summary that walks through everything in the order it happened is a log.

When a form has its own required structure (a template, a ticket shape, a platform's fields), keep
the structure and apply these rules to the prose inside it.

## After drafting, run the checks

- [ ] **Shuffle test.** Could the body paragraphs be reordered without losing meaning? Then they are
      a list; rebuild the chain.
- [ ] **Deletion test.** Does the point survive removing a paragraph? Then cut that paragraph.
- [ ] **Subject scan.** Read the subject of every sentence. Most should be people or concrete
      things; rewrite each one where an abstraction acts.
- [ ] **Glue scan.** Search for the stock phrases above and remove them.
- [ ] **Cadence scan.** Are sentence lengths actually varied, and does each short line sit at a
      real point of emphasis?
- [ ] **Promise check.** Does every setup in the opening pay off?
- [ ] **Specifics check.** Is every number, name and date real and from your context? Is anything
      vague that could be concrete? Is anything invented?
- [ ] **Stance check.** When the task was to argue or recommend, does the piece commit?

Read [Examples](references/examples.md) for worked rewrites (an argument, a doc section, release
notes and a status email) when rewriting a draft or teaching the difference, and
[Sources](references/sources.md) when auditing or changing a rule here.
