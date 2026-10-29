---
name: writing-task-tickets
description: Use when writing, rewriting, trimming or scoping a task ticket, user story or epic in a tracker such as Jira or Linear that product people and engineering read to understand what needs doing and why — including turning a stated problem or a technical spec into a ticket, cutting a long or process-heavy one down, or deciding whether one should be split. It supplies a user-story shape written from the user's side, outcome-level pass-or-fail requirements, where technical context for engineering goes, and what to leave out. Do not use for a bug report, a GitHub issue, an implementation plan or build steps, or a full product requirements document.
---

# Writing task tickets

A task says who it is for, what they are trying to do, what gets in their way today, and how
everyone will know it is fixed — readable in about a minute by anyone on the team. It is written
from the user's side, not the system's: engineering plans the build from it, so it carries outcomes,
never a plan. A ticket written as components and guarantees is one the product side cannot check
and the builder did not need.

The **user** is whoever the work is for: a customer, a shopper, a staff member using an internal
tool, a partner, or the person who must make a decision the task produces. Name them as a role.

## The shape

```markdown
**Title:** <what the user can do or get once this ships>

**User story**
As a <user>, I want <what they are trying to do>, so that <why it matters to them>.
<Or, when nobody's experience changes, **Goal** with one sentence saying what is true after.>

**Problem**
<What the user runs into today, and what it costs them and the business. Two sentences at most.>

**Done when**
- <One outcome per line that the user, or someone checking for them, would see>

**Not included:** <What a reader might assume is part of this but is not. Omit when nothing needs saying.>

**Technical notes** (for engineering)
- <A technical fact or constraint, and why it matters. Omit the section when there is none.>
```

- **Title** names what changes for the user: "Shoppers keep their answers when they go back", not
  "Persist form state in session storage".
- **User story** is one sentence in the user's words. The "so that" is their reason, not the
  team's; when only the business benefits, the user is the person who decides or acts on it.
- **Goal** replaces the story when the work changes nothing anyone sees once it goes right — a
  dependency upgrade, a key rotation, a migration, a spike: one sentence saying what is true after.
  A story there reads "As a developer, I want the driver upgraded, so that it is up to date", which
  restates the title. The Title and Problem still speak for whoever is hurt if it is not done.
- **Problem** is two sentences: what happens to the user today, then what it costs — to them, and
  in money, risk, time or customers. A problem with no cost reads as optional. Use a real number
  when one is known; never invent one — write "[cost?]" and ask. Name a group rather than listing
  its members.
- **Done when** is the requirements, each something the user would notice. Read
  [Requirements](references/requirements.md) before writing the list; it holds the rules that make
  each line an outcome that passes or fails.
- **Not included** records limits the person set or the context makes plain — never a choice
  nobody made, which decides the build.
- **Technical notes** are addressed to engineering and kept apart, so the rest stays readable
  outside it. Read [Technical notes](#technical-notes) before adding one.

## Technical notes

Add a note only for a real technical reason — something engineering would otherwise miss, get
wrong, or spend time rediscovering:

- a constraint the outcome fails without: "Staging sends to live partner addresses by default, so
  testing there reaches real partners";
- a compliance, security or data rule that takes a technical form: "Message text must not reach
  analytics or logs";
- what already exists, so engineering sees the gap: "Opt-outs already sync daily; what is missing
  is checking against them";
- a technical fact the person supplied that locates the work: "The domain's DNS is managed in
  Cloudflare".

One sentence each, the reason included, at most four. A note states a fact or a limit, never a
solution, steps, estimates or guarantees the build derives — formats, retries, schemas, test
suites. A technical constraint the user would also notice belongs in **Done when** in their words;
the note says why. With no real reason, there is no section.

## Procedure

1. **Read what you were given:** the request, the conversation, an old task, the project's docs or
   code. Do not ask for what you can already see.
2. **Ask when there is no problem to state.** A request naming only an area and a vague word —
   "better reporting" — states no problem, and research cannot supply one: code shows what exists,
   never what the person finds wrong with it. Ask one to three questions (who it is for, what goes
   wrong for them, what should be true after) and stop without a draft.
3. **Find the user.** A request phrased as a technical change — "fix the DNS records", "add a
   webhook" — still serves someone. Ask what that person sees go wrong, and write from there; keep
   the technical part only as a note with its reason.
4. **Scope it.** One task holds one outcome that can finish on its own; a task carrying two gets
   half-done. A parent over tickets that already exist (an epic) uses the same shape for the
   shared outcome; its children are tracker links, not a list in the body. Propose a split when the material holds unrelated problems, the requirements fall
   into groups serving different users or goals, one part can finish while another waits on a
   decision, or the user story needs "and" to join two wants. Many requirements serving one goal
   is still one task. Propose it even when the person asked for one task — "put it all in one
   ticket" is said before anyone weighs the cost. Write each task in full, lead with one line
   saying why; the person decides.
5. **Write, then cut** every sentence the reader would not miss.
6. **Add the notes** and hand over.

## Notes after the task

Separate from the ticket's **Technical notes**: these are to the person who asked, and never go in
the tracker. Up to four bullets, one sentence each, under a **Notes** heading — and nothing after
them. Each carries something the person must know or decide: a line you added and why, a smaller
first version, a gap to fill, what a rewrite dropped. What already exists is a technical note, not
one of these: the person's notes never reach engineering. Plain words; no nested lists, file paths or
code. Never mention what you did not do or could not file; the person did not ask, and it buries
the notes that matter.

## Wording

- **No people's names.** Name the role or place. Assignment is a tracker field, and a name in the
  body goes stale when the work changes hands.
- **Plain words** for someone outside engineering, everywhere but the technical notes; expand an
  acronym or drop it. Short active sentences, no hedging. Say each thing once.

## Leave out

| Leave out | Because |
|---|---|
| Numbered requirements with matching acceptance criteria | The same points twice; **Done when** is both. |
| History, source documents, versions, meeting timestamps | Link them in the tracker. |
| Evidence lists, rollout, readiness, approval gates | Process the team already follows; **Not included** marks the edge. |
| Dependencies and blockers | The tracker's blocked-by link. |
| Solutions, estimates, technical guarantees — formats, retries, mappings, test suites | The implementation planning derives them from the outcome; a real constraint is a technical note. |

## Check before handing over

- One user and one outcome? If not, propose the split.
- Could someone outside engineering read everything above the technical notes?
- User story names a role and their own reason, or a Goal when nobody's experience changes?
  Problem in two sentences, the second its cost?
- Every **Done when** line new work — an outcome the user would miss, traced to the request or to
  context that requires it, and one two people would agree passed?
- Every technical note carries a reason, and none is a solution or a step?
- Notes four bullets or fewer, one sentence each, and nothing after them?
- Any person's name, or a sentence there for the writer's protection? Remove it.

Read [Examples](references/examples.md) when rewriting a long or technical task or proposing a
split, and [Sources](references/sources.md) when auditing or changing a rule here.
