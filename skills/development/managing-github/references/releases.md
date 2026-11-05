# GitHub releases

## Discover the release contract

Read applicable repository instructions, `CONTRIBUTING.md`, `RELEASING.md`, changelog, version files,
release workflows, and `.github/release.yml`. Determine the release branch, version source,
validation, artifacts, notes policy, and whether pushing a tag creates the GitHub Release. When
automation owns creation, use it; never also run `gh release create`.

Fetch the release branch and tags, then inspect existing releases:

```sh
git fetch <release-remote> <release-branch> --tags
gh release list --repo <owner/repo> --limit 20
```

Stop if the worktree is dirty, required content is not merged and pushed, validation is incomplete,
or the release branch, commit, repository, account, remote, tag owner, or automation is uncertain.

## Continue directly from a verified merge

When the same outcome already passed exact-head review and CI, was merged through the authorized
pull-request path, and has release authority, carry that evidence forward. First verify the stored
merge result and the exact merge commit's required default-branch workflow. That workflow is new
evidence for the integrated commit; previous exact-head validation remains evidence for the unchanged
pull-request content and is not work to repeat.

Do not reopen implementation, delegate another review, rebuild the development plan, or rerun the
previous exact-head validation merely because release execution has begun. Use one bounded wait
mechanism for each required post-merge, release, or deployment workflow rather than repeatedly
polling it, in the background when the runtime allows, so the wait does not block other work or
the owner's messages. Then do only the release contract's remaining work: select and confirm the version and
tag, publish through the repository's automation or documented manual path, verify stored release
state and artifacts, exercise the required production check, and reconcile a deployment branch only
when the repository requires it.

If the default-branch workflow fails, the release range or tag is uncertain, authorization does not
cover the exact release, or deployment needs corrective work, report the release blocker and stop.
Do not turn release administration into an implementation cycle without authority for that work.

## Run CI once per content

Checks attach to a commit, so moving the commit that already passed carries its evidence, and
every new commit starts CI again, even one with no new content. Promote that commit itself:

- Promote to a production or release branch by fast-forward when the repository allows it, so
  the branch tip becomes the commit that already passed. A merge commit is a new commit: it runs CI
  again, and it leaves a commit on that branch that later looks like unreconciled work.
- Do not update a pull-request branch from its base, rebase it, add an empty commit, or rerun a
  workflow when that pull request's content has not changed and its required checks already passed
  on its current head. Do it only when branch protection requires an up-to-date head or a check
  failed for reasons outside the code.
- When a new pull request's head is a commit that already passed, as when promoting `main` to
  `production` in a pull request, a workflow triggered by pull-request events may still run
  again. That comes from the workflow's configuration. Report it to the owner and propose a
  fix rather than editing the workflow or bypassing a required check.

Before waiting on CI for a promotion, compare its head with the commit that already passed:
`git rev-parse <head>^{tree} <passed-commit>^{tree}`. Equal trees mean the content is identical,
so a failure there comes from the branch, event, or environment, not the code. Report it that way.

A release-only version commit or pull request is new content and must pass its own required gates.

## Classify the branch before reconciling it

Determine purpose from repository instructions and deployment workflows, never the branch name
alone:

- A live website deployment branch represents code deployed to production. Its canonical
  integration branch is the repository's documented default, often `main`.
- An isolated product-version branch exists to build or support a specific release line.

For a live deployment branch, post-production reconciliation is part of release completion when the
repository contract requires it. After production verification, fetch both branches and list what
the deployment branch holds that the canonical branch does not:

```sh
git fetch <remote> <canonical> <deploy>
git diff <remote>/<canonical>...<remote>/<deploy>
```

Empty output means there is nothing to reconcile, even when promotion left a merge commit on the
deployment branch. Open no reconciliation branch or pull request for a commit that carries no
content. Otherwise return only that deployment-only content through the required pull-request,
review, and check path, on one reconciliation branch for the release. Do not merge the canonical branch into the deployment branch
and call that reconciliation. Prove the deployed commit is reachable from the updated canonical
branch; under squash or rebase policy, instead prove no deployment-only content remains.

Do not automatically apply that back-merge rule to an isolated product-version branch. Follow its
documented merge-forward or maintenance policy.

If authority does not include the required pull request or merge, prepare the authorized artifacts
and report reconciliation as an explicit remaining delivery step.

## Choose an exact version

Inspect all changes since the last published release. Follow the repository's established version,
tag, title, and prerelease scheme. Do not replace Calendar Versioning, a product prefix, an absent
`v`, or another published convention with SemVer merely for consistency.

When no version policy or established pattern exists, use stable SemVer with a `v`-prefixed tag:

| Bump | Fallback meaning |
|---|---|
| Patch | Backward-compatible fixes, documentation corrections, or internal changes with no new public capability. |
| Minor | Backward-compatible public functionality or deprecation. |
| Major | Any incompatible API, CLI, schema, configuration, data, or behavior change. |

Reset lower components after a minor or major increment. One breaking change makes the fallback
release major. For `v0.Y.Z`, use minor for incompatible change or new capability and patch for a
compatible correction. Use `v1.0.0` only when the project deliberately declares its contract stable.

Confirm the proposed tag does not exist and resolves inside the intended release line.

## Prepare and authorize the release

Update every required version source, changelog, generated artifact, migration note, and
compatibility instruction. Run complete release validation, wait for required CI on the exact
commit, inspect the release range, and record artifact digests when required.

Before a push, tag, draft, upload, or publication, present:

- repository, account, release branch, previous release, and comparison range;
- exact version, tag, title, target commit, and compatibility rationale;
- validation, CI, release automation, notes source, artifacts, and checksums; and
- each failed check, uncertainty, recovery requirement, or remaining reconciliation step.

Authorization must cover that exact repository, version, commit, and effect.

## Tag and prepare notes

Follow the repository's annotated, signed, lightweight, or automation-owned tag contract. When no
contract exists, create an annotated tag on the recorded commit and push only that tag:

```sh
tag=<approved-tag>
release_commit=$(git rev-parse <approved-release-commit>)
git tag -a "$tag" "$release_commit" -m "$tag"
git push <release-remote> "refs/tags/$tag"
```

If automation owns the release, monitor it and continue at verification. Otherwise create a draft
from the already pushed tag:

```sh
gh release create "$tag" --repo <owner/repo> \
  --draft \
  --verify-tag \
  --generate-notes \
  --fail-on-no-commits \
  --title '<approved title>'
```

Add `--prerelease` when approved. Add `--notes-start-tag <previous-tag>` when GitHub would compare the
wrong release line. Inspect the draft and correct missing breaking changes, migrations, security
instructions, or misleading summaries through a reviewed notes file:

```sh
gh release view "$tag" --repo <owner/repo> \
  --json url,name,tagName,targetCommitish,body,isDraft,isPrerelease,assets
gh release edit "$tag" --repo <owner/repo> \
  --notes-file <reviewed-release-notes.md>
```

Attach required artifacts and checksums before publication. Never use `--clobber` without explicit
approval and proof that replacing the draft asset is recoverable.

## Publish, verify, and recover

Publish only after the tag target, draft, notes, and assets match the approved release:

```sh
gh release edit "$tag" --repo <owner/repo> \
  --draft=false \
  --verify-tag \
  --title '<approved title>'
```

Fetch the remote tag and prove it resolves to the recorded commit. Read the published release back
and verify exact tag, title, target, stable or prerelease state, non-draft state, notes, URL, and
assets.

`gh release verify` and `gh release verify-asset` verify GitHub attestations and matching asset
digests. Use them when the release has attestations; they do not by themselves prove release notes,
tag policy, deployment health, or branch reconciliation.

After a failure, inspect the remote tag, workflow runs, draft, and published release before retrying.
Never delete, move, or recreate a published tag to conceal an error. Follow repository policy for a
corrective release, or use the next patch under the fallback policy. Report success only with the
stored URL, tag, target commit, compatibility rationale, and observed verification.

A release is complete only after cleanup. Remove the release-prep, version-bump, and
reconciliation branches and worktrees the release created once their pull requests have merged,
following the cleanup in [Pull requests](pull-requests.md). The release and deployment branches
themselves stay.
