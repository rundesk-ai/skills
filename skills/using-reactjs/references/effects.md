# React effects

## Ask first whether the effect is necessary

Effects synchronize a component with a system outside React. If there is no external system, the
work belongs in render or in an event handler. The documented unnecessary-effect cases, and their
replacements:

| Effect used for | Replace with | Failure it causes |
|---|---|---|
| Transforming props or state for display | Compute during render | An extra render pass and a second source of truth |
| Caching an expensive calculation | `useMemo` | Re-render churn plus stale intermediate state |
| Responding to a user action that already happened | The event handler | Loss of the reason the change occurred |
| Resetting all state when a prop changes | A `key` | One stale render before the reset |
| Adjusting some state when a prop changes | Derive it, or the render-time escape hatch | Cascading re-renders that are hard to follow |
| Sharing logic between two handlers | A shared function called by both | The logic runs when state changes, not when the user acts |
| A chain where each effect sets the next state | Compute the next state in one handler | Brittle multi-pass data flow |
| Notifying a parent after state changed | Call the callback in the same handler | An extra render pass per change |
| Subscribing to an external store | `useSyncExternalStore` | Torn reads under concurrent rendering |

The single most common review finding is an effect that exists only because a value was put in
state that should have been derived. Fix the state, and the effect disappears.

## Keep effects reactive and honest about dependencies

Every reactive value the effect body reads — props, state, context, and values computed from
them — belongs in the dependency array. Do not silence the linter to make an effect run less often;
that hides a stale closure rather than removing one.

```jsx
// Bad: roomId is read but not declared, so the effect keeps the first room forever.
useEffect(() => {
  const connection = createConnection(roomId);
  connection.connect();
  return () => connection.disconnect();
}, []);

// Good: the dependency is declared, and the cleanup makes re-running safe.
useEffect(() => {
  const connection = createConnection(roomId);
  connection.connect();
  return () => connection.disconnect();
}, [roomId]);
```

If declaring a dependency makes the effect run too often, the fix is to change what the effect
depends on — move a function inside the effect, hoist a constant out of the component, or read the
latest value from a ref for genuinely non-reactive logic — not to lie about the array.

## Always write the cleanup that makes a re-run safe

Strict Mode mounts, unmounts, and remounts each component once in development specifically to prove
the effect survives being re-run. An effect that breaks under that treatment will break in
production during a discarded or replayed render.

```jsx
// Bad: an out-of-order response overwrites a newer one.
useEffect(() => {
  fetchResults(query).then(setResults);
}, [query]);

// Good: the stale response is ignored.
useEffect(() => {
  let current = true;
  fetchResults(query).then((data) => { if (current) setResults(data); });
  return () => { current = false; };
}, [query]);
```

Subscriptions, timers, animation frames, observers, and network requests all need the matching
teardown. If the effect cannot be made idempotent, that is a signal it is doing event work.

## Prefer the framework's data layer for fetching

Fetching in an effect is legitimate but carries the problems above plus waterfalls and no caching.
Where a framework or data library owns loading — a router loader, a Server Component, or a query
cache — use it, and keep effects for genuine external synchronization.
