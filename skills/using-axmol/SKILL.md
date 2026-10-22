---
name: using-axmol
description: Use when building, reviewing, debugging, configuring, or migrating an Axmol game, including the pinned engine version contract, engine-object lifetime, scenes, input, UI, rendering, shaders, atlases, extensions, CMake integration, and platform builds. It supplies version-gated Axmol defaults, traps, and proof steps. Do not use for general C++ work without Axmol, or for Cocos2d-x or another fork of it.
---

# Use Axmol

Treat the pinned engine as the contract. Axmol v2 is C++20 LTS; v3 is an active-development line
with incompatible input and rendering changes.

## Establish the line before changing code

Locate the checkout instead of assuming its directory name:

```sh
git submodule status
git -C <engine-checkout> describe --tags --always
```

The rules below were checked against tag `v2.11.4`. Check GitHub Releases for the latest v2 LTS
before recommending an upgrade, and treat v3 roadmap items as intent until the pinned source or a tagged
release proves them.

## Work in this order

1. Record the engine commit or tag, target platform, generator, and resolution policy.
2. Reproduce the symptom in the smallest scene or target. Rule out a stale or partial build before
   changing code: reconfigure, rebuild the affected target, and confirm the binary postdates the edit.
3. Put the change on the correct side of the engine boundary. Domain and simulation code should not
   need Axmol headers.
4. Trace every stored engine pointer to an owner. Let the node tree own children; use `ax::RefPtr`
   for a reference that must survive independently.
5. Validate through the failing backend and live window. A successful compile or offline image does
   not prove runtime rendering, input coordinates, or batching.

## Defaults that prevent common failures

| Avoid | Prefer | Failure avoided |
|---|---|---|
| `new`/`delete` on engine objects | `create()`, scene ownership, or `RefPtr` | Leaks and dangling references |
| Mixing frame pixels with design-space coordinates | One `getVisibleRect()`-based scene coordinate contract | HUD, camera, and hit-test disagreement |
| Multiple non-sampler blocks in a v2 stage | One non-sampler block per stage | Metal-only shader failure |
| Assuming custom shaders batch | Finalize identical state, call `updateBatchId()`, measure | Draw-call explosion |
| Reusing Cocos project files | Fresh Axmol template plus pinned headers | Build and signature failures |

## Read only the reference the task needs

- [Memory](references/memory.md) for storing, creating, collecting, or diagnosing `ax::Object`
  instances.
- [Scene and UI](references/scene-and-ui.md) for resolution policies, node lifecycle, clipping,
  listeners, text input, and physics-sized nodes.
- [Graphics](references/graphics.md) for Axmol 2 shaders, batching, texture sampling, atlases, and
  SDF text.
- [Setup and build](references/setup-and-build.md) for `setup.ps1`, axslcc, CMake generators,
  extensions, and slow or stale builds.
- [Architecture](references/architecture.md) when engine dependencies leak into the core or tests.
- [Migration](references/migration.md) before a Cocos2d-x port or v2-to-v3 evaluation.
- [Review checklist](references/anti-patterns.md) for a scoped Axmol review; it indexes the
  references above by failure surface.
- [Source basis](references/sources.md) when changing or auditing a claim.

Report findings as symptom, cause, replacement, and proof:

```text
[HIGH] Stored autoreleased Sprite* can outlive its frame
Cause: no parent or retained owner keeps the object alive after the autorelease pool drains.
Replace: attach it to the owning node, or store ax::RefPtr<Sprite>.
Proof: in an isolated debug checkout, enable the pinned v2.11.4 source's
AX_OBJECT_LEAK_DETECTION gate, then exercise removal and scene teardown.
```
