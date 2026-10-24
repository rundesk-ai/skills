# React refs, context, and external stores

## Ref callbacks

A ref callback may return a cleanup function, and when it does React calls the cleanup instead of
calling the callback with `null`. An inline ref callback is a new function every render, so React
detaches and re-attaches it on every render: hoist it or wrap it in `useCallback` when attaching is
expensive (an observer, a third-party widget). In TypeScript, an implicit return from a ref callback is a
type error, because returning something by accident now means "cleanup".

## Context: measure before restructuring

Every consumer re-renders when the provider's value changes by `Object.is`, so an inline object literal
re-renders all of them on every render of the provider's parent. How much that costs depends on the
consumers: 2,000 cheap consumers re-rendered in about 0.4 ms (production build, jsdom), and the same
update with a memoized value took 0.01 ms. It matters when consumers are expensive or the value changes
often.

```jsx
const auth = useMemo(() => ({ user, signOut }), [user, signOut]);
return <Auth value={auth}>{children}</Auth>; // React 19: no .Provider needed
```

Split a context that mixes rarely changing data with frequently changing data; a stable dispatch context
and a separate value context is the usual shape. Give context a real default only when a consumer outside
any provider is valid; otherwise throw from a custom hook so the mistake surfaces at once.

## Stores React does not own

Read any value React does not own (a browser API, a non-React store, a module-level cache) through
`useSyncExternalStore`. Reading it directly during render, or copying it into state from an effect,
lets two components in one commit render different values.

`getSnapshot` must return the same value until the store changes, compared with `Object.is`. A selector
that builds a new array or object on each call loops forever: each new value schedules a render that
calls `getSnapshot` again, and React reports "The result of `getSnapshot` should be cached".

```js
// Bad: a new array every call.
const getSnapshot = () => store.items.filter((item) => item.visible);

// Good: return the store's own reference, and filter during render or with useMemo.
const getSnapshot = () => store.items;
```

If the store is mutable, cache the snapshot inside the store and replace it only when the data changes.
Keep `subscribe` stable (hoisted, or `useCallback`), or React re-subscribes on every render, and pass
`getServerSnapshot` when the component renders on the server.
