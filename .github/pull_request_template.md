## Summary

<!-- What was wrong or missing, and what is true now. One or two sentences. -->

## Changes

- <!-- One change per bullet, as someone using the skill would notice it — not a file list. Add one bold **Breaking:** or **Risk:** line when it applies; it is required when a skill is removed or renamed, or when a change could stop the package installing. -->

## Testing

- [ ] `./scripts/check.sh`
- [ ] `./tests/run.sh`, including `real_catalog_frontmatter_parses_as_yaml`
- [ ] `git diff --check`
- [ ] Every changed skill was run on a realistic task with and without it and both outputs read, or no skill changed; a new or rewritten skill was benchmarked with `prompts/benchmark-skill.md`, or the gap is stated below.
- [ ] Required GitHub checks pass for the exact head commit.

```text
# Each command run on this exact head, with what it showed.
```

## Repository gates

- [ ] The diff contains no credential, account, real email, real person, client or private project, machine path, or unrelated artifact.
- [ ] Every skill stands alone: it names no other skill and needs no integration, account or service.
- [ ] Every frontmatter holds only `name` and `description`; the description starts `Use when` and contains no `: ` or ` #`.
- [ ] `manifest.json`, each changed skill's `references/sources.md`, its benchmark cases, and `THIRD_PARTY_NOTICES.md` are true in this change.
- [ ] `AGENTS.md` and `CLAUDE.md` still match, or neither changed.
- [ ] No commit, title or body carries machine authorship.

## Release

- Manifest version: `<before>` → `<after>`
- SemVer reason:
- Release after merge: tag only after both gates pass on the merge commit and the package installs through Rundesk from it; sync after tagging and confirm the version (see `AGENTS.md`, Releasing).
