# Design, refine and resume a game model

This is a working procedure, not evidence that any model made with it is good. It rests on four
things holding together: assembled mockups rather than isolated parts, structural form before surface
detail, one shared direction across a family, and review in context. The task owns its artistic
choices; the project owns its source and delivery constraints. Do not transplant one game's look to
another.

## Begin with the target and a durable checkpoint

Keep one current-state record for the model: a section in the project's durable work record, or a
dedicated design-state file, never both. Keep it outside ignored scratch directories and commit it by explicit path under the repository's document rules.
Record only information needed to resume the work; link evidence instead of copying it into prose.

Record the target fields listed in `SKILL.md` before modeling, and separate approved direction from
experiments. Start from this game's accepted look and refine only the decisions this task actually
needs.

Maintain this compact checkpoint at every meaningful iteration, owner correction, stage transition and
before a handoff or anticipated compaction. Do not rely on predicting when compaction will occur.

| Field | Record |
|---|---|
| Objective and current stage | Intended look/use; blockout, representative assembly, surfaces, family review or delivery |
| Workspace and source | Branch/worktree, last committed source revision, recipe or editable source paths, current local changes and any in-progress command/session |
| Direction and decisions | Named references and comparison purpose; accepted proportions/materials; owner decisions with date and exact approval scope |
| Current candidate and baseline | Distinct ids; source revision or digest and parameter/seed values; render paths and whether each is a Blender preview or native engine capture |
| Reproduction | Exact invocation and input paths; camera, lighting, scale, resolution and pose/state needed to repeat the comparison |
| Observation and open defects | What was actually inspected, what changed, what still fails, and which checks have not run |
| Rejected approaches | Brief reason for rejection and evidence link, so the next session does not repeat the same experiment |
| Plan and next action | Remaining stages and the next concrete change, its reason and the view that will reveal whether it helped |
| Approval status | Approved, candidate, rejected or pending, separately for direction, model appearance and delivery; unresolved owner questions |

Preserve recoverable source for every baseline and checkpointed candidate before overwriting it: commit
the recipe and parameters, or save an exact source snapshot through the project's permitted source
mechanism, including versioned inputs and dependencies. A digest identifies bytes but cannot restore
them; a description of uncommitted edits is not a snapshot. Record the source commit being described;
do not try to embed the checkpoint commit's own hash in itself. Commit the checkpoint promptly.
Ignored render files may remain local under project rules, but their
exact locations and regeneration inputs belong in the durable record. Missing captures invalidate visual
evidence until recovered or regenerated; do not label a replacement as an old approved image.

## Resume after compaction or a session change

1. Reload repository instructions and applicable skills, then read the brief and its checkpoint.
2. Confirm the branch/worktree and inspect status/diffs. Reconcile the recorded source with the actual
   files before editing; do not overwrite unexplained changes or assume they belong to this task.
3. Open the named references and latest baseline/candidate captures. Read the relevant recipe parameters
   and any still-running command's output. A chat summary or prose claim alone cannot re-establish a look.
4. State the stage, unresolved defect and next experiment; continue the recorded plan. If source or
   evidence has drifted, record the discrepancy and recover from the exact saved revision in an isolated
   location, preserving unexplained current edits. If recovery is impossible, mark the comparison pending
   and establish a new candidate explicitly. Existing approval applies only to its recorded source and
   scope; a modified candidate does not inherit it. Ask only for missing decisions that prevent progress,
   not for approvals already recorded.

## Iterate through the stages

The stage table and the per-iteration loop are in `SKILL.md`. Beyond them: keep enough of an assembly
visible to expose repetition, not just its most attractive crop; use close views for diagnosis and
gameplay views for acceptance. For a new family, three assets can be a useful pilot, not a mandatory
quota for a one-off. If the direction needs owner judgment, present the concrete comparison at that
checkpoint, and never claim owner acceptance because an agent found no defect.

## Choose the authoring route by what must read

| Asset | Working route | Trap to avoid |
|---|---|---|
| Rigid buildings, vehicles and props | Establish overall masses; refine useful repeated parts and their joins in an assembly; use the modular contract for parts that actually mate | Perfect individual windows on an ill-proportioned house; repeated components stretched beyond their intended shape |
| Animals and other deforming organic forms | Establish anatomical masses, silhouette and proportion; develop surface continuity and deformation-compatible topology; inspect required poses/motion before expanding variants | Treating anatomical design masses as mandatory disconnected meshes, or assuming one neutral pose proves animation quality |
| Vegetation | Establish crown/trunk masses, branching rhythm and visible gaps; develop a representative cluster within the whole; compare required growth forms and distance views | Polishing individual leaves while the crown silhouette is wrong, or treating every age as a uniformly scaled adult |
| Rocks and other continuous static forms | Establish primary mass and characteristic planes, then secondary breaks and surface treatment | Decomposing a continuous form just to satisfy a part count |

These are design routes, not newly approved geometry generators. Use tools and sources the project
allows. Scripts automate repetition and reproducibility; they do not choose convincing forms on their
own. Keep design parts, authoring objects and delivered meshes distinct; `modular-kits.md` owns that
contract. Surface detail may be represented in geometry, textures or a bake according to the intended
camera and consumer; no high-to-low baking requirement or universal polygon budget follows from this.

## Surface treatment is a required handoff

An untextured or flat-colored preview can settle form without settling appearance. Before declaring a
surfaced model ready, identify the source of each material family and which of its geometry, UV mapping,
textures, vertex data and shader setup carries the intended result. Record any unimplemented surface
work as pending, with its next action; do not let it disappear because standalone painting or engine
material graphs belong to a different task or skill.

Compare related wood, stone, metal, skin or foliage side by side. Check physical feature scale, grain
direction, broad color/value grouping, roughness/specular character and wear placement. Shared materials
should support a family without making all substances respond alike. Use restrained variation with a
visible reason, and preserve quiet areas where detail would compete with the major forms.

Inspect the material treatment both in neutral diagnostic light and in the intended game context.
An attractive Blender render is a preview, not proof that the engine has the same material response.
The UV, slot, color-space and import contracts belong to the tool and the consumer, not here; verify
every control against the installed version when implementing.

## Completion evidence

Keep the accepted whole-model comparison, representative part/assembly views and relevant family lineup
linked from the checkpoint, with the owner's actual verdict or "not yet given". Record reproducibility
and delivery checks separately. When an asset's appearance has not been rendered and inspected, report
the workflow or geometry as prepared, never as visually proven. A reusable workflow is demonstrated by
accepted assets produced through it, not by this document passing a validator.
