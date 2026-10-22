---
name: naming-software-terms
description: Use when choosing, reviewing, or standardizing software terminology across source code, schemas, APIs, logs, and product interfaces, especially when one concept crosses several layers. It supplies the naming grammar for precise terms, layer-appropriate names, clear interface text, and compatibility-safe renames. Do not use for general prose editing, brand naming, marketing copy, or work where naming is incidental.
---

# Name software terms

Keep one vocabulary per concept across code, data contracts, and product interfaces. Preserve
intentional layer forms and compatibility mappings instead of forcing identical spelling.

## Name the meaning

> **Name each value or entity for what it is, and each operation for its outcome.**

A value or entity name states what it represents. An operation name states the outcome it produces. A description explains mechanism, context, or constraints. These are different jobs; mixing them produces names that are hard to scan and easy to misread.

| Layer | Mechanism (wrong) | Meaning (right) |
|---|---|---|
| Column header | `How retries are handled` | `Retry limit` |
| Field label | `Why is this archived?` | `Reason` |
| DB column | `retry_mode_flag_2` | `retry_limit` |
| Function | `processData()` | `normalizeAddress()` |
| Class | `InvoiceHelper` | `InvoiceRateSheet` |
| API error | `ERR_5` | `INVOICE_NUMBER_TAKEN` |
| Event | `invoiceUpdateHappened` | `invoice.archived` |

## The four failure modes

Assume you are about to commit one of these and check explicitly.

**1. Naming the mechanism instead of the value.**
`How retries are handled` → `Retry limit`. `handleUserStuff()` → `deactivateUser()`. The name describes the process rather than identifying the thing.

**2. Question words and sentences where value names or compact labels belong.**
`Why` → `Reason`. `Who asked` → `Requester`. `did_the_user_confirm` → `is_confirmed`. Name values and entities with noun phrases or established state terms; name actions with verbs. A form journey may deliberately use a direct question when that pattern helps the user.

**3. Blending two jobs into one string.**
A label trying to also be an explanation. A function name trying to describe its whole algorithm. A column name carrying its own documentation. Split it: the noun stays, the explanation moves to a tooltip, a docstring, or a comment.

**4. Prose register where a factual statement belongs.**
`There is nothing here right now` → `No archived documents.` `// this is where we cleverly loop back around and fix the thing` → say why, in one line, or delete it.

Generated names and interface text often blend prose, mechanism, and explanation. Check these failure modes explicitly instead of assuming a fluent sentence occupies the correct slot.

## Test each proposed name

Run these on any name or string before writing it.

1. **Meaning test.** What fact, value, action, or outcome is established? Do not choose an exact
   name, migration, endpoint, event, interaction, owner, or risk severity that the evidence does
   not support. If the outcome is unknown, say that the exact name is unresolved; do not fill the
   gap with illustrative domain names that look like recommendations.
2. **Canonical-term test.** Does the concept already have a term in the code, schema or interface? Reuse it instead of coining a synonym.
3. **Slot test.** Is this explaining something? Then it belongs in a description slot, not a name.
4. **Constraint test.** Is a spelling fixed by a published or third-party contract, regulated text,
   localization, privacy, or an established platform convention? Preserve it and document the
   mapping.
5. **Fortieth-time test.** Read it as the person who encounters it for the fortieth time: the operator scanning the table, the engineer reading the stack trace at 2 AM. Does it help them scan, or make them read?

## Keep one canonical term

Give each concept one canonical term. Canonical parity means shared meaning, not character-for-character
spelling. Express the term through each layer's convention and document intentional compatibility,
vendor, localization, privacy, or audience-specific mappings:

```
consumer          DB column / table
consumer_id       foreign key
consumer          API field
Consumer          class / type
consumer          variable
Consumer          UI label
Consumers         page title, nav item, export header
```

When the database says `cust_flg`, the model says `isCustomer`, the API says `customer_type`, and the screen says `Client`, you have four vocabularies for one idea. Every engineer, every support agent, and every user pays a translation tax forever, and every new agent session invents a fifth.

**The parity test:** when two layers represent the same concept, confirm that their names map to one canonical term. Do not require mechanical spelling parity: database columns, public API fields, localized labels, and compatibility aliases may differ deliberately. Record the mapping.

## Look up terms before inventing them

Agents **look terms up before proposing them.** Consistency is unreachable through better writing
alone, because every file and screen written independently can invent a fresh synonym for the same
concept. Search how the codebase already names the concept — its schema, models, API, interface
strings and docs — and reuse that term. When the project already keeps a glossary, follow it and
update only the entry your change touches.

**Do not build a lexicon.** Never create a glossary, term registry or vocabulary database as part of
naming work, and never inventory a product's terms. It is a second source of truth that drifts from
the code it describes, and it turns one naming decision into a documentation project nobody asked
for. The code is the record of the vocabulary; the name you choose is the deliverable.

When no established term exists, state the missing evidence, propose only the smallest supported
candidate, and request the owner's decision instead of filling every layer speculatively. Add or
rename product vocabulary only with the owner's authority.

## Apply the product defaults

Use these as defaults for operator-style software. Follow a product's established exceptions; regulated wording, published contracts, platform conventions, localization, and established domain language take precedence.

| Don't | Do | Why |
|---|---|---|
| Em dashes used as routine asides | Period, parentheses, or restructure | Keeps operator text direct. A product may choose another punctuation style; `—` may also be its null marker |
| Abbreviations that are not domain standard (`cust`, `qty_rcv`, `mgr`) | Full words | Saves keystrokes once, costs comprehension forever |
| Negated names that merely invert a positive condition (`is_not_active`, `disable_notifications`, `hideCompleted`) | Positive form (`is_active`, `notifications_enabled`, `show_completed`) | Double negatives at every call site and an ambiguous "off" state; preserve a negative form when the domain fact or fixed contract is genuinely negative |
| Type or class in the name (`strName`, `reason_text`, `InvoiceObject`, `user_list`) | The meaning (`name`, `reason`, `Invoice`, `users`) | The type is already declared, and it changes |
| Grab-bag words (`data`, `info`, `item`, `thing`, `util`, `helper`, `manager`, `handler`, `stuff`, `temp`) | The specific thing | These are names that mean "I have not decided what this is" |
| Numeric suffixes (`data2`, `processUser3`, `column_b`) | Distinct meanings, distinct names | The suffix is the missing distinction |
| Vague pronouns for named entities (`Something here already exists`) | Name the entity | The system knows what it is; say it |
| Unchosen first-person voice (`we couldn't find`, `our records`) | The product's defined voice or a factual statement | Prevents one screen from inventing a different speaker |
| Marketing adjectives in functional text (powerful, seamless, robust, smart) | Nothing | Says nothing to someone doing the task |
| Unchosen exclamation marks and emoji in system text | The product's defined feedback style | Prevents accidental tone changes in operational text |
| Minimizers (simply, just, easily, only) | Omit | They add no recovery information and can understate difficulty |
| Hedging (`it looks like`, `it seems`, `apparently`) | State what is known | Erodes trust in every other message |
| Inconsistent verbs for one operation (`get` / `fetch` / `retrieve` for the same act) | One verb per meaning, product-wide | Every synonym implies a distinction that does not exist |
| Stale names after a refactor | Classify the boundary, then rename privately or stage a compatible migration | A wrong name misleads, while an unsafe rename breaks consumers |

## Choose the product register

One decision per product, read from its existing interface and rules.

| Register | Fits | Character |
|---|---|---|
| **Operator** (default) | Internal tools, admin panels, back office, developer tools | Dense, factual, terse; optimized for scanning |
| **Practitioner** | Professional SaaS with self-serve onboarding | Same grammar, more explanation slots filled |
| **Consumer** | Public apps, first-run flows | Same grammar, plainer vocabulary, more guidance |

Register changes **how much explanation appears** and **how domain-specific the vocabulary is**.
Keep each slot's purpose stable while allowing language, localization, accessibility, and established
design-system grammar to shape the surface form. "Plain and human" is not the same as "chatty and vague."

For new work with no product evidence, operator register is a fallback. In an existing product,
inspect its interface and conventions before applying that fallback; keep recommendations
conditional when the evidence is unavailable.

## Apply the conventions

Before writing any name or user-facing string:

1. **Identify what you are naming**: a stored value, a behavior, a type, an event, or a slot on screen. If you cannot say which, you do not yet know what you are writing.
2. **Look up how the codebase already names every recurring concept.** Missing? Propose the smallest supported term to the owner before coining a synonym.
3. **Apply the form** for that kind of name (see the reference files).
4. **Split, don't blend.** Name in the name; explanation in the docstring, comment, tooltip, or help text.
5. **Check parity** across layers. Distinguish accidental drift from an intentional, documented mapping.
6. **Scan the product defaults.**
7. **Apply the fortieth-time test.**
8. **Report proportionately.** Answer the requested naming scope first. Separate facts, assumptions,
   owner decisions, and compatibility risks. Do not invent adjacent architecture or repeat the same
   rationale for every layer. Omit executive summaries, status sections, checklists, and exhaustive
   layer tables unless the user asks for them or they materially clarify the decision.

## Resolve the convention stack

Consistency means each owner supplies one part of the name; it does not mean copying one layer's
spelling into every other layer.

1. The product's established term, as the code and interface already use it, supplies the canonical
   concept and meaningful distinctions.
2. The data model supplies engine-independent value composition, cardinality, relationships, and
   shape.
3. The active framework or ORM supplies derived forms such as model, table, key, relationship, and
   timestamp conventions.
4. The database engine supplies identifier and migration constraints, from its own documentation.
5. Published, generated, vendor, regulated, and localized forms remain documented boundary mappings.

Inspect the owning stack before recommending a spelling. Preserve one convention within each
bounded layer, configure deliberate exceptions explicitly, and do not export Laravel, PostgreSQL,
MySQL, SQLite, or another ecosystem's convention as a universal rule.

## Read the relevant reference

Read the one that matches what you are writing. Read more than one when a change crosses layers, which most do.
Do not load every reference for a single-layer task.

| File | Covers |
|---|---|
| [Code](references/code.md) | Read for variables, booleans, collections, functions, classes, modules, parameters, constants, errors, events, jobs, feature flags, config and environment variables, tests, comments, and commits. |
| [Data and contracts](references/data-and-contracts.md) | Read after the model is chosen for stored and published names: columns, enums, migrations, error codes, events, logs, and exports. Modelling, framework schema conventions, and HTTP resource and payload design belong to that work's own guidance. |
| [Product interface text](references/product-ui.md) | Read for titles, navigation, columns, labels, placeholders, controls, buttons, tooltips, empty states, validation, errors, confirmations, metrics, and charts. |
| [Sources](references/sources.md) | Read only when auditing, changing, or extending a rule; it maps each rule to its evidence and scope. |

## Respect established constraints

Apply the same exception every time rather than deciding case by case.

- **Regulated wording wins.** Legal disclosures, consent language, and required notices are written by counsel and reproduced exactly.
- **Established platform and language conventions win.** Follow the idioms of the language and framework in use over the preferences here. Ruby is not Java is not Go.
- **Real domain jargon wins over plain language.** If practitioners say "endorsement," the term is `endorsement`, not `policy change`. Plain language means avoiding *invented* abstraction, not avoiding the reader's actual vocabulary.
- **Existing codebase conventions win over local preference.** Consistency with the surrounding code beats correctness in isolation. If a codebase is uniformly wrong, propose a migration rather than introducing a second convention.
- **Fixed third-party names stay at the boundary.** Preserve vendor fields and generated contract
  names verbatim, map them to the canonical term at the adapter, and do not spread the external form
  into new first-party names.
- **Distinct meanings stay distinct.** Similar words may be valid terms for different concepts;
  never put a contextual term on a global avoid list or collapse states merely to make names match.
- **Conflicting constraints require an owner decision.** Do not manufacture a universal precedence
  rule when regulation, accessibility, privacy, localization, and a published contract pull in
  different directions.
- **Marketing and landing pages are out of scope.** Different discipline. Do not let that voice migrate into the product.
