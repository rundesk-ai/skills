# React tests

## Assert what the user observes

Query by accessible role, label, and text. Those queries fail when the feature breaks and survive
refactors that change structure but not behavior. Reaching into internal state, a component
instance, or a CSS-module class name produces tests that break on harmless changes and stay green
on real ones.

```jsx
// Bad: passes even if the button is unreachable, mislabelled, or never rendered.
expect(wrapper.state().submitted).toBe(true);

// Good: fails exactly when the user-visible outcome fails.
await user.click(screen.getByRole('button', { name: /save/i }));
expect(await screen.findByText(/saved/i)).toBeVisible();
```

Prefer `user-event` over firing raw DOM events: a real click also focuses, and typing produces the
key sequence a real keyboard produces. Tests built on synthetic `fireEvent` calls routinely pass
against components that a person cannot actually operate.

## Let `act` do its job instead of working around it

Every update React processes in a test must be wrapped in `act`, so that effects flush and the DOM
settles before assertions run. React Testing Library already wraps `render` and its event helpers,
so most tests should never call `act` directly.

In React 19, `act` is exported from `react`. Every other `react-dom/test-utils` helper was removed;
its `act` re-export remains only as a deprecated shim that logs an error. `react-test-renderer` is
deprecated in favour of Testing Library.

```js
// Deprecated in React 19; logs an error on first use.
import { act } from 'react-dom/test-utils';

// Correct.
import { act } from 'react';
```

An "not wrapped in act" warning is a real finding: something updated state after the test stopped
looking. Fix it with an async query — `findBy*`, or `waitFor` around the assertion — rather than by
silencing the warning or adding a fixed timeout.

## Distinguish absence from not-yet

`getBy*` throws when nothing matches, `queryBy*` returns null and is the only correct way to assert
absence, and `findBy*` returns a promise and is the only correct way to wait for something
asynchronous. Using `getBy*` for a value that arrives later produces a flaky test; using `findBy*`
to assert absence always passes.

## Control asynchrony rather than sleeping

Fake or stub the network at the boundary the component actually uses, and resolve it explicitly.
A fixed `setTimeout` in a test trades correctness for a delay that is too short on a loaded machine
and too long on every run.

## Fake timers hang Testing Library under Vitest

With `vi.useFakeTimers()`, `await user.type(...)`, `await user.click(...)` and `findBy*` time out, even
with `userEvent.setup({ advanceTimers: vi.advanceTimersByTime })`. Testing Library waits on a
`setTimeout(0)` after each async helper and advances fake timers only when a global `jest` exists, so
under Vitest that timeout never fires.

```js
vi.useFakeTimers({ shouldAdvanceTime: true });
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
// advance the component's own timers inside act:
await act(async () => { vi.advanceTimersByTime(1000); });
```

A test that renders with a plain `createRoot` instead of Testing Library must set
`globalThis.IS_REACT_ACT_ENVIRONMENT = true`, or `act` warns that the environment is not configured for
it; Testing Library sets the flag itself.

## Test a hook through a component

A hook's contract is what it does inside a render. Render a small component that uses it, drive it
through user interaction, and assert the rendered result. That covers dependency mistakes and
cleanup, which a direct function call cannot reach.

## Prove the test has teeth

Before trusting a new test, break the code it covers and watch it fail. A test that passes against
a deliberately broken implementation is worse than no test, because it advertises coverage that
does not exist.
