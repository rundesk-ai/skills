# React concurrency, Suspense, and actions

## Deferred values and transitions

```jsx
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

The `memo` is what makes it work. Without it the urgent render re-renders `Results` with the old value,
paying the full cost on every keystroke, and then renders it again in the background: with a 50 ms list,
the keystroke took 51 ms without `memo` and under 1 ms with it. Where the React Compiler has compiled the
parent, it supplies the memoization.

Neither `useDeferredValue` nor `useTransition` makes rendering faster; they change what may be
interrupted. A list slow because it renders ten thousand rows needs virtualization or pagination. Keep a
controlled input's own value out of a transition, or typing lags.

With an async action, `isPending` from `useTransition` stays true across the awaited work, so it is the
right loading flag for that action. It does not cover work started outside the transition, such as a
fetch an effect starts after the commit.

## Suspense in React 19

- When a child suspends, the fallback commits at once and the siblings render afterwards in a pre-warm
  pass.
- When the data arrives, React throttles the reveal, so content can appear about 300 ms after its data:
  by design, and something a fake-timer test has to advance through.
- Keep an already-visible region on screen during an update by driving it through a transition rather
  than letting it fall back to a spinner.

## Form actions and optimistic updates

- Return the submitted values from an action (with `useActionState`) so a reset form can show them again
  as `defaultValue`; or use `onSubmit` with `startTransition` when no reset is wanted.
- `useFormStatus` reads only the `<form>` above the component that calls it, so called in the component
  that renders the form, `pending` is always false. Put the submit button in a child component.
- `useOptimistic` applies its value only inside a transition or action; outside one it shows nothing and
  logs an error. Inside, the optimistic value rolls back by itself when the action ends without
  committing real state. A state update after an `await` is no longer part of the transition: wrap it in
  `startTransition` again.
