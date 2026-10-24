# Using C# validation

The current record for `using-csharp`; the method is `prompts/benchmark-skill.md`, and the latest result
is in `bench/results/using-csharp/`.

The `tycoon` fixture is a business simulation with seeded defects, each reproduced before the cases were
written: banker's rounding in tax, an unsaved RNG and job counter, culture-dependent save parsing
(`double.Parse("0.1")` reads 1 under de-DE), equal-priority jobs ordered by an unstable sort over
dictionary order, linear scans inside the tick, LINQ and string allocation per tick, and a log that grows
forever.

2026-10-23: routing 3/3 on Claude and Codex. Quality was the same on the easy and medium cases; on the
complex case both Claude runs with the skill measured allocation per tick and added a zero-allocation test,
which neither run without it did. Codex arms were indistinguishable. See the result's notes.
