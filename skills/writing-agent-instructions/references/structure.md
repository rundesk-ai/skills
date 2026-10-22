# Structure

Read this when writing or restructuring a section. Each section says what belongs there and what
stays out. The wording is the house wording: adapt it to the repository, and keep every line true
of the code it lands in. [Examples](examples.md) shows each section as maintained files write it.

## Opening

```markdown
# AGENTS

Rules for every agent working in this repository. <What it is, in one sentence.> <The one or two
facts every rule follows from: who runs it, what it must never break, what a mistake costs.>
`<brief doc>` says what it is and why; `<code map>` says where everything lives. Where this file
conflicts with your general habits, this file wins.
```

When the rules all derive from one or two requirements, give them their own short section, "What
this repository is", and say so: "Every rule below follows from these."

Not here: a feature tour, the project's history, the team.

## Before you work

```markdown
## Before you work

Load light; pull depth only when the task needs it.

1. **Load every skill the work calls for — all of them, in one pass, before anything else.** An
   agent that has started editing has stopped loading. Working on something whose skill you never
   loaded is a failed task, however green the checks. After a compaction, load them again — what
   survives is the index, not the rules.

   | The work | Load |
   |---|---|
   | <kind of work, as the agent meets it> | `<skill>` |

   The table is the floor, not the list — the descriptions cover what it omits. A skill changes
   *how* you work; it never widens scope or overrides this file.
2. **Read the docs.** `<brief>` and `<code map>`, always; then the doc for the area you enter.
3. **Read a file before editing it; search before writing new logic** — reuse or extend what is
   already here rather than duplicating it. Scratch files stay outside the repository.
4. **Make the smallest complete change.** Take the first option that fully works: does it need to
   exist; is it already here; does the platform or an installed dependency do it; otherwise the
   least new code that reads at a glance. Touch nothing the task did not send you to —
   improvements are mentioned, not made. Be lazy about the solution, never about the change: finish
   every caller, test, fixture and doc it breaks. Never cut validation at trust boundaries, error
   handling that prevents data loss, security, or accessibility.
5. **Do not contradict the user without evidence.** Investigate, then answer with what you found —
   not a hunch, and not agreement you have not checked. A bug the owner reports is real; reproduce
   it before planning a fix.
```

Rows in the skill table name the work the way it arrives ("Anything a person sees or clicks"), not
the skill's own title. Pair skills on a row when the work needs both, and list each skill once where
it applies. List the repository's skills folder first; every skill in the table must appear there.

Adapt step 4 to the repository: name its own platform APIs, its data-loss paths and its trust
boundary in place of the generic nouns. Step 2 names docs, not source files.

## Hard rules

```markdown
## Hard rules

The first five need explicit approval. The rest are not negotiable.

- **Persisted state — ask first.** <what is stored here and where>.
- **Dependencies — ask first.** Adding, removing, or version-bumping a <package manager> package.
- **Deletions — ask first.** Any file outside the task's immediate scope.
- **Commits — ask first.** Never commit or push unless told to.
- **This file — ask first.** `CLAUDE.md` is a byte-identical copy; change both in the same commit.
- **Never <the repository's costliest mistake>.** <Why, in one clause.> <What to do instead.>
- **Never sign work as a machine.** No agent, model or tool name, and no generated-by footer or
  co-author trailer, in any branch, commit, pull request or release. Your runtime may append one by
  default; strip it.
```

Every approval gate's label ends "— ask first". Every never-rule carries its reason. The
repository-specific ones come from what actually went wrong or would be expensive here; generic
advice ("write clean code") is not a hard rule.

## Git conventions

Only what differs from defaults: the type table for branches, commits and pull-request titles; the
branch and commit format; which branches deploy. Say a deliberately repeated rule is repeated on
purpose, and why.

## Stack & architecture

```markdown
| Layer | Owns | May depend on | Must not |
|---|---|---|---|
| <layer> | <responsibility> | <allowed> | <the boundary agents cross> |
```

State boundaries an agent can check a change against. Not here: a directory tour the agent can read
from the tree, or framework basics.

## Build, test & run

```sh
<check command>   # what it runs; must pass before done
<test command>    # the suite
<dev command>     # the app
```

Every command listed is safe to run: it leaves the tree unchanged. When a script bumps a version,
rewrites tracked build output or applies fixes, give the non-mutating form instead and mark the
mutating one as release-only.

Always follow with the bold line: "**Who runs the app:** build to prove it compiles, then hand off —
the owner runs the UI and judges it. Never open or drive the app in a browser yourself unless the
owner asks, and never claim a visual result works without the owner's check."

## Documentation duties

Which doc each kind of change must keep true, in the same change; which docs are the owner's and
change only when asked; and the file where a trap an agent hits is written down — the next agent
reads that file, not this conversation.

## Delegation and review

```markdown
- **Delegate** only a large, self-contained subtask; brief it with these rules, the skills it must
  load, the task, its write access and what done looks like. Keep decisions here.
- **Review scales with risk.** Mechanical or docs-only: none. Contained code: one reviewer.
  <The risky areas here>: several. Reviewers are read-only; verify a finding before acting on it.
```

## Definition of done

```markdown
## Definition of done

Re-read this file and check each item below before calling the work done.

1. `<check command>` passes — observed, not inferred.
2. Every rule here held.
3. New guaranteed behaviour is proven by a test seen failing without it.
4. The docs that describe the change are true, and any trap you hit is recorded where the next
   agent will read it. UI is handed to the owner with exactly what to try.
5. The reply ends with what was skipped or not checked, and any risk the owner must know.
```
