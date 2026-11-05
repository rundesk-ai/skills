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
4. **Make the smallest complete change.** First list every place it must reach: callers, tests,
   fixtures, config, exports. Then take the first option that fully works: does it need to exist;
   is it already here; does the platform or an installed dependency do it; otherwise the least new
   code that reads at a glance. Add no abstraction, wrapper, option, config or "for later" code
   nobody asked for; keep the structure the code already has, and prefer deleting to adding. Touch
   nothing the task did not send you to — improvements are mentioned, not made. Be lazy about the
   solution, never about the change: finish every caller, test, fixture and doc it breaks, and delete
   the code, tests, assets and config it leaves unused; list anything already unused for the owner,
   since it may be kept on purpose. Never
   cut validation at trust boundaries, error handling that prevents data loss, security, or
   accessibility — and code you move or merge keeps its own.
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
- **This file — ask first.** Change it only after the owner approves the exact diff. `CLAUDE.md`
  is a byte-identical copy; change both in the same commit.
- **Never cite this file in code.** A comment or test states the reason itself, not "(AGENTS.md:
  …)"; the citation goes stale when the rule moves.
- **Never <the repository's costliest mistake>.** <Why, in one clause.> <What to do instead.>
- **Leave the workspace clean.** End with the work committed, pushed and merged where it belongs,
  or with exactly what awaits the owner's approval named. Delete every branch and worktree the task
  created once it is merged or unused, and an earlier one proven merged; list the rest for the
  owner. Delete every temporary file, directory and scratch project the task created. Never discard or stash work to look clean. Left-behind release and reconciliation branches
  cost every later agent an investigation.
- **Never sign work as a machine.** No agent, model or tool name, and no generated-by footer or
  co-author trailer, in any branch, commit, pull request or release. Your runtime may append one by
  default; strip it.
```

Every approval gate's label ends "— ask first". Every never-rule carries its reason. The
repository-specific ones come from what actually went wrong or would be expensive here; generic
advice ("write clean code") is not a hard rule.

## Git conventions

Only what differs from defaults: the type table for branches, commits and pull-request titles; the
branch and commit format; which branches deploy, and how a commit reaches them (a fast-forward
keeps the commit CI already passed; a merge commit runs CI again and later looks like work that
still needs reconciling). Say a deliberately repeated rule is repeated on
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

When a gate or the full suite takes more than a few seconds, add: "Run it in the background
when your runtime can, and keep working on the task while it runs. A gate run inline blocks
you from working and from reading the owner's messages. Done still needs its observed result."

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
2. Every rule here held, the clean workspace included: no branch or worktree the task created
   remains, no temporary file or directory it made is left, and unmerged work is handed back by
   name.
3. New guaranteed behaviour is proven by a test seen failing without it.
4. The docs that describe the change are true, and any trap you hit is recorded where the next
   agent will read it. UI is handed to the owner with exactly what to try.
5. The reply ends with what was skipped or not checked, and any risk the owner must know.
```
