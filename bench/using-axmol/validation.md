# Using Axmol Validation

This is the current validation record for `using-axmol`.

## Boundary under test

The skill should activate for Axmol engine behavior — the pinned engine version contract,
engine-object lifetime, scenes, input, UI, rendering, shaders, atlases, extensions, CMake
integration, and platform builds. It should not activate for general C++ without Axmol, or for
Cocos2d-x or another fork.

## Trigger and exclusion cases

| ID | Request shape | Expected behavior |
|---|---|---|
| AXM-T01 | A sprite leaks or dangles after a scene transition | Load |
| AXM-T02 | "Touches land in the wrong place after I changed the window size" | Load |
| AXM-T03 | Review ownership in a C++ project with no engine | Do not load; `using-cpp` owns it |
| AXM-T04 | Port a Cocos2d-x project that is not Axmol | Do not load; state the fork boundary |
| AXM-T05 | Edit game design copy with no engine behavior | Do not load |
| AXM-T06 | Upgrade the pinned engine across a minor version | Load |
| AXM-T07 | Engine-object lifetime bug that is also a C++ lifetime bug | Compose with `using-cpp`; neither package is a runtime dependency of the other |

## Workflow and authority cases

| ID | Request shape | Expected behavior |
|---|---|---|
| AXM-W01 | `new`/`delete` used on an engine object | Replace with `create()`, scene ownership, or `RefPtr`, and explain the leak or dangling reference |
| AXM-W02 | Domain code including engine headers | Move the engine type to the presentation seam so the domain target stays testable without a graphics runtime |
| AXM-W03 | Advice applied without recording the engine tag or commit | Establish the pinned version first; treat v3 roadmap items as intent until a tag proves them |
| AXM-W04 | A version claim about the latest release | Re-check GitHub Releases rather than trusting a date in this package |
| AXM-W05 | A rendering fix accepted because it compiles | Require the failing backend and a live window; a compile or an offline image proves neither batching nor input coordinates |
| AXM-W06 | "The scene works now" | Reject fluent assurance; require the reproduction path re-run |
| AXM-W07 | Engine version cannot be determined | Inspect the pinned source or stop and name the unknown |
| AXM-W08 | A claim sourced only from an undocumented project observation | Do not teach it as an engine rule without tagged source or independent evidence |

## Provider evidence

Last verification: not yet run against a live provider matrix.

- Claude Code: pending. Cases marked for the sampled run are AXM-T01, AXM-T03, AXM-W06, and AXM-T07.
- Codex: not run.

No case below is marked passed. Record client versions, model identifiers, isolation constraints,
and per-case results here before claiming provider compatibility.

## Limits

AXM-T07 is the C++/Axmol composition case. No case builds or runs an Axmol project, so every
rendering and input case is graded on the decision and the proof demanded, not on observed output.
The engine-version statement in `SKILL.md` was re-verified on 23 August 2026 and will go stale.
