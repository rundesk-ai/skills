# Projects, frameworks and the test loop

## A project's references are its architecture

The cheapest architectural boundary in .NET is a project that does not reference the thing it must not
use. It needs no reviewer, no convention and no lint rule: the build fails.

```xml
<!-- The simulation: the base library and nothing else. -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

Put the layer that must stay pure in its own project, and let every other layer reference *it*. When
somebody reaches the other way, they find out at compile time.

## Target frameworks

`TargetFramework` is what you compile against. The installed **runtime** is what executes it, and they
are different questions: `dotnet --list-sdks` answers the first, `dotnet --list-runtimes` the second. An
assembly targeting a framework with no matching runtime installed builds and then fails to load, and the
error names the framework rather than the project — which is why a load failure is so often misread as a
code bug.

The newest SDK builds older targets, so one SDK is usually enough. A host that loads your assembly, such
as a game engine, may pin which targets it supports; that pin is a property of the host, not of C#.

## Analyzers and warnings

`TreatWarningsAsErrors` is the setting that makes the rest worth having. Without it warnings accumulate
until nobody reads them, and the one that mattered scrolls past.

- `EnforceCodeStyleInBuild` turns style rules into build diagnostics.
- `AnalysisLevel` and `AnalysisMode` select how much the built-in analyzers say.
- A `.editorconfig` at the repository root is where a rule is turned down, with a comment saying why.
- **Suppress in the narrowest place, with a reason.** `#pragma warning disable` around one line and a
  sentence explaining it is a decision; the same setting in the project file is a policy nobody wrote
  down.

Note that `var x = Expensive();` where `x` is unused does **not** raise a compiler warning: CS0219 only
fires for a variable assigned a constant. The analyzer rule IDE0059 (unnecessary assignment) reports
it, but only in the build when `EnforceCodeStyleInBuild` is on and the rule's severity is raised, so an
assignment dropped during an edit can otherwise compile clean and do nothing.

## The test loop

```sh
dotnet test                                      # everything
dotnet test --filter "FullyQualifiedName~Clock"  # one area
dotnet test --nologo                             # readable output
```

A suite over a project with no engine reference runs in milliseconds and needs nothing installed. That
speed is the reason to keep the pure layer pure — it is not a stylistic preference, it is the difference
between a suite run on every change and one run before a commit.

Keep the framework choice conventional: xUnit or NUnit, whichever the repository already uses. `[Theory]`
with `[InlineData]` covers a table of cases without a loop that stops at the first failure.

## The build's own evidence

```sh
dotnet build -bl:/tmp/build.binlog   # the complete record of what MSBuild did
dotnet build -v:n                    # readable, when the diagnostic is not enough
dotnet restore --force-evaluate      # when the restore graph is suspect
```

A binary log is the only complete answer to "which flags did that project actually compile with", and it
settles arguments that verbose output leaves open.
