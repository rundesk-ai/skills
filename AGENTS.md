# AGENTS

This repository is a public catalog of skills for any coding agent: each skill is a folder under
`skills/<group>/`, and `manifest.json` lists them all by path. The Rundesk app and the Rundesk CLI
(the installers) install the catalog from the manifest as one skill package: they take the newest
release tag and update every project that has a skill when a new tag lands, so a change here reaches
every project at once. The repository is public: everything committed is published, and git history
keeps it after a later fix.

## Before you work

1. **Load the skills the work needs**, in one pass, before editing; an agent that has started
   editing has stopped loading. The table is the floor, not the list; load them again after a
   compaction. When one is not installed in this session, read its `SKILL.md` under `skills/`
   directly.

   | The work | Load |
   |---|---|
   | Creating, editing, splitting, reviewing or benchmarking a skill | `writing-skills` |
   | `AGENTS.md` and its `CLAUDE.md` copy | `writing-agent-instructions` |
   | `README.md`, a pull-request body or release notes | `writing-prose` |
   | A pull request, tag or release | `managing-github` |
   | Python in `scripts/check.sh` | `using-python` |
   | A test in `tests/run.sh` | `testing-code` |

2. **Read before you write.** Read `README.md`, then every file of the skill you are changing,
   `references/sources.md` included. Before adding a skill, read the descriptions of every skill in
   `manifest.json`, and the bodies of the close ones: extend the skill that already owns the work
   rather than adding a neighbour that splits its trigger.
3. **Make the smallest complete change.** First list every place it must reach: `manifest.json`,
   the skill's `references/sources.md`, its benchmark cases, `THIRD_PARTY_NOTICES.md`, the catalog
   lists and counts in `README.md`, and any reference link the change breaks. Then take the first
   option that fully works: does the guidance need to exist; does a skill here already say it; does
   the agent already do it unaided; otherwise the fewest words that change what the agent does. Add
   no section, reference file, example or script nobody asked for. Touch nothing the task did not
   send you to; improvements are mentioned, not made. Be lazy about the wording, never about the
   change: finish every place on the list, and delete what the change leaves unused, such as a
   reference no link reaches or a case for a rule that is gone. Never cut a safety rule, a data-loss
   guard, a security or accessibility rule, or a trap a skill teaches.
4. **Do not contradict the owner without evidence.** Investigate, then answer with what you found.
   When the owner says a skill misbehaves, reproduce it in a run before changing it.

## Hard rules

The first three need the owner's approval. The rest are not negotiable.

- **Deleting or renaming a skill — ask first.** It disappears from every project that has it at the
  next release.
- **A script or executable in a skill, or a version, tag or release — ask first.** Releasing is the
  owner's call, and a tag reaches every project at once.
- **This file — ask first.** `CLAUDE.md` is a byte-identical copy except for its first line
  (`# CLAUDE`); regenerate it with `sed '1s/AGENTS/CLAUDE/' AGENTS.md > CLAUDE.md` in the same
  change. `scripts/check.sh` fails when they drift.
- **Nothing personal or secret, anywhere.** No credential, account, account ID, endpoint, real email
  address, private repository, or the name of a real person, client or private project, in a skill,
  a benchmark case or result, a prompt, or a commit message. Examples use reserved or invented
  names (`example.com`, `shop.example`, a fictional company). Published content cannot be recalled;
  `scripts/check.sh` catches credentials, real emails and machine paths, and you inspect the full
  diff for the rest before every commit.
- **Every skill stands alone.** A skill names no other skill, assumes no other skill is installed,
  and needs no integration to work: no MCP server, API key, account, sign-in or service. A tool it
  can use when present is optional, described by what it does, and the skill still works without
  it. A project installs any subset of this catalog, and a dependency missing there fails silently.
  `scripts/check.sh` refuses a skill that names another skill or an MCP tool (`mcp__…`).
- **No machine path, repository or setup in a skill.** A skill is copied into every project that has
  it, and a path or repository named in it points nowhere there. Describe the work instead ("the
  stack's own guidance").
- **Change a skill only here.** A skill in a project's `.agents/skills` or `.claude/skills`, or in
  an installed package, is a copy the next release overwrites; an edit there is lost.
- **Never edit a skill in the same run as its benchmark.** A skill tuned against the cases it was
  measured on handles those cases and nothing else; measure, report, then change it.
- **Leave the checkout clean.** Scratch files and benchmark runs go outside the repository, and you
  delete every branch, worktree and temporary file the task created; list anything else left
  behind for the owner. Never discard or stash work to look clean. A stray file in a public
  repository is one `git add` from being published.

## Git conventions

- Commit and push only when asked. Work on a branch and open a pull request to `main`; CI runs both
  gates on every push. Merging and releasing happen only when the owner says so.
- No commit, branch, pull request or release carries machine authorship: no co-author line, no
  "generated with", no agent sign-off. Your runtime may append one by default; strip it.

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
  one verb per activity, because there the verb is what tells two skills apart.
- A skill's frontmatter holds only `name` and `description`, and the description starts `Use when`
  and contains no `: ` and no ` #`: the installers read frontmatter as strict YAML, where an
  unquoted `: ` is a nested mapping and ` #` starts a comment. Write "It supplies a workflow for …"
  or use a comma, as the other skills do.
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
merge, then tag `vX.Y.Z` on the merge commit. The installers take the newest tag and ignore untagged
commits, so nothing reaches a project until the tag exists.

Tag only a commit the installers accept. One invalid file makes Rundesk reject the whole package, so
every project stops updating at once (v1.3.0 did this with one unquoted `: `):

1. On the merge commit, `./scripts/check.sh` and `./tests/run.sh` pass; `tests/run.sh` parses every
   frontmatter with a real YAML parser.
2. Before tagging, the package installs through Rundesk from that commit: add
   `https://github.com/rundesk-ai/skills/tree/main` as a skill package (Rundesk's
   `skill_package_add`, or Settings), confirm every skill in `manifest.json` is listed, then remove
   that package.
3. After tagging, sync the package (Rundesk's `skill_package_sync` for `rundesk-ai/skills`) and
   confirm it reports the new tag and version with nothing dropped. This is how v1.3.1 was verified.

## Definition of done

Re-read this file and check each item below before calling the work done.

1. `./scripts/check.sh` and `./tests/run.sh` passed, observed in this session.
2. A changed skill was run on a realistic task with and without it, and both outputs read; a new or
   rewritten one was benchmarked with `prompts/benchmark-skill.md` and its result recorded.
3. `manifest.json`, `references/sources.md`, `THIRD_PARTY_NOTICES.md` and the catalog lists and
   counts in `README.md` are true in the same change.
4. The full diff was read for anything personal or secret, and no scratch file, branch or worktree
   the task created is left behind.
5. The reply names what was skipped or not checked, and any risk the owner must know.
