---
name: writing-prose
description: Use when writing, rewriting or reviewing prose a person will read — a doc, README, guide, PRD, proposal, report, summary, email, announcement, release notes, a pull request or issue description, a status update, or any reply longer than a few lines — and when a draft reads as generic, padded, listy or machine-written. It supplies the order of work for a piece that builds to one point, written from the reader's side with real actors and nouns, varied cadence and real specifics, with checks to run before and after drafting. Do not use for code, code comments, or names and labels inside an interface.
---

# Writing prose

People who read model-written prose feel their time was wasted even when they cannot say why. The
cause is usually the same: the sentences link to each other well (**cohesion**), but the piece does
not build to a point (**coherence**), and every sentence has the same rhythm (**cadence**). The
fixes come in that order of importance: **coherence, then cadence, then cohesion.** A reader
forgives a clumsy sentence around a clear point; polished sentences with no point leave them
cheated, and no amount of polish rescues that. Underneath all three is perspective: write from
where the reader sits, about who does what, in the reader's own words.

Scrubbing the tics (the em dashes, "not X, but Y", "honestly?") does not fix this. Text with every
tic removed still reads as machine-made when it has no point, no chain and one rhythm, because those
live in the structure of the whole piece, not in any sentence.

**The three C's are required, not advice:** a piece that fails any one of them is not done, however
clean its sentences. Prose that sounds like a person is what passing all three produces: a point
the reader is led to, a rhythm that moves, and sentences that lean on each other. The stiff run of
"It does X. It does Y." fails two at once, cadence (one length and shape) and cohesion (facts
stacked with no so, because or then between them), and no edit may fix one C by worsening another.

## Before drafting

1. **Write the point in one sentence:** what the reader should believe or do by the end. If you
   cannot, you are not ready to draft. Work it out, or ask for it. When the requester gave you a
   thesis and their reasons, the piece argues that, not a safer consensus version. The point, the
   angle and the judgment are the requester's to supply: a point you generate from a bare topic
   drifts to the safe average. With only a topic, ask for the point; when you cannot ask, propose
   one and say plainly it is your proposal. Never write a balanced survey in its place.
2. **Name the reader, what they already know, and what they will do with the text:** decide,
   approve, follow steps, look something up. That decides the form (see
   [Fit the form](#fit-the-form)) and which words need no explaining.
3. **List the claims that support the point, strongest first,** then order them as a chain in which
   each depends on the one before: because A, B; because B, C; so the point.
4. **Find where a skeptical reader stops agreeing,** and plan where the text answers them.
5. **Decide the ending, then the opening that sets it up,** or draft through to the conclusion and
   then rewrite the opening so it points there.

## Coherence: build a chain, not a list

The usual failure is a row of reasonable, parallel points, then a conclusion that is asserted
rather than earned. Any paragraph could move or go and nothing would break.

- **Every paragraph moves the reader toward the point.** A paragraph that is true and interesting
  but moves nobody comes out.
- **Rank the support.** Lead with the strongest reason or build to it on purpose; five reasons given
  equal weight read as no reason. Judge strength by this reader: the reason that touches what they
  are trying to do, or answers what they would object to, beats the one that sounds most general.
  When you cannot tell, ask the requester which reason carries the argument.
- **Shepherd the reader.** Notice where a reader would wander off the path or stop agreeing, and
  close that path where it opens: answer the objection, or raise an idea and reject it in the open.
  The strongest pieces make the objection part of the conclusion ("the debt work isn't a delay on
  their requests; it's the fastest route to them").
- **Keep every promise.** An analogy, question or setup in the opening pays off later. An ending
  that restates the opening is not a payoff; a callback works only if the middle earned it.
- **Don't argue in bullets.** A bullet list drops the "because" between claims, so the reader gets
  parallel assertions and has to build the chain themselves. Bullets are for things that really are
  parallel: steps, options, a checklist, items to compare.

## Perspective: write from the reader's side

The reader was not there while you worked. They don't know your file names, your ticket numbers,
the order you tried things in, or the label you coined an hour ago, and nothing in the text tells
you what they are missing, because to you it all reads as obvious.

- **Lead with what the reader gets, not what you did.** "Exports now finish in under a minute," then
  how, only if they need the how to trust or repeat it. A report that narrates the work in the order
  it happened ("First I looked at…, then I tried…") makes the reader dig for the result.
- **Hold one point of view.** Where the text speaks to the reader, call them "you" and the writer
  "I" or "we", and keep it. Never call the reader "the user" in text they read, and don't drift
  between "we", "the team" and "one".
- **Sound like a person talking to them.** Where the text speaks to the reader, write it the way
  you'd explain it across a desk: "you" leads often, contractions are fine unless the project's
  style says otherwise, and why it matters to them comes in the same breath as what happens. Plain
  is not flat: "it opens even when you're offline" beats "it opens without a network connection",
  because the reader hears a person in the first. Warmth comes from specifics, never from
  adjectives or exclamation marks.
- **Start from what they know and end on what is new.** Open a sentence with something the reader
  already has (the thing they asked about, the term from the last sentence), and put the new
  information last, where a reader puts the weight. The first words of each paragraph and heading
  carry the point, because a skimming reader reads little else.
- **Every heading stands alone.** A headline, title, subtitle, section heading, table column
  header, list label, button, navigation title or link is often all a skimming reader sees, so a
  reader who sees only that line knows what it labels.
  It names its subject: no pronoun ("it", "this", "they") unless its noun is in the same line,
  and nothing borrowed from the line before or the page around it. Its verb is the action, not a
  vague stand-in, and it needs no body to decode: "Shape it chapter by chapter." fails twice,
  because "shape" names no action and "it" names nothing; "Know how long it runs, and how long it
  reads." is a riddle; "See your word count and reading time." works. A column header names
  what the column holds, not the row's subject by pronoun: "What it does" becomes "Description". The
  section's first sentence stands alone too, without leaning on the heading above it.
- **Write for the least-informed reader you are writing for.** Define a term the first time it
  appears, or replace it with the plain words it stands for.

## Sentences: actors, not abstractions

The most reliable tell of machine prose is an abstract noun doing the action: "That number changes
everything." "Accumulated shortcuts create friction across the lifecycle." Nobody can say such a
sentence is wrong, which is why it says nothing. People write about what people and concrete things
do, software included:

- "That number means we can't hire until Q3."
- "Our engineers spend three of every ten days working around the old builder."
- "Once every team uses the same schema, the billing service can drop its translation layer."

An occasional abstract subject is fine; paragraph after paragraph of them is the tell. Make the
subject the one who acts and the verb what they do. "We analyze the data," not "an analysis
of the data is conducted." If you cannot name the actor, you may not understand the claim well
enough to make it; find out before writing it.

**Give software only the verbs software does.** Code stores, sends, counts, matches, totals,
applies a rule and refuses. People and the business learn, know, decide, judge, want and
understand. "Insights learns what each lead is worth" hides who learns, and from what, and states
something nobody can build or test; write "insights totals what each lead earned, so the team sees
which sources pay". "Routing decides where a lead goes" becomes "routing applies the rule sales
set". A system with a mind in the prose is a decision nobody owns. A goal the requester gave as
theirs ("we want to learn which leads bind") stays theirs; don't let it drift into a feature. A
company that learns, as when a seller learns which leads convert, is a real actor and fine.

**Every sentence survives a cold read from the reader's seat.** A person reads each sentence as
news about their own situation: what they learn, what they can now do or decide, what to expect,
how it affects them. Read it as that person, who was not there, and ask two things: can they say
who does what, to what, and what does it tell them about theirs? A sentence that fails makes the
reader stop and think "what did I just read?", and it is usually an abstraction acting, software
given a mind, a metaphor standing in for the mechanism ("the scoring service is the brain of the
platform"), a stack of nouns hiding a process ("routing by learned value"), or a true statement
about the system's insides that means nothing to this reader. Rewrite it as the plain event and
what it means for them: "routing sends each lead to the partner whose leads bound most often, so a
partner's share grows as their leads bind". When you cannot, you do not yet know what happens or
why it matters to them; find out, or mark the gap.

## Nouns: the reader's words for concrete things

- **Name the thing, not its category.** "The Export button", "the March invoice run", "the two
  admins at the customer", not "the functionality", "the process", "stakeholders", "the solution",
  "resources". A category noun marks where a specific should have been.
- **Use the reader's word,** not the code's or yours: "invoice" when the reader says invoice, even
  if the table is `billing_documents`. When the reader needs both, as in a developer guide, give the
  reader's word and the identifier once, together.
- **One term per thing.** Once it is "the import", it stays "the import", not "the upload", "the
  sync" and "the ingestion" in turn. A reader assumes a new word means a new thing.
- **Put the action back in the verb.** "Decide," not "make a decision"; "we migrated the data," not
  "the migration of the data was performed". A noun made from a verb hides both the action and who
  did it.
- **Spell in American English** unless the project's published copy or the requester spells
  another way, and keep it even when your notes or sources use British, because a reader who
  meets both reads two writers. Each British pattern has an American form:
  colour → color, flavour → flavor, favourite → favorite, behaviour → behavior;
  organise → organize, customise → customize; analyse → analyze; centre → center;
  licence → license, defence → defense; cancelled → canceled, travelling → traveling;
  catalogue → catalog; grey → gray. Write the plain word for the old one: while, not whilst;
  among, not amongst; will or must, not shall. A name, quote or interface label keeps its own
  spelling.

## Cut what performs instead of saying

**Stock glue** is a connective phrase that performs a transition without making one:

- "Not just X, but Y" · "It's not X, it's Y"
- "Here's the thing:" · "Now for the important part:"
- "Still X. Still Y. Just Z."
- "Honestly?" · "Let that sink in."
- "Ultimately," · "At the end of the day,"
- "In today's fast-paced world…"

Good writers use these devices too; the tell is reaching for them by reflex, several to a piece.
Default to cutting them, and keep one only where it does a turn the text needs. Keep the links that
carry logic: "because", "so", "which means", a pronoun that points at one specific thing, a callback
to a term defined earlier.

The same test, does this sentence tell the reader anything, removes the other tells of machine
prose:

- **Signposts and wrap-ups:** "In this section, we'll explore…", "It's worth noting that", "In
  summary,". Say the thing; a summary is earned only by a long piece.
- **Empty praise and reassurance:** "great progress", "the team has been amazing", "rest assured",
  "moving in the right direction". Replace with the fact behind it or cut it. A thank-you that names
  what someone did ("Priya's script cut the validation run from a day to an hour") is a fact; keep
  it.
- **Catch-alls:** "various improvements", "and more", "other fixes". Name the items or leave them
  out.
- **Hedge stacks and inflation:** "may potentially help to", "truly", "incredibly", "robust",
  "seamless", "leverage", "delve", "pivotal", "serves as" where "is" would do, adjectives in threes
  ("fast, reliable and scalable"), and a trailing clause that asserts significance (", highlighting
  the importance of…"). One honest qualifier where the doubt is real; otherwise the plain claim.
- **Vague attribution:** "experts say", "studies show", "many users feel". Name who, or drop it.

## Cadence: length steers attention

Readers skim long sentences and slow down on short ones. Use that on purpose.

- **Don't hold one rhythm.** Both failures are common: every line a three-word fragment, or every
  paragraph eight dense sentences.
- **A short sentence or one-line paragraph marks where the reader should stop:** the verdict, the
  surprising number, the decision, the ask. Once or twice in a piece; every line short means none
  is.
- **Vary the shape, not only the length.** Sentence after sentence with the same subject and build
  ("It stores X. It sends Y. The app shows Z.") reads as a spec sheet even when every one is true;
  it fails cadence, and cohesion with it. Join the facts that lean on each other with so, because, then, while or which means, and let
  another subject, often "you", open the next. Software keeps its software verbs; it just stops
  being the subject of every sentence.
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
works when it breaks a pattern on purpose and then resolves into the point; one without that payoff
earns a glance and is forgotten. Novelty wears out: a device everyone now uses (the self-deprecating
hook, a line per sentence, the contrarian opener) is no longer a surprise.

## Fit the form

The rules hold everywhere; their weight changes with what the reader came to do.

- **Argument and recommendation** (a proposal, a PRD's case, a decision memo, an opinion post):
  take a position. Hedging every claim is a coherence failure, not balance. Give the stance, the
  ranked chain behind it, and the objection answered.
- **Reference and instructions** (docs, a README, a guide, a runbook): the point is what the reader
  can do, stated first. Open a guide or doc page from the moment the reader is in, then what
  they'll be able to do, never from a definition of the system: not "The rollback command reverts
  a deployment to a previous release", but "A deploy just broke checkout and you want the last
  good release back. This page shows how to roll back with one command and check it worked." Put
  the most-used task before the rare one. Write steps with the reader as the actor ("Run `make
  test`", "you'll see…") and with exact commands, values and names. "Take a position" applies
  less: say which option to choose by default and when to choose another.
- **Short forms** (release notes, a commit or pull request summary, a status update, an email): one
  point per line or paragraph, with the reader or their users as the actor ("You can now export
  invoices as CSV", not "CSV export functionality has been introduced"). Lead with what changed for
  them; put the ask or the decision on its own short line where it lands; stop when the point is
  made.
- **Short-attention forms** (a social post, a headline, the top of a landing page): novelty does
  the most work. One deliberate pattern break, resolved into the point in the next line.
- **A summary** states what was found or decided first, then only the support the reader needs to
  trust it. A summary that walks through everything in the order it happened is a log.

When a form has its own required structure (a template, a ticket shape, a platform's fields), keep
the structure and apply these rules to the prose inside it.

## Improving a draft

The same rules apply when the text already exists, yours or someone else's, but the order matters
more: coherence is a property of the whole piece, so no amount of sentence editing creates it.
Work from the outside in, and don't polish a paragraph you may cut.

1. **Find the draft's point.** Write it in one sentence. If the draft has none, that is the
   finding; ask the author for it, or propose one and say so, before touching a sentence.
2. **Fix the structure.** Write one line per paragraph saying what it claims, then run the shuffle
   and deletion tests on that outline. Reorder into a chain, cut what moves nobody, add the missing
   objection, and check the opening's promises against the ending.
3. **Set the cadence.** Find the one or two places the reader must stop, and land them short; let
   the explanation around them run long.
4. **Then the sentences:** subjects, nouns, perspective, and the performative phrases, last.
5. **Keep what is the author's:** their point, their facts and their voice. Never add a claim,
   number or name they did not give; mark the gap instead. Change only what fails a rule, with the
   smallest edit that fixes it, and leave a true, natural sentence as it is. An edit keeps every
   concrete detail and the author's register: "notarized, with its own notarization ticket, so it
   opens even when you are offline" must not become "notarized, so it opens without a network
   connection", which drops the ticket and the person.

When asked to review rather than rewrite, report in the same order: whether the piece has a point
and a chain first, then cadence, then sentence-level fixes, each with the passage quoted and the
change it needs, offered as a suggestion. A review that lists only phrase-level edits has skipped the part that matters.

## After drafting, run the checks

The piece passes only when the coherence checks (shuffle, deletion, promise, stance), the cadence
scan and the cohesion check all pass; fix each failure and run them again. When reviewing, report
each C by name, pass or fail, with the passage behind it.

- [ ] **Shuffle test.** Could the body paragraphs be reordered without losing meaning? Then they are
      a list; rebuild the chain.
- [ ] **Deletion test.** Does the point survive removing a paragraph? Then cut that paragraph.
- [ ] **Subject scan.** Read the subject of every sentence. Most should be people or concrete
      things; rewrite each one where an abstraction acts. Then search for learn, know, decide,
      judge, want, understand, think, own and care, and confirm each subject is a person or the
      business, not software.
- [ ] **Cold read.** Read every sentence as the reader, who was not there. Can they say who
      does what, to what, and what it means for them? Rewrite each one where they would stop and
      ask what it means.
- [ ] **Reader check.** Does the first paragraph give the reader the result, not your process? Is
      every name, label and abbreviation one this reader already knows or is told once? One point
      of view throughout?
- [ ] **Heading check.** Read each headline, title, subtitle, heading, column header, list
      label, button, navigation title and link alone, with nothing around it. Would a skimmer
      know what it labels? Rewrite each one that
      leans on a pronoun, a vague verb, wordplay or the text around it, and check the first
      sentence under it the same way.
- [ ] **Noun scan.** Replace each category noun (functionality, process, solution, stakeholders)
      with the thing it stands for; one term per thing; verbs back out of nouns; American
      spelling unless the project spells another way.
- [ ] **Glue scan.** Search for the stock phrases, signposts, empty praise, catch-alls and
      inflated words above, and remove them.
- [ ] **Cadence scan.** Are sentence lengths and shapes actually varied, with no run of sentences
      opening on the same subject, and does each short line sit at a real point of emphasis?
- [ ] **Cohesion check.** Does each sentence take up something from the one before (a term, a
      pronoun pointing at one thing, a so, because, then or while) instead of starting a new fact
      cold? Join the stacked ones.
- [ ] **Detail check.** When editing existing text, is every concrete detail still there, and did
      any natural phrase become a more formal one? Put it back.
- [ ] **Promise check.** Does every setup in the opening pay off?
- [ ] **Specifics check.** Is every number, name and date real and from your context? Is anything
      vague that could be concrete? Is anything invented?
- [ ] **Stance check.** When the task was to argue or recommend, does the piece commit?

Read [Examples](references/examples.md) for worked rewrites (an argument, a doc section, release
notes, a status email, a report of finished work, and stiff product and docs copy made to sound
like a person) before writing or rewriting copy that speaks to the reader, and when teaching the
difference, and [Sources](references/sources.md) when auditing or changing a rule here.
