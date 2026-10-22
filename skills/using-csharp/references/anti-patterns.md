# C# anti-patterns

Each entry is a mistake, the failure it produces, and the replacement. The defaults in `SKILL.md`
(nullability, mutable structs, `async void`) and the per-frame allocation table in
[Allocation and collection](allocation-and-gc.md) are not repeated here.

## State and types

**A `public` field on a type others construct.** Nothing can be validated later without breaking callers.
→ A property, and validate in the constructor.

**A collection property with a public setter.** Any caller can replace the whole collection.
→ Expose `IReadOnlyList<T>`, or a `ReadOnlySpan<T>` for a hot read.

**`==` on a reference type expecting value comparison.** Two equal objects are not the same object.
→ `record`, or implement `IEquatable<T>` deliberately.

## Control flow

**`catch (Exception)` with no rethrow.** The failure vanishes and the program continues in a state
nobody designed.
→ Catch the specific type you can handle; let the rest travel.

**`.Result` or `.Wait()` on a Task.** Deadlock on a context that needs the thread you just blocked.
→ `await`.

**An exception used for ordinary control flow.** Slow, and it buries the real one in the log.
→ A `TryX` method returning `bool`.

**An empty `catch` block.** The single most expensive line in any codebase.
→ Log it, or do not catch it.

## Collections and loops

**`Dictionary` or `HashSet` enumeration in simulation state.** Order is not part of the contract; see
[Determinism](determinism.md).
→ An ordered collection, or a sorted key snapshot.

**`.Count()` on an `IEnumerable<T>`.** Walks the whole sequence; on a lazy one it may walk it twice.
→ `.Count` on a collection.

**Mutating a collection while iterating it.** An exception, or worse, a silently skipped element.
→ Collect what to change, then change it.

## Lifetime

**A `static` mutable field.** Survives between tests, so a suite passes in one order and fails in
another; and, in a host that reloads assemblies, it resets when nobody asked.
→ Instance state, owned by something.

**An event subscription never removed.** The subscriber cannot be collected, and it keeps receiving
events after it should have stopped.
→ Unsubscribe where you subscribed, or use a weak pattern deliberately.

**`IDisposable` not disposed.** A handle or buffer held until the finalizer, which may be never.
→ `using`.

## Shape

**A method that both decides and acts and reports.** It cannot be tested without doing all three.
→ Split until each part can be proved alone.

**A parameter that only chooses a branch.** `Build(grid, preview: true)` is two methods.
→ Two methods.

**A comment restating the code.** It goes stale and then it lies.
→ Comment the *why*: the rule, the constraint, the failure this shape prevents.
