# AGENTS

This repository is the one source of the skills Rundesk agents load: each skill is a folder under
`skills/`, and `manifest.json` lists them all. Rundesk installs this repository as a package from its
newest release tag and updates every project that has a skill when a new tag lands, so a change here
reaches every project at once. The repository is public: everything committed is published, and
git history keeps it after a later fix.

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
  Rundesk's library, is a copy the next release overwrites; an edit there is lost.
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
skills/<name>/SKILL.md                a skill; a directory is a skill iff it holds this file
skills/<name>/references/*.md         detail the skill links to, read only when the work reaches it
skills/<name>/references/sources.md   the verified evidence behind the skill's rules
skills/<name>/variants/<v>/           overlay files for a deliberate fork; never shipped as a skill
bench/<name>/cases/*.md               benchmark cases, rubric written before the first run
bench/results/<name>/<date>.json      one file per benchmark run
prompts/*.md                          task prompts for catalog work: new skill, benchmark, sources
scripts/check.sh                      the catalog gate
scripts/deploy.sh                     copies skills into a scratch directory for benchmarks only
manifest.json                         schema, name, version, description, and every skill by path
```

- `manifest.json` lists exactly the skills in `skills/`, sorted by name; adding, removing or renaming
  a skill updates it in the same change, and `scripts/check.sh` refuses a mismatch.
- A skill's name is `<verb>-<object>` with a verb from the table in `writing-skills`; its frontmatter
  holds only `name` and `description`, and the description starts `Use when`.
- Adapted material keeps its upstream licence notice in the skill's `references/sources.md` and a
  line in `THIRD_PARTY_NOTICES.md`.

## Build, test & run

```sh
./scripts/check.sh   # names, frontmatter, links, isolation, privacy, manifest, CLAUDE.md copy
./tests/run.sh       # deploy.sh and check.sh against fixtures and the real catalog
```

Both write only to a temporary directory. Benchmark a skill with `prompts/benchmark-skill.md`, in
scratch directories outside any git checkout; `scripts/deploy.sh` refuses a checkout.

## Releasing

Releasing is the owner's call. The version in `manifest.json` follows semver: a removed or renamed
skill is major, a new skill minor, a change to an existing skill patch. Bump it in the pull request,
merge, then tag `vX.Y.Z` on the merge commit. Rundesk installs the newest tag and ignores untagged
commits, so nothing reaches a project until the tag exists.

## Definition of done

Re-read this file and check each item below before calling the work done.

1. `./scripts/check.sh` and `./tests/run.sh` passed, observed in this session.
2. A changed skill was run on a realistic task with and without it, and both outputs read; a new or
   rewritten one was benchmarked with `prompts/benchmark-skill.md` and its result recorded.
3. `manifest.json`, `references/sources.md` and `THIRD_PARTY_NOTICES.md` are true in the same change.
4. The full diff was read for anything personal or secret.
5. The reply names what was skipped or not checked, and any risk the owner must know.
