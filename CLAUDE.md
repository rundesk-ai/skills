# CLAUDE

This repository is a public catalog of skills for any coding agent: each skill is a folder under
`skills/<group>/`, and `manifest.json` lists them all by path. The manifest is the format the
Rundesk app and the Rundesk CLI install from: they take the newest release tag and update every
project that has a skill when a new tag lands, so a change here reaches every project at once. The
repository is public: everything committed is published, and git history keeps it after a later fix.

`CLAUDE.md` is a byte-identical copy of this file except for its first line; `scripts/check.sh`
fails when they drift.

## Before you work

1. **Load the skills the work needs**, in one pass, before editing. The table is the floor, not the
   list; load them again after a compaction. When one is not installed in this session, read its
   `SKILL.md` under `skills/` directly.

   | The work | Load |
   |---|---|
   | Creating, editing, splitting, reviewing or benchmarking a skill | `writing-skills` |
   | Python in `scripts/check.sh` | `using-python` |
   | A test in `tests/run.sh` | `testing-code` |

2. **Read before you write.** Read `README.md`, then every file of the skill you are changing,
   `references/sources.md` included. Before adding a skill, read the descriptions of every skill in
   `manifest.json`, and the bodies of the close ones: extend the skill that already owns the work
   rather than adding a neighbour that splits its trigger.
3. **Make the smallest complete change.** Take the first option that fully works: does the guidance
   need to exist; does a skill here already say it; does the agent already do it unaided; otherwise
   the fewest words that change what the agent does. Touch nothing the task did not send you to;
   improvements are mentioned, not made. Be lazy about the wording, never about the change: update
   `manifest.json`, the skill's `references/sources.md`, its benchmark cases and any reference link
   the change breaks. Never cut a safety rule, a data-loss guard, a security or accessibility rule,
   or a trap a skill teaches.
4. **Do not contradict the owner without evidence.** Investigate, then answer with what you found.
   A skill the owner says misbehaves is reproduced in a run before it is changed.

## Hard rules

- **Every skill stands alone.** A skill names no other skill, assumes no other skill is installed,
  and needs no integration to work: no MCP server, API key, account, sign-in or service. A tool it
  can use when present is optional, described by what it does, and the skill still works without
  it. A project installs any subset of this catalog, and a dependency missing there fails silently.
  `scripts/check.sh` refuses a skill that names another skill or an MCP tool (`mcp__…`).
- **Nothing personal or secret, anywhere.** No credential, account, account ID, endpoint, real email
  address, private repository, or the name of a real person, client or private project, in a skill,
  a benchmark case or result, a prompt, or a commit message. Examples use reserved or invented
  names (`example.com`, `shop.example`, a fictional company). Published content cannot be recalled;
  `scripts/check.sh` catches credentials, real emails and machine paths, and you inspect the full
  diff for the rest before every commit.
- **No machine path, repository or setup in a skill.** A skill is copied into every project that has
  it, and a path or repository named in it points nowhere there. Describe the work instead ("the
  stack's own guidance").
- **Change a skill only here.** A skill in a project's `.agents/skills` or `.claude/skills`, or in
  an installed package, is a copy the next release overwrites; an edit there is lost.
- **Ask first** before deleting or renaming a skill (it disappears from every project that has it at
  the next release), adding a script or executable to a skill, changing a version, tag or release,
  or editing this file.
- **Never edit a skill in the same run as its benchmark.** A skill tuned against the cases it was
  measured on handles those cases and nothing else; measure, report, then change it.

## Git conventions

- Commit and push only when asked. Work on a branch and open a pull request to `main`; CI runs both
  gates on every push. Merging and releasing happen only when the owner says so.
- No commit, branch, pull request or release carries machine authorship: no co-author line, no
  "generated with", no agent sign-off.

## Layout

```text
skills/<group>/<name>/SKILL.md        a skill; a directory is a skill iff it holds this file
skills/<group>/<name>/references/     detail the skill links to, read only when the work reaches it
  references/sources.md               the verified evidence behind the skill's rules
skills/<group>/<name>/variants/<v>/   overlay files for a deliberate fork; never shipped as a skill
subagents/<name>.md                   a subagent, in the Rundesk subagent library's format
bench/<name>/cases/*.md               benchmark cases, rubric written before the first run
bench/results/<name>/<date>.json      one file per benchmark run
prompts/*.md                          task prompts for catalog work: new skill, benchmark, sources
scripts/check.sh                      the catalog gate
scripts/deploy.sh                     copies skills into a scratch directory for benchmarks only
scripts/bench-status.sh               which skills a benchmark is due for, and which are current
manifest.json                         schema, name, version, description, every skill and subagent by path
```

- The groups are `development`, `writing`, `design`, `research`, `marketing`, `stacks`, `games`
  and `media`. Every skill sits in exactly one, and a name is unique across all of them: projects get
  skills flat by name, so the group exists only here. Move a skill between groups with `git mv`,
  keeping its name.
- `manifest.json` lists exactly the skills in `skills/`, by name and path, sorted by name; adding,
  removing, renaming or moving a skill updates it in the same change, and `scripts/check.sh` refuses
  a mismatch. Its `subagents` list does the same for `subagents/`.
- A subagent is one file: frontmatter `name` (its file name), a `description` starting `Use when`,
  and optionally one block of settings per agent CLI (`claude`, `codex`, `grok`, …); the body is its
  instructions. Rundesk writes it into every agent CLI on the machine, so it stands alone as a skill
  does, and the same privacy rules apply.
- A skill's name starts with its group's prefix, listed in `skills/groups.txt`; development keeps
  one verb per activity. Its frontmatter holds only `name` and `description`, and the description
  starts `Use when`.
- Adapted material keeps its upstream licence notice in the skill's `references/sources.md` and a
  line in `THIRD_PARTY_NOTICES.md`.

## Build, test & run

```sh
./scripts/check.sh   # groups, names, frontmatter, links, isolation, privacy, manifest, CLAUDE.md copy
./tests/run.sh       # deploy.sh, check.sh and bench-status.sh against fixtures and the catalog
```

Both write only to a temporary directory. Benchmark a skill with `prompts/benchmark-skill.md`, in
scratch directories outside any git checkout; `scripts/deploy.sh` refuses a checkout.
`./scripts/bench-status.sh --due` lists the skills a benchmark is due for; one whose last result
measured its current files is not run again.

## Releasing

Releasing is the owner's call. The version in `manifest.json` follows semver: a removed or renamed
skill is major, a new skill minor, a change to an existing skill patch. Bump it in the pull request,
merge, then tag `vX.Y.Z` on the merge commit. Installers take the newest tag and ignore untagged
commits, so nothing reaches a project until the tag exists.

## Definition of done

Re-read this file and check each item below before calling the work done.

1. `./scripts/check.sh` and `./tests/run.sh` passed, observed in this session.
2. A changed skill was run on a realistic task with and without it, and both outputs read; a new or
   rewritten one was benchmarked with `prompts/benchmark-skill.md` and its result recorded.
3. `manifest.json`, `references/sources.md` and `THIRD_PARTY_NOTICES.md` are true in the same change.
4. The full diff was read for anything personal or secret.
5. The reply names what was skipped or not checked, and any risk the owner must know.
