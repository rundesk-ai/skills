# Projects, runtimes and analyzers

## The layer that must stay pure is its own project

Put the simulation in a project that references nothing it must not use — no engine, no UI — and let
every other layer reference it. Its tests then run in milliseconds with nothing installed, which is the
difference between a suite run on every change and one run before a commit.

## Target framework and runtime are different questions

`TargetFramework` is what you compile against; the installed runtime is what executes it
(`dotnet --list-runtimes`). An assembly whose framework has no matching runtime builds and then fails to
load, with an error naming the framework rather than the project — so a load failure is often misread as a
code bug. A host that loads your assembly, such as a game engine, pins the targets and sometimes the
runtime itself; that pin decides which APIs exist.

## Analyzers

- `<AnalysisMode>Recommended</AnalysisMode>` turns on the culture rules (CA1304, CA1305, CA1309, CA1310,
  CA1311) and the double-lookup rule CA1854. CA1305 does not flag string interpolation.
- Enable single rules in `.editorconfig` rather than taking `All`: CA1851 (multiple enumeration) and
  CA2002 (`lock (this)`) are worth it; CA2007 (`ConfigureAwait`) is wrong in code that runs inside an
  engine host, because `ConfigureAwait(false)` moves the continuation off the main thread.
- `<WarningsAsErrors>nullable</WarningsAsErrors>` makes nullable warnings errors without failing the build
  on everything else — how a project adopts null safety a step at a time.
- Suppress in the narrowest place, with a reason: `#pragma warning disable` around one line and a
  sentence, not a project-wide setting nobody wrote down.
- `<Deterministic>` makes identical source produce identical assemblies. It does nothing for simulation
  determinism.

## When the build itself is in question

`dotnet build -bl` writes a binary log, the only complete answer to which flags a project actually
compiled with.
