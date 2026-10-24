# Traps that compile clean

Each one builds without a warning and fails later, usually far from the line that caused it. The
determinism, number and allocation traps have their own references; these are the rest.

## Collections

**Mutating a dictionary while iterating it no longer throws.** Since .NET Core 3.0, `Remove` and
overwriting an existing key during `foreach` succeed — only adding a key throws — so the bug that used to
announce itself now skips or reorders silently. Collect the changes, then apply them.

**A key mutated after it went into a `HashSet` or `Dictionary`.** `Contains` returns false for an object
that is still inside. Keys are immutable (`readonly record struct`), or hash only fields that never change.

**`ConcurrentDictionary.GetOrAdd(key, factory)` with an expensive or side-effecting factory.** Under
contention the factory ran eight times for one key; only one result is kept, and the other seven spawned
entities or loaded assets anyway. Store `Lazy<T>` values so the work runs once.

## Records and structs

**A record holding a `List<T>`.** Equality compares the list by reference, and `with` copies the
reference: the "copy" made for undo, prediction or a what-if shares its list with the live state.
Immutable collections, or deep-copy collections when cloning state.

**A struct field initializer trusted everywhere.** `struct Cfg { public int Speed = 5; public Cfg() {} }`
gives `5` from `new Cfg()` and `0` from `default` and from every element of a new array. Make the zero
value valid, or always construct.

## Events and lifetime

**An event subscription that outlives the subscriber.** The publisher keeps the subscriber alive, and it
keeps receiving events after the object it represents is gone — in an engine host, after the native
object was freed, where the next access throws. Unsubscribe where you subscribed, when the object leaves.

**`handler -= () => Refresh();` removes nothing.** A new lambda is a new delegate. Keep the delegate in a
field, or subscribe a method, and remove that.

**`static` mutable state.** It survives between tests, so a suite passes in one order and fails in
another, and between play sessions in a host that skips reloading the assembly. Instance state, owned by
something that is created and discarded with the session.

## A tick that throws halfway

An exception in the middle of a tick leaves the simulation half-updated: some agents stepped, some not,
a total out of step with its parts. Validate before mutating, or compute the next state into a buffer and
swap it in only when the whole tick succeeded.
