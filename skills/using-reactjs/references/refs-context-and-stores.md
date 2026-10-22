# React refs, context, and external stores

## Use a ref for what render must not depend on

A ref holds a mutable value whose change does not trigger a render. That makes it right for timer
handles, previous values, instance-like scratch space, and DOM nodes — and wrong for anything the
UI displays.

```jsx
// Bad: the screen never updates, because writing a ref does not re-render.
const count = useRef(0);
function handleClick() { count.current += 1; }
return <p>{count.current}</p>;

// Good: rendered data is state.
const [count, setCount] = useState(0);
```

Do not read or write `ref.current` during render — that is the same purity violation as any other
render-time side effect. Read it in event handlers and effects.

For DOM access, prefer a ref over any form of node lookup; React 19 removed `findDOMNode`. A ref
callback may return a cleanup function, and in React 19 TypeScript builds an implicit return from a
ref callback is a type error precisely because it was a common accidental bug.

`ref` is an ordinary prop for function components in React 19, so a component can accept `ref`
directly without `forwardRef`.

## Shape context around what changes

Context is a delivery mechanism, not a state manager. Every consumer re-renders when the provider's
value changes by `Object.is`, so an inline object literal re-renders all of them on every parent
render.

```jsx
// Bad: a new object identity on every render of the provider's parent.
<Auth.Provider value={{ user, signOut }}>

// Good: the identity changes only when the contents do.
const auth = useMemo(() => ({ user, signOut }), [user, signOut]);
<Auth.Provider value={auth}>
```

Split a context that mixes rarely changing data with frequently changing data — a stable dispatch
context and a separate value context is the usual shape. Also give context a real default only when
a consumer outside any provider is genuinely valid; otherwise throw from a custom hook so the
mistake surfaces immediately.

## Subscribe to an external store with `useSyncExternalStore`

Any value React does not own — browser APIs, a non-React store, a module-level cache — must be read
through `useSyncExternalStore`. Reading it directly during render, or mirroring it into state via an
effect, allows tearing: two components in the same commit rendering two different values while
React yields between them.

```jsx
// Bad: an effect mirror. Two components can disagree within one commit.
const [online, setOnline] = useState(navigator.onLine);
useEffect(() => {
  const update = () => setOnline(navigator.onLine);
  window.addEventListener('online', update);
  window.addEventListener('offline', update);
  return () => {
    window.removeEventListener('online', update);
    window.removeEventListener('offline', update);
  };
}, []);

// Good: React controls the read and stays consistent within a commit.
function subscribe(callback) {
  window.addEventListener('online', callback);
  window.addEventListener('offline', callback);
  return () => {
    window.removeEventListener('online', callback);
    window.removeEventListener('offline', callback);
  };
}
const online = useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
```

Three contracts must hold:

- `subscribe` must be stable. Defining it inside the component re-subscribes on every render;
  hoist it or wrap it in `useCallback`.
- `getSnapshot` must return a cached, immutable value and a new one only when the store actually
  changed, compared with `Object.is`. Returning a fresh object each call produces React's
  "The result of `getSnapshot` should be cached" error, because each new value schedules a render
  that calls `getSnapshot` again — an infinite loop.
- `getServerSnapshot` is required for server rendering and hydration, and must return the same data
  on the server and during the client's hydration pass. Omit it only when the component is
  client-only.

```js
// Bad: a new object every call.
const getSnapshot = () => ({ todos: store.todos });

// Good: the store's own stable reference.
const getSnapshot = () => store.todos;
```

If the underlying store is mutable, cache the snapshot inside the store and replace it only when the
data changes.
