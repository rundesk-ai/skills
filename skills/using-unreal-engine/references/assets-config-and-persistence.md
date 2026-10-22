# Assets, configuration, and persistence

Use this reference when introducing or changing asset identity, load policy, authored data,
configuration, reflected names, asset paths, or save-game data.

## Separate the three data roles

| Role | Typical Unreal form | Contract |
|---|---|---|
| Authored definition | Data Asset, Data Table, config, Blueprint class defaults | Reviewed content shipped with a build |
| Live runtime state | Plain values, UObject/Actor state, subsystem state | Owned by a declared runtime lifetime and authority |
| Cross-session state | Versioned `USaveGame` data or an external persistence boundary | Validated and migrated before it mutates the live world |

Do not serialize pointers to a live Actor graph as a save format. Store stable semantic identifiers and
the minimum state needed to reconstruct behavior.

## Choose references and Asset Manager deliberately

- Use a hard object/class reference only when the dependency should load with its owner.
- Use a soft reference when content is optional, streamed, large, or selected later. Make the load point visible.
- Retain the streamable handle or another strong reference for content that must stay resident.
- Use `UDataAsset` for designer-authored structured definitions. Use `UPrimaryDataAsset` or another
  Primary Asset only when stable primary identity, discovery, bundles, auditing, cook rules, or explicit
  load/unload control is required.
- Query unloaded asset metadata through the Asset Registry instead of loading every candidate.
- Add `IsDataValid` checks or editor validators when invalid authored content can survive compilation.
- Prefer the built-in Asset Manager until a concrete extension requirement exists. Configure narrow scan
  paths and exclude test/development content from production cook rules.
- Audit load behavior in cooked output. Editor discovery and an already-loaded asset can hide a missing
  cook reference.

## Change configuration at the owning layer

- Determine the configuration category and hierarchy before editing a value. Later layers override earlier ones.
- Keep shared defaults in the relevant checked-in `Config/Default*.ini` file. Keep platform differences in
  checked-in platform configuration. Do not copy local `Saved/Config` output back as an unexplained default.
- Use config-backed classes for settings that belong to startup/configuration, not as an ad hoc save system.
- When changing a setting, verify the resolved runtime value in the relevant target and platform, not only the
  text of one `.ini` layer.
- Never silently change an engine-wide base configuration when a repository or plugin layer owns the need.

## Version and migrate saves

1. Define a stable save schema independent of live Actor/UObject layout.
2. Write an explicit schema version with the save.
3. Parse and validate into temporary data before changing the live world.
4. Migrate older supported versions in deterministic steps.
5. Reject or safely preserve unsupported newer/corrupt data; never partially apply it.
6. Use a GUID-based custom version when custom UObject or package serialization needs its own schema.
7. Prefer asynchronous saving for normal play when a synchronous write could hitch.
8. Test empty, round-trip, corrupt, interrupted, oldest-supported, and newest-supported cases.

## Rename without losing serialized references

- Move and rename assets with Unreal-aware tooling so redirectors are created and referencers can be fixed.
- Fix redirectors and resave affected packages before deleting the old path.
- Add narrow Core Redirects when serialized assets depend on renamed reflected C++ symbols or packages.
- Use reflection names in Core Redirects, including Unreal's documented prefix rules.
- Validate unopened/unloaded assets and a clean cook after the rename. A currently loaded editor session is
  not proof that disk references migrated.
- Keep redirects only as long as the repository's compatibility policy requires; do not add broad substring
  redirects without auditing what they can match.
