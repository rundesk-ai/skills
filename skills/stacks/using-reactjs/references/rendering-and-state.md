# React rendering and state

## Treat render as a pure function of props, state, and context

React may render a component more than once for one update, and Strict Mode deliberately
double-invokes component bodies, initializers, and updater functions in development to expose
impurity. Anything not idempotent shows up here first.

Do not mutate props, state, values returned from Hooks, or values already placed in JSX. If a value
must be built up, build it before it reaches JSX:

```jsx
// Bad: the array used in JSX is mutated afterwards.
const rows = items.map(toRow);
return <List rows={rows} onSort={() => rows.sort(byName)} />;

// Good: sorting produces a new array at the point it is needed.
const rows = useMemo(() => [...items].sort(byName).map(toRow), [items]);
return <List rows={rows} />;
```

The bad version mutates an array React already handed to a child, so a re-render can observe a
different order than the one that produced the last commit.

## Store only what cannot be computed

Ask whether the value can be derived from props, existing state, or context. If it can, derive it.

```jsx
// Bad: selection state can point at an item that no longer exists.
const [selected, setSelected] = useState(null);
useEffect(() => { setSelected(null); }, [items]);

// Good: selection is derived from an id that survives list changes.
const selected = items.find((item) => item.id === selectedId) ?? null;
```

The bad version renders once with a stale selection before the effect clears it, and it silently
discards a valid selection whenever `items` changes for an unrelated reason.

Keep an id in state rather than an object copied out of a list. The copy goes stale the moment the
list updates.

## Reset state with identity, not with an effect

When a prop change means "this is now a different thing", give React that information directly:

```jsx
// Bad: one render with the previous user's draft still visible.
useEffect(() => { setComment(''); }, [userId]);

// Good: a new key means a new component instance with fresh state.
<Profile userId={userId} key={userId} />
```

Use this deliberately. A `key` change unmounts the subtree, so anything expensive inside it is
rebuilt; prefer it when the state genuinely belongs to the old identity.

## Adjust state during render only when nothing else works

React documents a narrow escape hatch: a component may set state during render to adjust to a prop
change, provided it only does so conditionally and only for its own state. React re-runs the
component immediately without committing the first result. Reach for a derived value first; use
this when the previous value is genuinely needed to compute the next one.

## Lift state to the closest common owner

Two components that must agree share one owner. Passing an updater down is normal React; passing
state back up through an effect is not.

```jsx
// Bad: the child mirrors the parent's value and reports changes late.
useEffect(() => { onChange(isOn); }, [isOn, onChange]);

// Good: one handler updates local state and notifies the owner together.
function toggle(next) {
  setIsOn(next);
  onChange(next);
}
```

If the same state is needed far apart, move it to context or an external store rather than
threading it through components that do not use it.

## Give list items stable identity

Keys tell React which element is which across renders. Use an id from the data. An array index is
correct only for a list that is never reordered, filtered, or inserted into; when it is,
index keys attach the wrong state and DOM to the wrong item.

```jsx
// Bad after a reorder: the input's text follows the position, not the row.
{rows.map((row, i) => <Row key={i} row={row} />)}

// Good: state follows the row.
{rows.map((row) => <Row key={row.id} row={row} />)}
```

Keys must be unique among siblings and stable across renders. Generating one during render — a
random value or a counter — defeats reconciliation entirely and remounts every item every time.
