---
name: writing-agent-instructions
description: Use when writing, restructuring, reviewing, or trimming a repository's AGENTS.md and its CLAUDE.md copy, including setting up agents for a new repository, adding a rule so agents stop doing something, adapting a template's rules to a fork, two copies that drifted apart, rules agents keep ignoring, or a file grown too long. It supplies the house section order, how to write a rule an agent follows, the smallest-complete-change rule every file carries, and the checks that prove the file works. Do not use for documentation written for people or for a skill's own instructions.
---

# Writing agent instructions

`AGENTS.md` is the operating instructions for every agent that works in a repository. Every line is
a deliberate decision about behaviour — inherited, pasted or generic lines are the ones agents follow
wrongly.

It is loaded into every session before the agent knows what it will be asked, so every line is paid
for on every turn, adherence falls as the file grows, and when two lines disagree the agent may
follow either. A good one is specific to its repository and written so an agent that reads it once
works the way the owner would: the least new code, and nothing left unfinished.

The file governs every agent that works in the repository, so change it only when asked to, and show
the owner the diff.

## 1. Read the models, then the repository

Read [Examples](references/examples.md) before writing: excerpts from maintained files, each with
why it works. Match their voice and depth. Then read the repository itself — the manifests, the
commands that really exist, the docs, the history of what went wrong — because every rule must be
true of this code. A rule the code disproves teaches the agent to ignore the file.

**Search the tests and CI for the file's name first.** Some repositories test the rules file itself:
pinned headings, a heading order shared with sibling repositories, the copy check. Keep whatever is
pinned exactly — map each section below into the existing heading — and never rename a pinned one.

**When rewriting an existing file, inventory it first.** List every rule in the old file, verify each
against the code, and mark it keep, merge, fix or drop. A rule is dropped only when it is false,
derivable from the code, or stated in the new file in substance. A nearby house rule does not count:
"re-read this file before calling it done" or "establish the outcome and its proof" survive unless
the new wording says the same thing. Request every link (`curl -I` or `gh api`); a 404 is fixed, and
every other file carrying the same stale link is named in your reply. A skill the old file names that
is installed nowhere is reported, not carried over.

**Report what the code already breaks.** When a rule you write is broken in the code today — an
active local endpoint, a component crossing a stated boundary — say so in your reply. Writing the
rule does not fix the code, and the owner needs to know.

## 2. Keep the pair identical

`AGENTS.md` is the file. `CLAUDE.md` is a byte-identical copy of it, because Claude Code reads
`CLAUDE.md` and the other agent CLIs read `AGENTS.md`.

- Write and edit `AGENTS.md`, then copy it over `CLAUDE.md` in the same change. Never edit
  `CLAUDE.md` on its own.
- State the pairing in the file itself, under the hard rule about editing it: "`CLAUDE.md` is a
  byte-identical copy; change both in the same commit."
- Back it with a check. Look for one first — a test that already compares the files. Add a new one
  only where none exists, as its own gate, not chained onto an unrelated command. A written rule
  without a check is how copies drift.
- Prove it before finishing: `cmp AGENTS.md CLAUDE.md` prints nothing.

## 3. Write the sections in this order

Read [Structure](references/structure.md) for what each section holds and what stays out of it.
The order follows a task from start to finish:

1. **Opening** — `# AGENTS`, then what the repository is and the one or two facts every rule follows
   from: who runs it, what it must never break, what a mistake costs. Name the always-read docs.
2. **Before you work** — numbered, in the order the agent acts:
   1. Load every skill the work needs, in one pass, before editing, from a "The work | Load" table;
      the table is the floor, not the list; load them again after a compaction. List the
      repository's skills folder first: every skill in the table must appear there. A skill
      installed for the user rather than the repository gets no row.
   2. Read the always-read docs, then the area doc when the task enters that area.
   3. Read a file before editing it; search before writing new logic.
   4. Make the smallest complete change — step 4 below.
   5. Do not contradict the user without evidence: investigate, then answer with what you found. A
      bug the owner reports is real; reproduce it before planning a fix.
3. **Hard rules** — the ask-first gates (persisted state, dependencies, deletions, commits, this
   file), then the never-do rules. Each with its reason.
4. **Git conventions** — only what differs from defaults, including whether agents commit at all
   and that no machine authorship appears anywhere.
5. **Stack & architecture** — boundaries as what each part owns and must not do. Grep each "must
   not" against the code: if the code already breaks it, write "new code must not…" and name the
   existing exceptions, or drop the row. A table that describes intent as fact teaches agents the
   code is wrong.
6. **Build, test & run** — exact commands, each one safe to run: it leaves the tree unchanged. Read
   each script for side effects (a version bump, a write to tracked build output, an auto-fix) and
   give the non-mutating form, in the form that shows the evidence done requires — a `--quiet` lint
   cannot prove "no new warnings". A gate is one line; if a safe form needs a script, propose the
   script to the owner instead of pasting a shell block into the rules. Run the safe form once in a
   scratch copy and compare `git status` before and after: write what you observed, not what you
   fear. Then the bold **Who runs the app** line: agents build to prove it compiles and hand off;
   the owner runs the UI, and an agent never verifies it in a browser itself unless the owner says
   so.
7. **Documentation duties** — which doc a change must keep true, in the same change, and the file
   where a trap an agent hits is recorded, so the next agent reads it.
8. **Delegation and review** — when the repository uses other agents; review scaled to risk.
9. **Definition of done** — last, numbered, observed evidence.

Omit a section with nothing specific to say. Worked galleries of good and bad code go in a linked
file, not an appendix: they are the bulk of every oversized rules file.

## 4. Build in the smallest complete change

Agents over-build: options nobody asked for, wrappers, a new helper beside an existing one. They also
under-finish: a fixed function with its callers left broken. Every file carries one rule in Before
you work that holds both lines, in five parts:

1. List every place the change must reach — callers, tests, fixtures, config, exports — then take
   the first option that fully works (the ladder).
2. Add no abstraction, wrapper, option, config or "for later" code nobody asked for; keep the
   structure the code already has, and prefer deleting to adding. This is the part that cuts code:
   a ladder alone stops at "the least new code", and an agent counts a wrapper or an option as part
   of the least.
3. Touch nothing the task did not send you to.
4. Be lazy about the solution, never about the change: finish what it breaks, and delete what it
   leaves unused — code, tests, assets, config — listing anything already unused for the owner.
5. Never cut validation, data-loss guards, security, accessibility, or anything the user asked for
   — and code moved or merged keeps its own.
[Structure](references/structure.md) has the house wording to start from.

Keep all five parts, and adapt every generic noun to this repository: its platform APIs instead of
"the standard library", its actual trust boundary, and its data-loss guards by their literal value or
symbol — `0700` directory, `0600` file, the lock file, the conflict error's name, the migration
constant — so a later rewrite keeps them checkable. A clause copied unchanged is an unadapted
rule.

## 5. Write each rule so an agent follows it

- **Make it checkable.** Name the command, path, value or pattern. "Run `pnpm check` before
  claiming done" is a rule; "keep quality high" is not.
- **Give the reason in one clause**, or the failure it prevents. An agent given a bare imperative
  applies it literally and nowhere else.
- **Say what to do instead** when forbidding something.
- **Label, rule, reason.** Each hard rule opens with a bold label of two to five words, then the
  rule, then its reason in one clause — three lines at most. Bold the label, not the sentences; if
  everything is bold, nothing is. No capitals for emphasis — current models overreact to shouting.
- **Put the costliest mistakes first.** Agents weight earlier instructions more.
- **Add a rule after a real mistake**, and say what it prevents.
- **When a rule is duplicated on purpose**, say so and why, so nobody "cleans it up".

## 6. Keep out what does not need to be there

- **Anything the agent can learn from the code**: file-by-file tours, standard conventions,
  framework basics, the rules a linter already enforces.
- **Procedures and long examples**: a multi-step workflow is a skill; a gallery is a linked file.
- **Machine paths, retired tool names and facts that change often**, including counts of warnings,
  tests or files. They go stale silently and the agent trusts them. State the rule instead: "add no
  new warnings in the lines you change".
- **A template's rules that do not fit the fork.** Delete or rewrite each one the fork's stack
  contradicts.

Anything that must happen every time, with no judgment, belongs in a check, not only in prose. A
rule worth having is a check where one can be written.

## 7. Make "done" observable

The definition of done opens with "Re-read this file and check each item below before calling the
work done", then lists the evidence a finished task leaves: the named gates that passed,
observed and not inferred; the test seen failing before the fix; the docs updated in the same
change; UI handed to the owner with exactly what to look at. Name the gates rather than repeating
their commands, and keep it to about five items. It ends with the report rule: the reply names what
was skipped or not checked, and any risk the owner must know.

When a deliberate shortcut is taken, the rules can ask for it to be marked where it lives — a comment
such as `shortcut: <the limit>, <when to revisit>` — so a reviewer reads it as a decision, and the
debt can be found by searching.

## 8. Prove the file works

1. **Count it.** About 120 to 250 lines of rules is the working range; past that, move detail out
   rather than cutting rules that prevent real mistakes. Prefer short sentences to qualified ones:
   a rule an agent has to parse twice is followed once.
2. **Cut-test every line:** would removing it cause a mistake here? If not, remove it.
3. **Verify every claim** — each path and named mechanism exists in the code; each command is
   confirmed by reading its script, and run only in a scratch copy or when it writes nothing.
4. **No line contradicts another**, and none contradicts the code.
5. **The pair is identical:** `cmp AGENTS.md CLAUDE.md` prints nothing.
6. **Watch behaviour.** Give an agent a realistic task in a fresh session and read what it did.

Read [Sources](references/sources.md) when a rule here is questioned or changed: it holds the
evidence behind the length, emphasis and ordering advice.

## Traps

- **The copies drift.** Symptom: `CLAUDE.md` differs from `AGENTS.md` in one rule. Cause: an edit
  reached only one file. Fix: copy `AGENTS.md` over `CLAUDE.md`, and add the `cmp` check. Proof: the
  check fails when one file is edited alone.
- **The file grew into a manual.** Symptom: hundreds of lines, rules ignored at random. Cause:
  galleries, tours and procedures inlined. Fix: move them to linked files, keep the rules. Proof: the
  line count, and a fresh session that follows the rules.
- **Inherited rules contradict the code.** Symptom: a fork's file names a mechanism the code does not
  use. Cause: a template's rules copied without checking them against the fork. Fix: rewrite or
  delete each rule the stack disproves. Proof: every rule names something that exists.
- **The smallest-change rule read as permission to skip work.** Symptom: a small diff that leaves
  callers or tests broken. Cause: the ladder kept without its "never lazy about the change" half.
  Fix: keep both halves in one rule. Proof: the rule in the file names callers, tests and docs.
- **Finishing read as fixing only what breaks.** Symptom: review rounds keep finding helpers, tests,
  assets and config whose only caller an earlier change removed. Cause: "finish the change" covers
  what fails to compile, and an orphan compiles. Fix: step 4 says to delete what the change leaves
  unused. Proof: the rule in the file names it.
- **The ladder kept without what not to add.** Symptom: agents still add a helper, option or wrapper
  layer and call it the least new code. Cause: step 4 condensed to the ladder, its "add no
  abstraction, wrapper, option, config or 'for later' code" sentence dropped. Fix: keep that
  sentence in step 4, naming this repository's own usual over-builds. Proof: the rule names them.
