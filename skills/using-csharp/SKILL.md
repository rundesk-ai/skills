---
name: using-csharp
description: Use when writing, reviewing, debugging, organizing, or building C#, including nullability, struct versus class, allocation and garbage collection in a per-frame or per-tick loop, collection choice and iteration order, determinism, analyzers and warnings, solution and project layout, target frameworks, and `dotnet build` and `dotnet test`. It supplies C# defaults, the failure each one prevents, and an evidence-first workflow. Do not use it for another .NET language, for engine APIs, or for test design method alone.
---

# Use C#

Make state explicit, allocation deliberate, and iteration order something you chose rather than something
you inherited.

## Establish the environment before changing code

The language version, the target framework and the warning settings decide which of the rules below even
apply. Read them rather than assuming them.

```sh
dotnet --list-sdks                          # which SDKs exist; the newest builds every target
dotnet --list-runtimes                      # which runtimes can RUN what you build
cat *.sln 2>/dev/null | head -20            # what the solution holds
grep -rE "TargetFramework|LangVersion|Nullable|TreatWarningsAsErrors" --include="*.csproj" .
```

A project that sets `TreatWarningsAsErrors` has already decided that a warning is a defect; do not
suppress one to get a build green. A project without it has warnings nobody reads, and adding a rule
there is a change of its own.

## Work in this order

1. **Read the repository's rules and the nearest existing code.** Match its idiom before importing one.
2. **Name what the change must be true of** — a value, an invariant, an order — and where that is
   enforced.
3. **Write the narrowest change**, then read it back against the failure modes below.
4. **Build, and read every warning.** A warning about nullability or an unused result is the compiler
   reporting the defect you were about to ship.

## Determinism is the expensive default

In a simulation that must replay, iteration order and floating-point accumulation are load-bearing, and
the language's convenient defaults are the wrong ones. **Read
[Determinism](references/determinism.md) before writing simulation state**; the short version:

| Convenience | What it costs | Instead |
|---|---|---|
| `Dictionary<K,V>` / `HashSet<T>` enumeration | Order is not part of their contract and changes with insertion **and removal** history | An ordered collection, or sort a key snapshot before iterating |
| `string.GetHashCode()` | Randomized per process by default | Never order or bucket simulation state by a hash |
| Sorting or comparing strings with the default comparer | Culture-sensitive, so the order changes with the machine's locale | `StringComparer.Ordinal`, and `StringComparison.Ordinal` on every comparison that is not shown to a person |
| `float`/`double` accumulation across a tick | Order of operations changes the low bits | Integer or fixed-point where bits must match |
| `DateTime.Now` | Wall clock | The simulation's own tick |
| `Random` without stored state | Not reproducible and not saved | RNG state inside the simulation state |
| `Parallel.For`, `AsParallel` | Completion order, and reduction order | Single-threaded until a measurement demands otherwise |

## Defaults and the failure each prevents

- **Nullable reference types on, and honoured.** `?` on a reference type is a claim about whether it can
  be null; `!` withdraws that claim and is a promise you are making to the compiler. A file full of `!`
  has the syntax of null safety and none of the benefit.
- **`readonly` on a field that does not change, `readonly record struct` for a small value.** A mutable
  struct passed by value is copied, and the copy is what you mutated.
- **Prefer a `struct` for a small immutable value and a `class` for identity.** A struct in a
  `List<T>` is stored inline, which is what makes a cell grid cheap; a struct with identity semantics is
  a bug waiting for someone to compare two of them.
- **Give a struct `IEquatable<T>` before using it as a dictionary key or comparing it in a loop.**
  Without it the default comparer falls back to `ValueType.Equals`, which boxes both sides and compares
  by reflection — correct, and orders of magnitude slower than the comparison you meant to write.
- **`StringComparison.Ordinal` for every comparison a person does not read.** The default for
  `string.Compare` and for sorting is culture-sensitive: the same code orders differently on another
  machine, and `ToLower()` to compare allocates a string to throw away. Culture-aware comparison is for
  text shown to a user, and nothing else.
- **Throw on a precondition, at the boundary.** `ArgumentOutOfRangeException` where an index is checked
  beats reading a neighbouring element and returning a plausible wrong answer.
- **Do not allocate in a per-tick or per-frame path.** The collection you build every frame is the
  garbage the collector pauses to clean. Read
  [Allocation and collection](references/allocation-and-gc.md).
- **`var` where the type is on the line, the type where it is not.** `var x = Get();` tells a reader
  nothing.
- **An `async void` that is not an event handler has nowhere to report a failure**, so its exception
  becomes a process-level crash or silence. Return `Task`.

Read [Anti-patterns](references/anti-patterns.md) for the longer list with the failures each one produced.

## Organize projects around what may depend on what

Read [Project setup](references/project-setup.md) for target frameworks, solution layout, analyzers and
`dotnet test`. The rule that matters most: **a project's references are its architecture, enforced by the
compiler.** A layer that must not reach the engine is a project that does not reference it, and the day
someone breaks that rule the build fails rather than a reviewer noticing.

## Report what you changed and what proves it

Name the behaviour, the file and function, and the command whose output shows it. A build succeeding is
evidence that the code compiles and nothing else.

## References

- [Determinism](references/determinism.md) — iteration order, hashing, floating point, and what a
  digest actually proves.
- [Allocation and collection](references/allocation-and-gc.md) — where garbage comes from in a game
  loop and how to see it.
- [Project setup](references/project-setup.md) — frameworks, solutions, analyzers, `dotnet test`.
- [Anti-patterns](references/anti-patterns.md) — the recurring mistakes, each with its failure.
- [Sources](references/sources.md) — the primary documentation behind these claims.
