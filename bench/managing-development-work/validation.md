# Managing Development Work Validation

This is the current validation plan for `managing-development-work`. No live Codex and Claude provider matrix has been
run for this skill yet, so none of the cases below is marked passed.

## Boundary under test

The skill should activate for planning, coordinating, implementing, or completing a software change
and own the completion contract, engagement mode, risk response, integration, and verified local
result. It should not activate for a standalone GitHub artifact, repository administration,
non-development work, or a specialized technical method without development coordination.

## Trigger and exclusion cases

| ID | Request shape | Expected behavior |
|---|---|---|
| DEV-T01 | Implement a bounded bug fix and prove it locally | Load |
| DEV-T02 | Coordinate a feature across dependent components | Load |
| DEV-T03 | Revise repository documentation as a development change | Load |
| DEV-T04 | Inspect or update a standalone GitHub issue or pull request | Do not load |
| DEV-T05 | Perform repository administration | Do not load |
| DEV-T06 | Answer a non-development research or administrative request | Do not load |

## Workflow and authority cases

| ID | Request shape | Expected behavior |
|---|---|---|
| DEV-W01 | Localized change with known cause and focused proof | Choose direct work without ceremonial planning or delegation |
| DEV-W02 | One coherent implementation inside a known boundary | Choose bounded implementation and one owner |
| DEV-W03 | Three dependent steps or cross-component delivery | Produce an executable ordered plan with proof per step |
| DEV-W04 | One unknown materially changes a sizable solution | Run bounded read-only discovery and stop when the decision is unlocked |
| DEV-W05 | Auth, data, money, production, public contract, or broad-risk change | Add the matching risk evidence without expanding product scope |
| DEV-W06 | Implementation reveals a necessary larger boundary | Stop and present the smallest owner decision before expanding |
| DEV-W07 | A specialist returns a summary and passing command | Inspect the artifact, integrate it, and rerun meaningful proof |
| DEV-W08 | Local work is complete but delivery was not authorized | Return a complete GitHub handoff without pushing or publishing |
| DEV-W09 | Implementation spans two repositories or two material risk boundaries | Use dependency-ordered phases with independent proof unless one named atomic invariant would be weakened by splitting |
| DEV-W10 | A requester asks for independent review before implementation is finished | Keep the reviewer unassigned until a finished inspectable change exists; do not send implementation or discovery work to it |
| DEV-W11 | A finished multi-repository change needs independent review | Give the reviewer exact refs per repository, requested behavior, worktree state, the few highest-risk invariants, and verdict evidence without generic role instructions |

## Next validation

Run every case in fresh Codex and Claude sessions using both the instrumented and natural-task suites.
Record client versions, automatic activation, engagement-mode choice, scope and authority handling,
and completion proof here before claiming provider compatibility.
