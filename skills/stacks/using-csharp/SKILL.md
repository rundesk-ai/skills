---
name: using-csharp
description: Use when writing, reviewing, debugging, organizing, or building C#, including nullability, struct versus class, allocation and garbage collection in a per-frame or per-tick loop, collection choice and iteration order, determinism, money, rounding and overflow, culture-safe parsing and save formats, analyzers and warnings, solution and project layout, target frameworks, and `dotnet build` and `dotnet test`. It supplies C# defaults, the failure each one prevents, and an evidence-first workflow. Do not use it for another .NET language, for engine APIs, or for test design method alone.
---

# Use C#

Make state explicit, allocation deliberate, and iteration order something you chose rather than something
you inherited.

## Establish the target before changing code

The language version, the target framework and the runtime decide which of the rules below even apply.

```sh
grep -rE "TargetFramework|LangVersion|Nullable|TreatWarningsAsErrors" --include="*.csproj" --include="*.props" .
```

A game engine host pins these, and may run the code on a runtime other than CoreCLR — Mono or an
ahead-of-time compiler — where the GC settings, allocation counter and float behaviour below differ.
Find out which before using an API from this list:

| API | Needs | Fallback |
|---|---|---|
| `CollectionsMarshal.AsSpan` | .NET 5 | an array you own |
| `PriorityQueue`, `CollectionsMarshal.GetValueRefOrAddDefault` | .NET 6 | a sorted list; `TryGetValue` |
| `record struct` | C# 10 | a `readonly struct` implementing `IEquatable<T>` and `GetHashCode` |
| `UnmappedMemberHandling` | .NET 8 | a strict-load test |
| saturating float-to-int casts, `RespectNullableAnnotations`, `System.Threading.Lock` | .NET 9 | clamp first; a test; a private lock object |
| `params ReadOnlySpan<T>` | C# 13 | fixed-argument overloads |

A project that sets `TreatWarningsAsErrors` has already decided a warning is a defect: do not suppress one
to get a build green. Read every warning; nullability and unused-result warnings are the defect you were
about to ship.

## Determinism is the expensive default

In a simulation that must replay, iteration order and floating-point accumulation are load-bearing, and
the language's convenient defaults are the wrong ones. **Read
[Determinism](references/determinism.md) before writing simulation state**; the short version:

| Convenience | What it costs | Instead |
|---|---|---|
| `Dictionary<K,V>` / `HashSet<T>` enumeration | Order is not part of their contract and changes with insertion **and removal** history | An ordered collection, or sort a key snapshot before iterating |
| `Array.Sort`, `List<T>.Sort` | **Unstable**: past 16 items, equal keys come out in an order that depends on the input order | A comparer that ends in a unique tie-break (`id`), or `OrderBy(...).ThenBy(id)`, which is stable |
| `PriorityQueue<TElement,TPriority>` | Equal priorities do not come out first-in, first-out | Priority `(int priority, long sequence)`, with the sequence counter kept in simulation state |
| `string.GetHashCode()`, `HashCode.Combine`, and any tuple, record or anonymous type holding a string | Randomized per process | Never order, bucket or persist simulation state by a hash |
| `Guid.NewGuid()`, object identity, `RuntimeHelpers.GetHashCode` as an entity id | Differs every run | A `long` counter kept and saved in simulation state |
| Sorting or comparing strings with the default comparer | Culture-sensitive, so the order changes with the machine's locale | `StringComparer.Ordinal`, and `StringComparison.Ordinal` on every comparison that is not shown to a person |
| `float`/`double` accumulation across a tick | Order of operations changes the low bits; `Vector<T>` width changes it per CPU | Integer or fixed-point where bits must match |
| `DateTime.Now` | Wall clock | The simulation's own tick |
| `Random`, seeded or not | Its state cannot be saved, and a seeded sequence is not promised across .NET versions | A small generator you own (xoshiro, PCG, SplitMix64) whose state is fields in the simulation state |
| `Parallel.For`, `AsParallel` | Completion order, and reduction order | Single-threaded until measured; then fixed chunks reduced in index order |

## Numbers lie quietly

None of these throws, so the first symptom is a wrong balance or a unit on the wrong tile. Read
[Numbers](references/numbers.md) before writing money, rounding, coordinates or a ratio:

- `Math.Round(2.5)` is `2`: the default rounds a midpoint to even. Pass the `MidpointRounding` the
  design wants, every time.
- `int` arithmetic wraps on overflow (`int.MaxValue + 1` is negative); LINQ `Sum()` throws instead. Hold
  money in `long` minor units and add `checked` where a total can grow without bound.
- `/` and `%` truncate toward zero, so `-1 / 16` is tile `0`. Use floor division, or `>>` and `&` for a
  power-of-two chunk size.
- `1.0 / 0` is infinity and `0.0 / 0` is NaN, and both spread through every value that reads them. A
  comparer that mishandles NaN mis-sorts without an exception.

## Text written to a file is not culture text

`ToString()`, interpolation and `double.Parse` use the machine's culture: on a de-DE machine
`double.Parse("1.5")` returns `15`, with no exception. Everything written to or read from a save, a
config or the network uses `CultureInfo.InvariantCulture`; analyzer CA1305 does not catch interpolation.
A data key lowered with `ToLower()` breaks under tr-TR (`"I"` becomes `"ı"`): `ToLowerInvariant`, or
`StringComparer.OrdinalIgnoreCase`.
Read [Saves and serialization](references/saves-and-serialization.md) before writing a save format.

## Traps that compile clean

- **`list[i].Move()` on a struct in a `List<T>` moves a copy**, with no diagnostic (`list[i].X = 5` is an
  error, the method call is not). Mutate through an array element or `CollectionsMarshal.AsSpan(list)[i]`,
  or make the struct `readonly` so the mistake cannot compile.
- **Key a map by a `readonly record struct`, never a packed `long`.** `long.GetHashCode()` is `x ^ y`:
  90,000 grid keys landed on 512 hash codes, 200 times slower. A bounded grid is a flat array — see
  [Data layout](references/data-layout.md), which also covers chunked worlds.
- **Prove a tick allocates nothing.** `GC.GetAllocatedBytesForCurrentThread()` is exact to the object on
  CoreCLR, so a warmed-up test can assert zero bytes per tick; an array of 85,000 bytes or more is freed
  only by a full collection, so a streamed world that drops big chunk arrays pauses on a schedule. Read
  [Allocation and collection](references/allocation-and-gc.md).
- **In an engine host, an `await` resumes on the main thread only through the host's
  `SynchronizationContext`.** `ConfigureAwait(false)` and `Task.Run` leave it, and engine objects touched
  from there fail or corrupt; `.Result` or `.Wait()` on that thread deadlocks the frame. Compute plain
  data off the main thread and apply it there — and the object you awaited for may have been destroyed
  meanwhile: tie a `CancellationToken` to its lifetime and check it after every `await`.
- **`!` silences a nullable warning without fixing it.** Fix the flow or make the type nullable.

Read [Anti-patterns](references/anti-patterns.md) for the rest that compile clean and fail later.

## A project's references are its architecture

A layer that must not reach the engine is a project that does not reference it, so the day someone breaks
the rule the build fails rather than a reviewer noticing. Read [Project setup](references/project-setup.md)
for frameworks, runtimes and analyzers.

## Report

Name the behaviour, the file and the command whose output proves it; a green build proves only that it
compiles. [Sources](references/sources.md) holds the evidence behind each rule.
