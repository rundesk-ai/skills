# Setup and build

## Configure cannot find axslcc

**Cause:** the engine checkout's setup has not populated its gitignored tools, or the tools belong to
a different branch.

**Replace:** initialize the pinned checkout and run its setup script. Pass platform options required
by that checkout's `docs/DevSetup.md`.

```sh
git submodule update --init
(cd <engine-checkout> && ./setup.ps1)
```

On Windows, GitHub ZIP files can carry blocking metadata that triggers PowerShell execution-policy
errors; the FAQ recommends a Git clone or an appropriate local `RemoteSigned` policy.

**Prove:** capture the engine commit and `axslcc` path/version, clean generated shader output, and
reconfigure. If shader errors began after a branch switch, restore matching tools before editing the
shader.

## An engine update becomes patch reconciliation

**Cause:** project-specific edits were made inside the pinned engine tree.

**Replace:** keep the submodule clean. Put project flags, platform packaging, and extension choices in
the project's CMake files. If the fix is genuinely engine-wide, carry it as a reviewable commit and
upstream it instead of leaving an unexplained working-tree patch.

**Prove:** `git -C <engine-checkout> status --short` is empty and updating the pointer requires no
manual edit replay.

## A new source file never compiles

**Cause:** a template that globs sources sees additions only when CMake regenerates.

**Replace:** reconfigure the existing build directory. Axmol's wrapper exposes `-f` for regeneration;
with plain CMake, run the same configure command the project already uses. Prefer explicit source
lists when the repository accepts that tradeoff.

```sh
cmake -S . -B <existing-build-dir> <existing-options>
cmake --build <existing-build-dir> --target <game-target>
```

**Prove:** inspect the regenerated build graph, then build the target and confirm the new translation
unit appears in verbose output.

## An extension option differs from copied guidance

**Cause:** extension names and defaults are versioned engine configuration.

**Replace:** use the upstream Extensions page to identify the feature, then take the exact
`AX_ENABLE_EXT_*` option and default from the pinned template's `AXGameEngineOptions.cmake`. Do not
copy a table or another release's cache line.

**Prove:** check the CMake configure summary and build the target that consumes the extension.

## An incremental Xcode build recompiles everything

This is a real workflow symptom, not an engine-wide diagnosis: it has not been reproduced
upstream, and ccache is a mitigation rather than a fix. Reduce the project against a fresh generated template, keep source-controlled inputs such as a
Podfile out of generated build directories, and compare verbose dependency output. Use ccache only
afterward to reduce unavoidable compile cost; do not let it hide a reconfigure loop.

For corrupted or raced build directories, duplicate macOS bundles, and stale artifacts, apply the
project's general C++ build-loop practice: a clean build directory, one configure command, and verbose
output that names the stale input.
