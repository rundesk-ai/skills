# React effects

## Effects that should be something else

The lint rules now flag an effect that only copies props or state into state (`set-state-in-effect`).
These cases they do not catch:

| Effect used for | Replace with | Failure it causes |
|---|---|---|
| Responding to a user action that already happened (state changed, so submit) | the event handler | the logic runs whenever the state changes, including on load, and the reason is lost |
| Notifying a parent after state changed | call the callback in the same handler that sets state | an extra render pass per change, and the parent sees the change a commit late |
| Subscribing to a store React does not own | `useSyncExternalStore` (see [refs-context-and-stores.md](refs-context-and-stores.md)) | torn reads under concurrent rendering |

## Dependencies that make an effect run too often

Change what the effect depends on rather than trimming the array: move a function inside the effect,
hoist a constant out of the component, or, from React 19.2, move logic that must read the latest value
without re-running the effect into an Effect Event:

```jsx
const onConnected = useEffectEvent(() => showToast(`Connected to ${roomId}`, theme));
useEffect(() => {
  const connection = createConnection(roomId);
  connection.on('connected', onConnected);
  connection.connect();
  return () => connection.disconnect();
}, [roomId]); // theme changes no longer reconnect; onConnected is not a dependency
```

An Effect Event is called only from effects, never during render (React throws), and never goes in a
dependency array. On React before 19.2, a ref holding the latest value is the fallback.

## Cleanups that make a re-run safe

Strict Mode mounts, unmounts and remounts each component once in development to prove the effect
survives a re-run. Production re-runs effects too: whenever a dependency changes, when a hidden
`<Activity>` is shown again, and when a framework or Fast Refresh remounts a tree. Subscriptions, timers,
animation frames, observers and requests each need the matching teardown; a request needs a cleanup that
ignores or aborts its response. If the effect cannot be made idempotent, it is doing event work.

Where a framework or data library owns loading (a router loader, a Server Component, a query cache), use
it rather than fetching in an effect.
