---
name: generating-unreal-worlds
description: Use when implementing, reviewing, debugging, or validating Unreal world-generation tooling, including commandlets, Landscape, foliage, PCG, World Partition, HLOD, collision, navigation, and generated assets, or when a generated map differs between runs, saves half-built, or loses its scatter or navmesh. It supplies the Unreal stage boundaries, determinism traps, and validation that keep generated maps reproducible from semantic world data. Do not use for engine-neutral generator design such as seeds, passes, constraints, or distributions.
---

# Generate worlds in Unreal

Generate meaning first and Unreal assets second. A valid world is reproducible, traversable, and
inspectable before it is attractive.

## Establish the generation contract

1. Read the repository rules, architecture, world requirements, generator and editor modules,
   generation commands, source-asset provenance, map/config state, and current plugin list.
2. Record the semantic input this tool consumes and its version, coordinate units, stable IDs, the
   presentation outputs, collision and navigation expectations, and measured workload. Seed, pass and
   constraint design belong to the engine-neutral generator, not to this tool.
3. Name what regeneration owns. Generated paths are never hand-edited.

Do not enable PCG, World Partition, Data Validation, or another plugin without repository approval.
Keep the existing generation path until a measured requirement proves another facility is needed.

## Keep a one-way generation pipeline

```text
normalized approved inputs + seed
  -> deterministic semantic world records
  -> validate and repair semantic invariants
  -> editor/tooling projection
  -> Landscape / meshes / foliage / materials / map actors
  -> collision and navigation products
  -> asset validation and save
```

Semantic data decides terrain meaning, regions, roads, buildable space, resources, and stable
identity. PCG graphs, Actor enumeration, streaming cells, viewport position, and generated assets do
not own those facts. Runtime presentation may read them but cannot become a second world model.

## Choose Unreal facilities from proved needs

- **Commandlet:** prefer for reproducible offline imports, construction, regeneration, and CI-safe
  checks. Finish every async stage before saving.
- **Landscape:** choose valid component/section dimensions and measure component, draw, collision,
  and memory cost at the supported camera range.
- **PCG:** if approved, use for presentation scatter or one bounded authored stage. Derive component
  and point seeds from stable semantic keys and validate the output independently.
- **World Partition/HLOD:** evaluate only when streaming or editor scalability requires it. Start a
  conversion decision with report-only evidence and stable Actor GUIDs.
- **Navigation:** choose static, dynamic-modifier-only, or dynamic generation from actual runtime
  construction behavior. Decorative meshes should not affect nav.

World Partition, PCG partitioning, Landscape components, foliage grids, HLOD cells, and navmesh tiles
are different grids. Change each from its own evidence; do not align them casually.

## Preserve determinism through Unreal

| Trap | What you see | Fix and proof |
|---|---|---|
| Output depends on `TActorIterator`, `TMap`/`TSet` order, task completion, or streaming order | Same input, different placement or names between runs | Sort by stable semantic ID before spawning or naming; generate twice and diff the manifest |
| PCG seeds left at defaults, or taken from spawn order | Scatter changes when an unrelated component is added | Set each PCG component's seed from a stable semantic key and record it in the manifest |
| Saving before async work finishes | A saved map or asset missing meshes, materials, scatter, or navmesh, differently per run | Finish asset compilation (`FAssetCompilingManager::Get().FinishAllCompilation()`), wait for PCG generation and navigation builds to complete, then save |
| `.uasset` bytes compared as the oracle | Spurious diffs on every regeneration | Compare a canonical manifest of stable IDs, counts, transforms, and invariants instead |

Fail with a structured reason when a hard invariant cannot be repaired. Do not silently publish a
partial or stale map.

PCG seeds and editor determinism tools do not promise byte-identical output across platforms and
schedules. World Partition navigation and PCG Biome are experimental in UE 5.8; treat adoption as an
architecture and dependency decision.

## Run generation headless

```sh
# A project commandlet that builds or regenerates the world
UnrealEditor-Cmd "$PWD/<Project>.uproject" -run=<CommandletName> -unattended -nopause -log

# World Partition builders (HLOD, navigation) on a partitioned map
UnrealEditor-Cmd "$PWD/<Project>.uproject" <Map> -run=WorldPartitionBuilderCommandlet \
  -Builder=WorldPartitionHLODsBuilder -AllowCommandletRendering -unattended -log
```

A commandlet that logs an error can still exit 0; grep the log for `Error:` and for the commandlet's own
summary line before trusting the run.

## Prove the Unreal output

1. Generate twice from the same semantic input and compare the normalized manifest.
2. Validate generated references, names, budgets, bounds, collision, representative reachability,
   population/scatter counts, and map load.
3. Measure generation time and runtime frame/memory cost against a named scene and machine.
4. Run the repository's required build, focused test, and world-generation commands.
5. Complete the repository's visual handoff at the supported camera range and traversal. NullRHI
   and a saved map do not prove rendered vegetation or visual quality.

Read [the UE 5.8 source map](references/sources.md) before adopting or changing Landscape, PCG,
World Partition, builder commandlets, validation, or navigation behavior.
