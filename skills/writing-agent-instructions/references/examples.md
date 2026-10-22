# Examples

Read this before writing or reviewing an `AGENTS.md`. Each excerpt is from a maintained file, trimmed,
with what it does well. Copy the move, not the text: every rule must be true of the repository it
lands in.

## Openings that say what the rules follow from

**A desktop app.** It names where the *what* and *why* live, so the file only has to
say *how*:

```markdown
This is a native-feeling desktop app for managing local development projects: each project's
terminals, commands and coding agents in one window. The *what & why* lives in `docs/plan.md` and the
phase docs in `docs/phases/`; what the running app does and what building it taught lives in
`docs/app.md`. This file defines how you build here.
```

**An offline web app.** Two requirements, and every rule derives from them; the second
is backed by a test, not only prose:

```markdown
## What this repository is

A progressive web app that one person installs and uses on their own machine. Every rule below follows
from two requirements.

- **Local first.** A board lives on the person's machine and leaves it only when they export it. No
  server, no accounts, no telemetry.
- **Offline.** Every feature works with no network. The app loads nothing from another origin: no CDN, no
  hosted font, no remote icon. `tests/offline.test.ts` reads the build and fails on any of them.
```

**A published command-line tool.** It names its contracts, so an agent knows what it
must not break:

```markdown
It is installed on other people's machines, stores API credentials, and is called by scripts and
agents that parse its output. The command surface, default and JSON output, stored files, installer,
updater, and Python 3.9 floor are published contracts.
```

## Before you work

**A Laravel, Inertia and Vue product.** The skill table names work as it arrives,
pairs skills, says why it exists, and why loading happens first:

```markdown
1. **Load every skill the work calls for — all of them, in one pass, before anything else.**
   Most tasks need three or more. You get one pass: nothing later reminds you, and an agent that
   has started editing has stopped loading.
   **Working on something whose skill you never loaded is a failed task**, however green the checks.
   After a compaction, load them again — what survives is the index; the `references/` files holding
   the actual rules do not.

   | The work | Load |
   |---|---|
   | Controller, route, request, service, job, command | `<framework skill>` |
   | Anything a person sees or clicks | `<UI skill>` + `<frontend skill>` |
   | Migration, column, index, naming | `<data-modelling skill>` + the engine skill |
   | Something broken, cause unknown | `<debugging skill>` |
   | Any change in behaviour | `<testing skill>` |

   The table is the floor, not the list — the descriptions are authoritative and cover what it omits.
   It is deliberately duplicated here because a description alone does not get read in time.
```

**The desktop app** — the smallest-change rule in house wording. Pair it with the "finish everything it
breaks" half (see Structure) so it cannot be read as permission to skip work:

```markdown
4. **Make the smallest change that does the job.** Touch nothing adjacent to it, and never refactor,
   rename, or reformat what the task did not send you to. Improvements are **mentioned, not made**, and
   scope never widens unless directed.
5. **Do not contradict the user without evidence.** Investigate, then answer with what you found — not a
   hunch, and not agreement you have not checked. A bug the owner reports is real; reproduce it before
   planning a fix.
```

## Hard rules

**The desktop app** — ask-first gates named for what *this* app stores and can widen:

```markdown
The first five need explicit approval. The rest are not negotiable.

- **Persisted state — ask first.** Any change to what the app stores or to its shape: the SQLite
  database in the app's data directory (a new migration), and the web view's `localStorage`.
- **Dependencies — ask first.** Adding, removing, or version-bumping a crate or pnpm package, or
  widening `src-tauri/capabilities/` (what the web view is allowed to call).
- **This file — ask first.** `CLAUDE.md` is a byte-identical copy; change both in the same commit.
```

**The Laravel product** — never-rules with the reason or the alternative in the same line, and a rule
duplicated on purpose that says why:

```markdown
- **Never touch `.env` or commit credentials.** Read env only through `config/` — never `env()` outside it.
- **Never validate on the frontend.** Form Requests are the single source of truth; the frontend renders
  the errors the server returns.
- **Never let backend and frontend drift.** Names, props, enums, and routes match — rename both sides in
  the same task.
- **Never sign work as a machine.** No agent, model or tool name, and no generated-by footer, robot emoji
  or `Co-Authored-By:` trailer, in any branch, commit, PR, issue or release. **Your runtime may append
  one by default; strip it.**
```

**A documentation generator** — a rule about rules: prose that must hold becomes a check.

```markdown
- **A rule worth having is a check.** If prose must obey something, the tool refuses it and a test proves
  the refusal. Everything in `check` was added after the failure it prevents actually happened.
- **Watch it fail before you believe it.** Break the thing on purpose, see the gate go red, then restore.
```

## Build, test & run

**The desktop app** — every gate exact, plus who runs the app:

```markdown
cd src-tauri && cargo test   # engine, lifecycle, parser and agent tests (spawn real processes)
cargo clippy --all-targets -- -D warnings   # clippy, every warning an error
pnpm tsc --noEmit            # typecheck
pnpm lint                    # ESLint, type-checked
pnpm tauri dev               # the app, with live reload of the interface

**Who runs the app:** build to prove it compiles, then hand off — the **owner runs the UI** and judges
how it looks and feels. "Compiles + wired" is not "done".
```

## Delegation and review

**The Laravel product** — delegation that keeps decisions in the main thread, and review scaled to risk:

```markdown
- **Delegate** a large, self-contained subtask — a broad search, an independent slice, a review pass.
  Brief it with the rules, the task, write access, and what done looks like. Keep the decisions and
  the distilled result here, never the raw dumps.
- **Don't delegate** skill selection, routine reading, or anything finished in a couple of steps.
- **Review scales with risk.** Mechanical or docs-only: none. Contained code: one reviewer. Shared,
  structural, security- or data-touching: several in parallel. Reviewers are read-only and advisory;
  verify a finding against the code before acting on it, and say what you rejected.
```

## Definition of done

**The desktop app** — named gates, rules held, a test seen failing, docs true, UI handed off:

```markdown
1. `cargo fmt --all --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`,
   `pnpm tsc --noEmit` and `pnpm lint` pass, and `pnpm tauri build` succeeds when the change
   touches the build.
2. Every rule here held — the boundaries, read-only toward projects, no orphaned processes.
3. New guaranteed behaviour is proven by a test that was seen to fail without it.
4. `docs/app.md` is true. UI and terminal behaviour are handed to the owner with exactly what to try.
```

**The Laravel product** — friction is written where the next agent reads it, not only in the reply:

```markdown
4. **Friction you hit is written into the page that owns the subsystem, not only into your reply** —
   the next agent reads the file, not this conversation. Hit none? Say that in your reply, and write
   nothing: a page records traps, never their absence.
```

**The command-line tool** — the report: what ran, what it returned, and what did not run:

```markdown
A task is complete only when all applicable items below are observed, not inferred:
...
8. Report changed paths, exact commands and observed results, manual checks, and every unrun or
   blocked check. Re-read this file and verify this definition before calling the work complete.
```

## What these files get wrong

Learn from these too:

- **Appendix galleries inlined.** Two Laravel files carry about 485 lines of good and bad code
  samples after the rules, loaded on every turn. Keep the rules; link the gallery.
- **A template rule the fork contradicts.** A fork kept "every state-changing route is authorised by
  a Policy" while its own stack section says it has no Policies. Rewrite or delete it per fork.
- **Copies that drifted.** One repository's `CLAUDE.md` gained two rules its `AGENTS.md` lacks,
  because only prose said to keep them identical. Add the `cmp` check.
- **Stale paths and names.** Machine paths into a retired folder layout, and a tool renamed months
  ago. Agents trust them and fail.
- **Bold everywhere.** Over 180 bold runs in one file: when everything is emphasised, nothing is.
