# C# source basis

The primary documentation behind the claims in this skill. Consult these when auditing or updating it.

| Guidance | Primary source |
|---|---|
| Dictionary and HashSet enumeration order is not part of their contract | [Dictionary\<TKey,TValue\>](https://learn.microsoft.com/dotnet/api/system.collections.generic.dictionary-2), [HashSet\<T\>](https://learn.microsoft.com/dotnet/api/system.collections.generic.hashset-1) |
| String hash codes are randomized per process | [String.GetHashCode](https://learn.microsoft.com/dotnet/api/system.string.gethashcode), [Object.GetHashCode](https://learn.microsoft.com/dotnet/api/system.object.gethashcode) |
| Floating-point behaviour and non-associativity | [Floating-point numeric types](https://learn.microsoft.com/dotnet/csharp/language-reference/builtin-types/floating-point-numeric-types), [IEEE 754 conformance in .NET](https://devblogs.microsoft.com/dotnet/floating-point-parsing-and-formatting-improvements-in-net-core-3-0/) |
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
| CS0219 fires only for a variable assigned a constant | [Compiler warning CS0219](https://learn.microsoft.com/dotnet/csharp/misc/cs0219) |
| `dotnet build`, `dotnet test`, binary logs | [dotnet build](https://learn.microsoft.com/dotnet/core/tools/dotnet-build), [dotnet test](https://learn.microsoft.com/dotnet/core/tools/dotnet-test), [MSBuild binary log](https://github.com/dotnet/msbuild/blob/main/documentation/wiki/Binary-Log.md) |

The determinism guidance is an application of these contracts rather than a citation to a single page:
each convenience named there is documented as unspecified, and the consequence for a replayable
simulation follows from that.
