# Sources

The public guidance behind the rules, each narrowed to the audience and ecosystem it supports.

## Terminology and interface writing

- [Microsoft, Style and tone](https://learn.microsoft.com/en-us/windows/win32/uxguide/text-style-tone)
  explains that consistent terminology reduces the need to decide whether different words mean the
  same action, and recommends parallel syntax for parallel interface elements. This supports one
  canonical product term without requiring identical spelling at every technical boundary.
- [Microsoft Style Guide, Top 10 tips](https://learn.microsoft.com/en-us/style-guide/top-10-tips-style-voice)
  uses sentence-style capitalization as Microsoft's default and omits terminal punctuation from
  headings and UI titles. The rules treat those as useful English UI defaults, not universal law.
- [Apple Human Interface Guidelines, Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
  recommends verbs for buttons and links and consistent formatting for each interface element type.
  Its platform-specific examples are why the rules defer to the owning design system.
- [GOV.UK Design System, Error message](https://design-system.service.gov.uk/components/error-message/)
  requires specific, concise recovery text and reuse of field-label language in errors. It also
  separates examples and hints from the error slot.
- [Microsoft Research, language choices](https://www.microsoft.com/en-us/research/?p=689796)
  reports findings from surveys, moderated and unmoderated studies, and practitioner roundtables
  across Microsoft admin products; the authors conclude that consistent terminology and content
  patterns improve predictability and scanning. The evidence concerns those products, not every
  audience.

## Accessibility

- [W3C WAI, Labeling controls](https://www.w3.org/WAI/tutorials/forms/labels/) requires labels that
  describe control purpose and recommends programmatic association, preferably with native HTML.
- [W3C WAI, Providing accessible names and descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/)
  explains that interactive elements need short, distinguishing accessible names and that visible,
  native text reduces maintenance and accessibility failures.
- [WCAG technique G211](https://www.w3.org/WAI/WCAG21/Techniques/general/G211) explains why the
  accessible name should match the visible label for speech input. WCAG 2.5.3 requires the visible
  text to be contained in the accessible name; it does not require exact equality.
- [W3C WAI, Form instructions](https://www.w3.org/WAI/tutorials/forms/instructions/) explains that
  placeholders disappear and must not replace labels or required instructions.
- [W3C WAI, User notifications](https://www.w3.org/WAI/tutorials/forms/notifications/) recommends
  concise errors that reference the field and explain correction, plus success feedback when needed.

## Code, data, and contracts

- [PEP 8](https://peps.python.org/pep-0008/) documents Python-specific naming forms and explicitly
  prioritizes internal consistency. It supports deferring casing and prefixes to the language and
  repository instead of presenting one naming convention as a cross-language rule.
- [Google AIP-140, Field names](https://google.aip.dev/140) requires the same name for the same
  concept and different names for different concepts within Google-style protobuf APIs. It also
  makes scalar fields singular, repeated fields plural, field names nouns, and measurable quantities
  carry unit suffixes. The rules use those as scoped examples for values and contracts, not as
  universal rules for every language or protocol.
- [Google AIP-180, Backwards compatibility](https://google.aip.dev/180) treats renaming a public API
  element as removal plus addition and therefore a breaking change in the same major version. This
  supports staged contract renames rather than synchronized copy edits.
- [Simon Holywell, SQL style guide](https://www.sqlstyle.guide/) is a practitioner convention for
  consistent, descriptive SQL identifiers and avoiding cryptic abbreviations. Its table plurality
  and casing choices are examples, not SQL requirements.
- [PostgreSQL lexical structure](https://www.postgresql.org/docs/current/sql-syntax-lexical.html)
  explains that unquoted identifiers fold to lower case and quoted identifiers remain case
  sensitive. This supports deferring engine identifier mechanics to the engine's own documentation.
- [AlSuhaibani et al., method naming practices](https://arxiv.org/abs/2102.13555) surveys more than
  1,100 professional developers and reports broad agreement that method-naming standards matter and
  are applied. It supports treating naming as a reviewable engineering concern; it does not establish
  one universal naming form across languages or ecosystems.

## Rules without a single source

The sources do not establish one universal vocabulary workflow. A do/don't pair not mapped to a
citation above rests on its own `Why` or failure column: apply it to that named failure and no
further. These rules are of that kind:

- Prefer a precise concept name over placeholders such as `data` or `item`; the stated failure is
  that a reader must reconstruct the value's meaning from assignments and callers.
- Name an operation for its observable outcome; the stated failure is that a generic verb such as
  `process` or `handle` makes the reader reconstruct the outcome from the implementation.
- Put regulated wording, published compatibility, and established ecosystem conventions ahead of a
  default here; those are authority constraints, while the default is only a preference.
- Preserve stored data, dashboards, alerts, and other consumers during non-API renames; AIP-180
  directly supports only published API compatibility.
- Preserve immutable third-party names at an adapter boundary and document the canonical mapping;
  AIP-180 does not govern vendor schemas.
- Prefer positive predicates only when they preserve the same fact. Negative domain facts,
  regulated wording, and fixed contracts are scoped exceptions; silently inverting them can change
  behavior rather than improve a name.
- Recommend an exact name, architecture, interaction, owner, or risk severity only when the supplied
  evidence establishes it. Otherwise state the assumption or decision needed. This is an execution
  guardrail against false precision, not a sourced universal naming rule.
- Comment non-obvious workflow sequencing, state handoffs, side-effect boundaries, and the reason a
  future maintainer must preserve them; avoid narrating self-evident statements. The named failure is stale prose becoming a
  second, conflicting description of the program.
- Treat missing meaning as unresolved rather than completing the scenario with plausible domain
  behavior. This restraint applies to names and to example comments; otherwise illustrative text
  is easily mistaken for a verified contract.
- Write confirmation consequences with the specific entity, availability change, affected existing
  relationships, and truthful recovery path. Vague pronouns and generic permanence language hide
  the decision a user is authorizing. Write only what the product behavior establishes.

## Name composition

- [ISO/IEC 11179-5:2005, *Metadata registries — Naming and identification principles*](https://cdn.standards.iteh.ai/samples/35347/775e430277b149ba8fe4c5b823cc8967/ISO-IEC-11179-5-2005.pdf) —
  the standard supplies the vocabulary the naming rule is built on: an **object class term** is "part
  of the name of an administered item which represents the object class to which it belongs", a
  **property term** "expresses a property of an object class", and a **representation term** is the
  "designation of an instance of a representation class" (clause 3). Clause 6.2 requires a naming
  convention to document its semantic, syntactic, and lexical rules, and notes that "an effective
  naming convention can also enforce the exclusion of irrelevant facts about the administered item
  from the name". **Read this boundary carefully before citing it:** the object class + property +
  representation composition appears in **Annex A, which the standard labels informative**, and
  clause 7.5 offers "the property term is always the last part of a name" merely as an example of an
  absolute syntactic rule. 11179-5 therefore does *not* mandate the composition, and writing "ISO
  11179 requires" it would be a citation error. The linked copy is a watermarked publisher preview
  covering clauses 1–7 and the start of Annex A. The current edition, 11179-5:2015, is behind
  [ISO's OBP](https://www.iso.org/obp/ui/en/#!iso:std:60341:en), which returned HTTP 403 and could
  not be verified.
- [WIPO Standard ST.96, Annex I — XML Design Rules and Conventions, v10.0 (2026)](https://www.wipo.int/standards/en/st96/v10-0/annex-i/03-96-i.pdf) —
  this is the normative, MUST-level statement of the composition, and states that its conventions
  "are based on the guidelines and principles described in document ISO 11179 Part 5". **[GD-21]**:
  "the Object Class Term MUST precede the Property Term and the Property Term MUST precede the
  Representation Term." **[GD-05]**: names "SHOULD consist only of nouns, adjectives, and verbs in
  the present tense". **[GD-27]**: "Connecting words like 'and', 'of' and 'the' SHOULD NOT be used
  … unless they are part of the business terminology." GD-05 and GD-27 together are the evidentiary
  basis for excluding interrogatives and sentence-shaped names: `who`, `why`, and `when` are none of
  noun, adjective, or present-tense verb, and `how_an_invoice_is_paid` carries both an article and a
  copula. **[GD-22]** removes a representation term that repeats the property term, which is why the
  skill treats the generic word as a suffix rather than a separate ban. **[GD-25]** — "Word(s) in a
  name SHOULD be in singular form unless the concept itself is plural" — is the ST.96 half of the
  table-number row in the skill's conventions table, and the reason that row reports no consensus
  rather than following the frameworks.
- [ISO/IEC 11179-4:2004, *Formulation of data definitions*](https://cdn.standards.iteh.ai/samples/35346/e1828b73c98b4fbca61fe950da0b7748/ISO-IEC-11179-4-2004.pdf) —
  clause 4.1 requires that a data **definition** "be stated as a descriptive phrase or sentence(s)"
  and clause 4.2 that it "be expressed without embedding rationale, functional usage, or procedural
  information". The standard assigns the sentence to the definition; 11179-5 clause 3.4 defines a
  name separately as a "designation of an object by a linguistic expression". **This is the skill's
  inference, not a literal prohibition:** no located source names question-shaped columns as an
  antipattern, and the skill's opening line — a sentence in the name's slot is a definition in the
  wrong place — is assembled from the two standards' division of labour.

## Domain vocabulary

- [Eric Evans, *Domain-Driven Design Reference*, March 2015](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) —
  the Ubiquitous Language pattern commits a team to one language "in all communication within the
  team and in the code", holds that "a change in the language is a change to the model", and
  directs teams to "refactor the code, renaming classes, methods, and modules to conform". Model-Driven
  Design adds "draw from the model the terminology used in the design". This supports taking the
  schema's words from the domain rather than inventing a superordinate. The Domain Events summary
  separately notes that such an event "typically contains a timestamp for the time the event
  occurred and the identity of entities involved", which is the model-level shape behind
  `paid_at` plus `payer_account_id`. The publisher returns HTTP 403 to some clients; the document
  was retrieved directly and read.
- [Martin Fowler, "Ubiquitous Language", 31 October 2006](https://martinfowler.com/bliki/UbiquitousLanguage.html) —
  a short attribution of the term to Evans and a statement of the practice. It establishes currency
  of the idea outside its source book and nothing more; it supplies no naming mechanics.
- [Feitelson, Mizrahi, Noy, Ben Shabat, Eliyahu, and Sheffer, "How Developers Choose Names",
  arXiv:2103.07487, 12 March 2021](https://arxiv.org/pdf/2103.07487) — 334 subjects across a
  sequence of experiments (the first survey ran on Qualtrics in May 2018: 121 questions, 11
  scenarios, 234 respondents, 70% students, mean 5.8 years of experience). Two findings carry the
  skill's rules. First, naming is not self-correcting: across 47 instances "the median probability"
  that two developers choose the same name "was only 6.9%". Second, a structured procedure measurably
  helps — names produced with the authors' three-step model (select the concepts, choose words for
  each, construct the name) "were judged by two independent judges to be superior … by a ratio of
  two-to-one". That model is the practitioner-facing analogue of the object class / property /
  representation decomposition, and it is the one empirical result that endorses structured name
  construction rather than taste.

## Meaningless and misleading names

- [Tim Ottinger, "Ottinger's Rules for Variable and Class Naming" (1997)](https://exelearning.org/wiki/OttingersNaming/) —
  Rule 14, "No Disambiguation without Differentiation", states plainly that "Info and Data are like
  'stuff': basically meaningless", with the pairs `ProductInfo`/`Product`, `CustomerObject`/`Customer`, and
  `NameString`/`Name`; the skill's `product_info` and `name_string` examples are these, transposed to
  SQL. Rule 11 supplies the disinformation case — do not call something an `AccountList` unless it is
  a list. This is the documented antecedent of the naming chapter in Robert C. Martin's *Clean Code*
  (2008); that chapter has no free primary text and is **not** cited here, because every available
  version of it was a third-party summary. The link above is a mirror — the original at
  `objectmentor.com` is defunct.
- [Avidan and Feitelson, "Effects of Variable Names on Comprehension: An Empirical Study", ICPC 2017](https://www.cs.huji.ac.il/~feit/papers/Names17ICPC.pdf) —
  9 professional developers, 6 methods drawn from production utility packages, 38 recorded sessions
  over roughly 22 hours, with variable names replaced by consecutive letters of the alphabet. The
  result that matters here is the negative one: in 3 of the 6 methods there was no significant
  difference between the real names and the meaningless ones, "due to poor and even misleading
  variable names". A bad name is not merely untidy — it can carry as little as no name at all.
- [Lawrie, Morrell, Feild, and Binkley, "Effective Identifier Names for Comprehension and Memory",
  *Software Quality Journal*](https://www.cs.kent.edu/~jmaletic/cs63902/Papers/Lawrie07.pdf) — 128
  participants, 12 functions of 8–36 lines, three variants differing only in identifier quality
  (single letters, abbreviations, full words), comments stripped. "Full-word identifiers lead to the
  best comprehension", though often without a statistical difference from well-chosen abbreviations.
  **Scope this claim honestly when citing it:** the study contrasts identifier *length*, not
  question-shaped against value-shaped names, so it supports the cost of meaningless names and not
  the specific antipattern. This is the author preprint; the publisher version is paywalled, and the
  ICPC 2006 conference original (DOI 10.1109/ICPC.2006.51) was not openly fetchable.

