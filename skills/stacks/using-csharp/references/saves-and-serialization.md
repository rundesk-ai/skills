# Saves and serialization

A save is a contract with every earlier build and every other machine. Prove it with a test that saves
mid-game, loads, keeps running both copies, and compares their digests: a round trip compared
immediately after load misses state that is not saved, such as a generator's position or an id counter.

## Culture

A text format you write yourself is read back with the current culture unless you say otherwise:

```csharp
// Bad: correct on the developer's machine only.
writer.WriteLine($"rate {rate}");
var rate = double.Parse(parts[1]);

// Good
writer.WriteLine(string.Create(CultureInfo.InvariantCulture, $"rate {rate}"));
var rate = double.Parse(parts[1], CultureInfo.InvariantCulture);
```

- Analyzer CA1305 flags `ToString()` and `Parse` without a provider, but **not interpolation**.
- Test a hand-written format under another culture: set `CultureInfo.CurrentCulture = new("de-DE")` in
  the test, or run it with `LANG=de_DE.UTF-8`.
- `<InvariantGlobalization>true</InvariantGlobalization>` makes the whole process invariant — right for
  a headless simulation server, a tool or a test runner, wrong for a client that shows localized text.
- System.Text.Json already writes and reads numbers invariantly; this applies to text you format.

## System.Text.Json

Each default below drops or refuses data silently:

| Default | What happens | Instead |
|---|---|---|
| Public fields are ignored | `Gold` is missing, a `(int X, int Y)` property is written as `{}` | Properties, `[JsonInclude]` or `IncludeFields = true`; a named `record struct` instead of a tuple |
| NaN and infinity throw | The save fails hours after the NaN was produced | Keep state finite; validate before saving |
| Enums are written as numbers | Inserting a member in the middle remaps every saved value | Explicit values on persisted enums, or `JsonStringEnumConverter` |
| Unknown and missing members are ignored | A renamed property loads as its default; a non-nullable `string` loads as `null` | `UnmappedMemberHandling = Disallow` (.NET 8) and `RespectNullableAnnotations` (.NET 9) in tests |
| Polymorphism needs declaring | A derived type saves as its base | `[JsonPolymorphic]` and `[JsonDerivedType]`; `$type` must be the first property unless `AllowOutOfOrderMetadataProperties` (.NET 9) |

Use the source generator (`[JsonSerializable(typeof(Save))] partial class SaveContext : JsonSerializerContext`)
where the build is trimmed or compiled ahead of time; reflection-based serialization is unsafe there.

`BinaryFormatter` throws `PlatformNotSupportedException` from .NET 9. A binary save is a format you
define — a `BinaryWriter` with a version header, or a schema'd library.

## Identity and order in a saved graph

- **Two references to one object save as two copies.** A citizen referenced by its home and by its
  workplace loads as two citizens. Save ids and resolve them after load (or `ReferenceHandler.Preserve`
  where the format is yours alone).
- A `Dictionary` serializes in its enumeration order, so two saves of the same state can differ byte for
  byte and a digest of the file proves nothing. Write sorted keys, or digest the loaded state.
- On .NET Framework and older Mono, `double.ToString()` does not round-trip: a value saved and loaded
  changes, and a replay diverges after load. Use `"R"`, or store the bits.

## Writing the file

Write to a temporary file, flush it, then replace the old save (`File.Move(tmp, path, overwrite: true)`
or `File.Replace`). A crash or a killed process mid-write otherwise destroys the only save.

## Versioning

Put a `Version` in every save root and migrate on load, keyed by it. Validate what you read: an enum
from a file can hold any integer (`Enum.IsDefined`, or a `switch` whose default throws), and a count can
be negative.

## What else belongs in the save

Everything the next tick reads: the generator's state, every id or sequence counter, pending queues in
their order, and the tick itself. A value recomputed on load is fine only when a test proves the
recomputation matches.
