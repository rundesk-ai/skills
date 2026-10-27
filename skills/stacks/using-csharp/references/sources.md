# C# source basis

The primary documentation behind the claims in this skill. Consult these when auditing or updating it.

| Guidance | Primary source |
|---|---|
| Dictionary and HashSet enumeration order is not part of their contract | [Dictionary\<TKey,TValue\>](https://learn.microsoft.com/dotnet/api/system.collections.generic.dictionary-2), [HashSet\<T\>](https://learn.microsoft.com/dotnet/api/system.collections.generic.hashset-1) |
| String hash codes are randomized per process | [String.GetHashCode](https://learn.microsoft.com/dotnet/api/system.string.gethashcode), [Object.GetHashCode](https://learn.microsoft.com/dotnet/api/system.object.gethashcode) |
| Floating-point behaviour and non-associativity | [Floating-point numeric types](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/floating-point-numeric-types), the language reference's note on precision |
| Nullable reference types and the null-forgiving operator | [Nullable reference types](https://learn.microsoft.com/dotnet/csharp/nullable-references), [`!` operator](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/null-forgiving) |
| String comparison is culture-sensitive by default, and ordinal comparison is the alternative | [Best practices for comparing strings](https://learn.microsoft.com/dotnet/standard/base-types/best-practices-strings), [StringComparison](https://learn.microsoft.com/dotnet/api/system.stringcomparison) |
| The default equality comparer boxes and uses reflection for a struct without `IEquatable<T>` | [EqualityComparer\<T\>.Default](https://learn.microsoft.com/dotnet/api/system.collections.generic.equalitycomparer-1.default), [ValueType.Equals](https://learn.microsoft.com/dotnet/api/system.valuetype.equals) |
| Structs, records, and readonly members | [Structure types](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/struct), [Records](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record) |
| Span, ReadOnlySpan and stackalloc | [Memory and span usage guidelines](https://learn.microsoft.com/dotnet/standard/memory-and-spans/memory-t-usage-guidelines), [Span\<T\>](https://learn.microsoft.com/dotnet/api/system.span-1) |
| ArrayPool | [ArrayPool\<T\>](https://learn.microsoft.com/dotnet/api/system.buffers.arraypool-1) |
| Garbage collection fundamentals and generations | [Fundamentals of garbage collection](https://learn.microsoft.com/dotnet/standard/garbage-collection/fundamentals) |
| Allocation and GC counters | [dotnet-counters](https://learn.microsoft.com/dotnet/core/diagnostics/dotnet-counters), [well-known counters](https://learn.microsoft.com/dotnet/core/diagnostics/available-counters) |
| async/await, and why `async void` is for event handlers | [Async return types](https://learn.microsoft.com/dotnet/csharp/asynchronous-programming/async-return-types), [Async best practices](https://learn.microsoft.com/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming) |
| Target frameworks, and the runtime that must exist to load one | [Target frameworks](https://learn.microsoft.com/dotnet/standard/frameworks), [.NET versioning](https://learn.microsoft.com/dotnet/core/versions/) |
| Warnings as errors, analysis level, EditorConfig | [Code analysis configuration](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/configuration-options), [.editorconfig for .NET](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/code-style-rule-options) |
| Unused private members, write-only members and unused parameters (IDE0051, IDE0052, IDE0060) are style rules whose severity `.editorconfig` sets | [IDE0051](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/ide0051), [IDE0052](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/ide0052), [IDE0060](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/ide0060), [Code-style analysis on build](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/overview#code-style-analysis) |
| CS0219 fires only for a variable assigned a constant | [Compiler warning CS0219](https://learn.microsoft.com/dotnet/csharp/misc/cs0219) |
| `dotnet build`, `dotnet test`, binary logs | [dotnet build](https://learn.microsoft.com/dotnet/core/tools/dotnet-build), [dotnet test](https://learn.microsoft.com/dotnet/core/tools/dotnet-test), [MSBuild binary log](https://github.com/dotnet/msbuild/blob/main/documentation/wiki/Binary-Log.md) |
| Turkish-I casing; invariant and ordinal-ignore-case comparison | [Best practices for comparing strings](https://learn.microsoft.com/dotnet/standard/base-types/best-practices-strings) |
| Shared references in JSON; `ReferenceHandler.Preserve` | [Preserve references](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/preserve-references) |
| Replacing a file atomically | [File.Move with overwrite](https://learn.microsoft.com/dotnet/api/system.io.file.move), [File.Replace](https://learn.microsoft.com/dotnet/api/system.io.file.replace) |
| `double.ToString()` round-trip on .NET Framework; `"R"` | [Standard numeric format strings](https://learn.microsoft.com/dotnet/standard/base-types/standard-numeric-format-strings#round-trip-format-specifier-r) |
| API availability by version | [.NET API browser](https://learn.microsoft.com/dotnet/api/), [C# language versioning](https://learn.microsoft.com/dotnet/csharp/language-reference/configure-language-version) |
| Sorts are unstable; `OrderBy` is stable | [Array.Sort](https://learn.microsoft.com/dotnet/api/system.array.sort), [Enumerable.OrderBy](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.orderby) |
| `PriorityQueue` is not FIFO for equal priorities | [PriorityQueue\<TElement,TPriority\>](https://learn.microsoft.com/dotnet/api/system.collections.generic.priorityqueue-2) |
| `HashCode` values are not stable across processes | [HashCode](https://learn.microsoft.com/dotnet/api/system.hashcode) |
| `Random` sequences may differ between .NET versions; not thread-safe | [System.Random](https://learn.microsoft.com/dotnet/api/system.random), [Random.cs](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Private.CoreLib/src/System/Random.cs) |
| `Vector<T>.Count` depends on hardware | [Vector\<T\>.Count](https://learn.microsoft.com/dotnet/api/system.numerics.vector-1.count), [SIMD-accelerated types](https://learn.microsoft.com/dotnet/standard/simd) |
| Deterministic parallel reduction pattern | [Parallel.For with thread-local variables](https://learn.microsoft.com/dotnet/standard/parallel-programming/how-to-write-a-parallel-for-loop-with-thread-local-variables) |
| `Math.Round` midpoint default | [Math.Round](https://learn.microsoft.com/dotnet/api/system.math.round) |
| Unchecked overflow, `checked`, `CheckForOverflowUnderflow`; LINQ `Sum` checked | [checked and unchecked](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/checked-and-unchecked), [compiler options](https://learn.microsoft.com/dotnet/csharp/language-reference/compiler-options/language#checkforoverflowunderflow), [Enumerable.Sum](https://learn.microsoft.com/dotnet/api/system.linq.enumerable.sum) |
| `%` and `/` truncate toward zero | [Arithmetic operators](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/arithmetic-operators#remainder-operator-) |
| Saturating float-to-int conversion from .NET 9 | [Breaking change: FP-to-integer conversions](https://learn.microsoft.com/dotnet/core/compatibility/jit/9.0/fp-to-integer) |
| Culture-sensitive formatting and parsing; CA1305; invariant globalization | [CA1305](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca1305), [Globalization config](https://learn.microsoft.com/dotnet/core/runtime-config/globalization) |
| System.Text.Json fields, number handling, enums, missing members, polymorphism, source generation | [Fields](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/fields), [JsonNumberHandling](https://learn.microsoft.com/dotnet/api/system.text.json.serialization.jsonnumberhandling), [JsonStringEnumConverter](https://learn.microsoft.com/dotnet/api/system.text.json.serialization.jsonstringenumconverter), [Missing members](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/missing-members), [Nullable annotations](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/nullable-annotations), [Polymorphism](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/polymorphism), [Source generation](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/source-generation) |
| BinaryFormatter removed | [BinaryFormatter migration guide](https://learn.microsoft.com/dotnet/standard/serialization/binaryformatter-migration-guide/) |
| `long.GetHashCode` folds halves with XOR | [Int64.cs](https://github.com/dotnet/runtime/blob/main/src/libraries/System.Private.CoreLib/src/System/Int64.cs) |
| Default struct hash may use one field | [ValueType.GetHashCode](https://learn.microsoft.com/dotnet/api/system.valuetype.gethashcode) |
| Mutating a struct through a `List<T>` indexer; `CollectionsMarshal` | [CS1612](https://learn.microsoft.com/dotnet/csharp/misc/cs1612), [CollectionsMarshal](https://learn.microsoft.com/dotnet/api/system.runtime.interopservices.collectionsmarshal) |
| Struct initialization and `default` | [Struct initialization](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/struct#struct-initialization-and-default-values) |
| Record equality and `with` | [Records](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/record#nondestructive-mutation) |
| `foreach` variable per iteration; iterator execution | [Iteration statements](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/iteration-statements#the-foreach-statement), [yield](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/yield#execution-of-an-iterator) |
| `Dictionary.Remove` during enumeration allowed since .NET Core 3.0 | [Dictionary.Remove](https://learn.microsoft.com/dotnet/api/system.collections.generic.dictionary-2.remove) |
| `ConcurrentDictionary.GetOrAdd` factory may run more than once | [GetOrAdd](https://learn.microsoft.com/dotnet/api/system.collections.concurrent.concurrentdictionary-2.getoradd) |
| `lock` and `System.Threading.Lock`; span in async methods | [lock](https://learn.microsoft.com/dotnet/csharp/language-reference/statements/lock), [C# 13](https://learn.microsoft.com/dotnet/csharp/whats-new/csharp-13) |
| `ConfigureAwait` and synchronization contexts | [ConfigureAwait FAQ](https://devblogs.microsoft.com/dotnet/configureawait-faq/), [CA2007](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca2007) |
| Exact per-thread allocation counter | [GC.GetAllocatedBytesForCurrentThread](https://learn.microsoft.com/dotnet/api/system.gc.getallocatedbytesforcurrentthread), [GC.GetTotalAllocatedBytes](https://learn.microsoft.com/dotnet/api/system.gc.gettotalallocatedbytes) |
| Large object heap threshold and collection | [The large object heap](https://learn.microsoft.com/dotnet/standard/garbage-collection/large-object-heap) |
| Latency modes, no-GC regions, workstation versus server | [Latency modes](https://learn.microsoft.com/dotnet/standard/garbage-collection/latency), [TryStartNoGCRegion](https://learn.microsoft.com/dotnet/api/system.gc.trystartnogcregion), [Workstation and server GC](https://learn.microsoft.com/dotnet/standard/garbage-collection/workstation-server-gc) |
| `GetValueRefOrAddDefault`, `AsSpan`, `RemoveAt` cost | [GetValueRefOrAddDefault](https://learn.microsoft.com/dotnet/api/system.runtime.interopservices.collectionsmarshal.getvaluereforadddefault), [AsSpan](https://learn.microsoft.com/dotnet/api/system.runtime.interopservices.collectionsmarshal.asspan), [List.RemoveAt](https://learn.microsoft.com/dotnet/api/system.collections.generic.list-1.removeat) |
| `params` collections | [C# 13 params collections](https://learn.microsoft.com/dotnet/csharp/whats-new/csharp-13#params-collections) |
| `ArrayPool.Rent` returns a larger, uncleared array; `stackalloc` in loops | [ArrayPool.Rent](https://learn.microsoft.com/dotnet/api/system.buffers.arraypool-1.rent), [CA2014](https://learn.microsoft.com/dotnet/fundamentals/code-analysis/quality-rules/ca2014) |
| Analysis modes; nullable warnings as errors; deterministic compilation | [AnalysisMode](https://learn.microsoft.com/dotnet/core/project-sdk/msbuild-props#analysismode), [WarningsAsErrors](https://learn.microsoft.com/dotnet/csharp/language-reference/compiler-options/errors-warnings), [Deterministic](https://learn.microsoft.com/dotnet/csharp/language-reference/compiler-options/code-generation#deterministic) |

The determinism guidance is an application of these contracts rather than a citation to a single page:
each convenience named there is documented as unspecified, and the consequence for a replayable
simulation follows from that.

Observed on .NET 10.0.9 (SDK 10.0.301, C# 14, Arm64), in throwaway console projects with Stopwatch
timing (warm-up, then best of 7) and `GC.GetAllocatedBytesForCurrentThread()` for allocation: every
measurement in [Data layout](data-layout.md) and the allocation figures in
[Allocation and collection](allocation-and-gc.md); unstable sort past 16 items; `PriorityQueue` order;
NaN and subtraction comparers; `HashCode.Combine` differing between launches; three float sums from
three methods; parallel totals (16 distinct in 20 runs, 1 with fixed chunks); `Math.Round`, overflow,
negative division, saturating casts; `double.Parse("1.5")` returning 15 under de-DE; the
System.Text.Json defaults; `list[i].Move()` mutating a copy; struct initializers skipped by `default`;
the 20,000-chunk large-object-heap churn; and the analyzer rules each `AnalysisMode` turns on.
Results are from one Arm64 machine; x64 was not measured.
Also compiled and run on .NET 10 when the references were last revised: the full-width FNV digest
distinguishing values that differ above the low byte; `SplitMix64` as a class sharing state across
references; the basis-point tax giving 3 for 25 at 10%; `FloorDiv` on negatives; the struct initializer
skipped by `default` and arrays; and `-=` with a new lambda removing nothing.

The duplication and dead-code patterns come from the cleanup history of a private multi-project C#
simulation (2026-10): about two dozen review rounds, most areas needing three or four before one came
back clean, found the formulas, lookups, copied methods, re-derived view rules, unread outputs and
left-behind paths shown in [Duplication and dead code](duplication-and-dead-code.md); the examples are
renamed. Its own instructions already said to search before writing new logic and to add no "for
later" code. The analyzer table was observed on .NET 10 (SDK 10.0.301) in a throwaway project with that
solution's settings: with `latest-recommended`, `EnforceCodeStyleInBuild` and no severity overrides,
an unused private method and an unused parameter produced no diagnostic, and a private field written
from a parameter produced none (CS0414 only for a constant); raising IDE0051, IDE0052 and IDE0060
reported each, and nothing reported an unused `internal` or `public` method. Run over that solution's
simulation projects after its review rounds, the three rules still found an unused private method and
an unused parameter, and one false positive on a record's own `PrintMembers`. Across its dead-code
commits, removed `public` declarations outnumbered `private` ones about two to one.
Later rounds in the same project removed whole public types and interface members kept alive only by
tests and test stubs, an event with no subscriber, a setter and probe hooks nothing set, a default every
caller overrode, and about twenty comments citing documents and task ids that the repository never had.
