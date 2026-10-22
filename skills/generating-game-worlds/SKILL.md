---
name: generating-game-worlds
description: Use when designing, implementing, reviewing, or validating procedural generation for game-world terrain, biomes, waterways, roads, regions, districts, settlements, sites, or semantic population; or when defining seeds, staged generator passes, constraints, repair and fallback, seed sweeps, distribution evidence, mixed-initiative overrides, or generator provenance. It supplies an engine-neutral semantic generation workflow. Do not use it for authored level design, runtime world simulation, rendering, asset creation, or engine-specific APIs alone.
---

# Generate game worlds

Generate semantic worlds that downstream systems can inspect, simulate, render, and reproduce. A
plausible screenshot is not proof of a valid world, and one attractive seed says little about the
generator's distribution.

## Define the generation contract

Before choosing noise, grammars, search, simulation, or learned generation, record:

- **Purpose:** production tool, fixed shipped seed, player-facing world creation, per-run variation,
  adaptive content, or another use.
- **World promise:** the player decisions, traversal, stories, economies, or simulations the output
  must support; treat any experience claim as a hypothesis.
- **Semantic outputs:** canonical terrain, elevation, water, climate, regions, networks, parcels,
  sites, resource opportunities, hazards, landmarks, and spawn envelopes actually required.
- **Granularity and scale:** world, region, route, district, site, cell, and object relationships that
  must agree.
- **Control:** fixed inputs, designer parameters, masks, anchors, protected content, editable stages,
  and permitted randomness.
- **Envelope:** offline or runtime, required or optional content, latency and memory limits, target
  platforms, and failure policy.

Use the simplest generator family that satisfies the contract. Noise can shape fields; graphs can
own connectivity; partitions can own regions and parcels; grammars can express structured families;
search or constraint solving can satisfy coupled objectives; simulation can model a causal process.
Do not choose a fashionable technique before defining the property it must guarantee or explore.

## Keep semantic truth ahead of presentation

Emit stable domain records, not sprite names, texture slots, scene nodes, or baked pixels:

```text
WorldSpec {
  generatorIdentity
  canonical coordinate and topology contract
  semantic layers, graphs, objects, relationships, and stable IDs
  declared constraints and validation evidence
  source and override provenance
}
```

Grid topology, projection, rendering, and visual assets consume these records; they do not own
them. This skill may assign a semantic style or asset-family key; it does not create the asset.

## Make reproducibility an explicit envelope

A seed is only one input. Persist enough identity to recreate or diagnose the output:

```text
generator name and version
configuration schema and normalized values
root seed and random-stream policy
stage versions and enabled rules
input dataset, mask, template, model, and asset-library identities
manual constraints and overrides
target compatibility envelope
```

Give stages independent named random streams or derive choices from stable semantic keys. Inserting
one optional decoration pass must not silently change every downstream river, road, or settlement.
Define whether identical output is promised only within one build, across compatible generator
versions, or across platforms; test that bounded claim.

```text
Good: reproduce a failure from generator version, normalized config, inputs, overrides, and seed.
Bad:  log only `seed=42` while code, masks, templates, and random call order change underneath it.
```

## Build a staged dependency pipeline

Order passes from broad constraints to dependent detail. A common world pipeline is:

```text
normalize inputs and protected anchors
-> substrate and boundaries
-> climate, water, and other causal fields
-> regions and biome classification
-> primary networks and connectivity
-> districts, blocks, parcels, or sites
-> semantic population and opportunities
-> validate -> repair or fallback -> publish
```

This is a dependency example, not a required city model. Declare what each pass reads, writes,
invalidates, and guarantees. Preserve intermediate semantic products and diagnostics. When a designer
changes an upstream constraint, rerun the smallest downstream closure whose guarantees may have
changed; never patch a derived sprite while leaving its semantic source inconsistent.

Create variation from changed causes and constraints where believability matters: coastlines shape
routes, routes shape parcels, parcels constrain buildings. Random jitter may add cosmetic texture,
but it is not a substitute for a world history or a valid topology.

## Specify constraints before generation

Classify every important property:

- **Hard invariant:** output is unusable if violated, such as required connectivity, legal support,
  non-overlap, reachable objectives, or a protected landmark.
- **Soft objective:** improve, score, or expose as a tradeoff, such as route directness, biome mix,
  density, sightline variety, or travel burden.
- **Distribution target:** behavior across many seeds, such as frequency, range, correlation, tail
  risk, or coverage—not a requirement on every world.

Attach the check to the earliest stage where the property becomes decidable. Validate both local
geometry and global graphs. A road can look connected at tile scale while its district remains
unreachable; a valid world graph can still produce a broken shoreline transition.

Never hide an unsatisfied hard invariant inside a weighted score. Do not invent target distributions
from aesthetics alone; derive initial ranges from the game promise, authored references, domain
constraints, or pilot worlds, then revise them with play evidence.

## Repair without concealing failure

Choose a bounded response per invariant:

1. prevent the invalid state constructively;
2. reject or backtrack the smallest responsible stage;
3. apply a deterministic semantic repair whose cost and side effects are checked;
4. fall back to a known-valid template or safe reduced form; or
5. stop with a structured failure when no honest output is possible.

Record original failure, repair actions, affected stages, and final validation. Cap attempts and time;
an unbounded reroll can hang at runtime and makes rare failures invisible during development. Do not
silently choose a new seed, because it destroys reproduction and biases distribution measurements.

```text
Good: detect a disconnected required site, reconnect under declared route constraints, then rerun
      reachability and dependent parcel checks.
Bad:  retry random worlds until one loads and discard every failed seed from the report.
```

## Support human direction at the semantic layer

For mixed-initiative or production tools, let designers pin anchors, paint influence fields, lock
regions, edit graphs, add constraints, accept a proposal, or request alternatives. State which edits
are authoritative and which generated details may be replaced.

Preserve human intent during regeneration. When constraints conflict, report the smallest conflicting
set and valid relaxations; do not silently move protected content. Keep generated proposals reviewable
and reversible. If a team cannot inspect the produced volume at representative scales, reduce the
batch, improve diagnostics, or sample from a declared distribution instead of treating volume as
quality.

## Evaluate the generator, not a favorite seed

Build a versioned seed suite containing:

- fixed regression seeds for every known failure and boundary condition;
- random or stratified seeds for distribution estimates;
- extreme parameter combinations and minimum/maximum world sizes;
- adversarial anchors, masks, coastlines, narrow passages, isolated regions, and crowded sites; and
- curated reference seeds for human visual and play inspection.

For every seed, store generation time, pass and repair counts, invariant results, semantic summary,
and a world hash within the promised envelope. Across seeds, inspect distributions and correlations
that correspond to the world promise. Include median, tails, worst valid cases, failed cases, and
repair-heavy cases—not only averages or exemplars.

Metrics reveal what the chosen representation measures; they do not prove beauty, believability,
difficulty, or enjoyment. Combine automated semantic checks with multiscale inspection:

```text
whole world -> region -> route or district -> site -> edge/object transition
```

Inspect the player's supported views, rotations, zooms, traversal, and starting conditions. Use
agents or path probes for reachability and workload evidence, then playtest whether representative
players perceive useful variation and make the intended decisions.

## Preserve provenance and shipping boundaries

Record the origin, version, license or usage terms, transformation, and approved shipping status of
every external dataset, heightmap, template, rule library, trained model, and content family used by
the generator. Generated output does not automatically erase restrictions on its inputs. Route legal
conclusions and product-specific rights review to qualified owners; this skill only requires that the
evidence and decision remain attached.

Separate development-only source material from redistributable runtime inputs and generated output.
Do not download, train on, transform, or ship material merely because it is publicly viewable. Keep
the shipping manifest reproducible from approved sources.

## Deliver and prove the generator contract

Produce:

1. purpose, player hypothesis, semantic output schema, controls, and non-goals;
2. versioned reproduction envelope and random-stream policy;
3. pass dependency graph with read, write, invalidation, and guarantee contracts;
4. hard invariants, soft objectives, distribution targets, and their evidence;
5. bounded reject, repair, fallback, and structured-failure policies;
6. designer override and regeneration behavior;
7. seed suite, metrics, multiscale inspection matrix, and player-test questions;
8. source, transformation, rights-review, and shipping provenance; and
9. unresolved failures, blind spots, performance limits, and compatibility boundaries.

The evidence and limits behind this workflow are in [sources.md](references/sources.md).
