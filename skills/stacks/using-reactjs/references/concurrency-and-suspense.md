# React concurrency and Suspense

## Know which behavior concurrency actually changes

Concurrent rendering means React may start a render, pause it, discard it, or run it again before
committing. Three consequences matter in review:

1. A render that is not pure can be observed twice or partially.
2. A value read outside React can change mid-render, producing a torn UI. That is what
   `useSyncExternalStore` exists to prevent; see
   [refs-context-and-stores.md](refs-context-and-stores.md).
3. Some updates can be marked lower priority so urgent input stays responsive.

## Separate urgent updates from the work they cause

An input that feels stuck is usually one state update driving both the field and an expensive list.

```jsx
// Bad: every keystroke renders the whole result list synchronously.
function Search() {
  const [query, setQuery] = useState('');
  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Results query={query} />
    </>
  );
}

// Good: the field stays urgent; the list is allowed to lag and be interrupted.
const Results = memo(function Results({ query }) { /* slow list */ });

function Search() {
  const [query, setQuery] = useState('');
  const deferred = useDeferredValue(query);
  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Results query={deferred} />
    </>
  );
}
```

The `memo` is what makes it work. Without it the urgent render re-renders `Results` with the old
value, paying the full cost on every keystroke, and then renders it again in the background: in a
measurement with a 50 ms list, the keystroke took 51 ms without `memo` and under 1 ms with it. Where the
React Compiler is on and has compiled the parent, it supplies the memoization.

`useDeferredValue` fits a value derived from an urgent one. `useTransition` fits an action — a tab
change, a route change, a submit — where you also want a pending flag:

```jsx
const [isPending, startTransition] = useTransition();
startTransition(() => setTab(next));
```

Neither makes rendering faster. They change what is allowed to be interrupted. If the list is slow
because it renders ten thousand rows, virtualize or paginate it; a transition only hides the cost
behind responsiveness.

Do not put a state update that must be applied immediately — a controlled input's own value — inside
a transition. It will lag visibly.

## Place Suspense boundaries where a fallback makes sense

A boundary defines the region that is replaced by a fallback while content below it is pending. One
boundary at the root turns every small load into a full-page spinner; a boundary per row turns a
list into a flicker field.

Put the boundary around a region the user can accept losing, keep the fallback close in size to the
real content to avoid layout shift, and let an already-visible region stay visible by driving the
update through a transition instead of a new boundary.

Two React 19 behaviours change how a boundary looks in practice. When a child suspends, the fallback
commits at once and the siblings render afterwards in a pre-warm pass. When the data arrives, React
throttles the reveal, so content can appear about 300 ms after its data: by design, and something a
fake-timer test has to advance through.

`use(promise)` needs a promise that survives re-renders. A promise created during render is a new one
each time, so the boundary shows its fallback forever while the component re-renders around a hundred
times a second, and development usually prints no warning. Create the promise in a Server Component, a
router loader, or a cache keyed by its inputs.

Suspense catches suspended reads, not errors. Pair it with an error boundary; they are separate
mechanisms with separate fallbacks.

## Do not read `isPending` as "loading"

`isPending` reports that a transition is still rendering, not that data arrived. A component that
uses it as a data-loading flag will show the wrong state whenever rendering and fetching do not
line up.

## Prove concurrency behavior through user-visible timing

Verification is the input remaining responsive while the expensive region lags, the fallback
appearing exactly where intended, and no torn value across components in one commit. A green unit
test that renders the component once proves none of that.

## Form actions and optimistic updates

- After a `<form action={fn}>` action finishes, React resets the form's uncontrolled fields, including
  when the action returned a validation error, so the user's input disappears. Return the submitted
  values from the action (with `useActionState`) and pass them back as `defaultValue`, keep the field
  controlled, or use `onSubmit` with `startTransition` when no reset is wanted. From 19.3 the automatic
  reset also fires `onReset`, so code in `onReset` runs after every successful action.
- `useOptimistic` applies its value only inside a transition or action; outside one it shows nothing
  and logs an error. Inside, the optimistic value rolls back by itself when the action ends without
  committing real state, so no `catch` is needed for the rollback. A state update after an `await` is
  no longer part of the transition: wrap it in `startTransition` again.
