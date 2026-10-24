# React tests

## `act` warnings are findings

A "not wrapped in act" warning means something updated state after the test stopped looking. Fix it with
an async query (`findBy*`, or `waitFor` around the assertion), not by silencing the warning or adding a
fixed timeout. In React 19, `act` comes from `react`; the `react-dom/test-utils` re-export is a
deprecated shim that logs an error, and `react-test-renderer` is deprecated in favour of Testing Library.

A test that renders with a plain `createRoot` instead of Testing Library must set
`globalThis.IS_REACT_ACT_ENVIRONMENT = true`, or `act` warns that the environment is not configured for
it; Testing Library sets the flag itself.

## Vitest traps

- **No automatic cleanup.** Testing Library unmounts between tests only when the runner exposes a global
  `afterEach`, which Vitest does only with `globals: true`. Otherwise the first test's DOM is still there
  in the second, which fails with "Found multiple elements" or passes against the wrong render. Add
  `afterEach(cleanup)` to the setup file.
- **Fake timers hang.** With `vi.useFakeTimers()`, `await user.type(...)`, `await user.click(...)` and
  `findBy*` time out, even with `userEvent.setup({ advanceTimers: vi.advanceTimersByTime })`. Testing
  Library waits on a `setTimeout(0)` after each async helper and advances fake timers only when a global
  `jest` exists, so under Vitest that timeout never fires.

```js
vi.useFakeTimers({ shouldAdvanceTime: true });
const user = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
// advance the component's own timers inside act:
await act(async () => { vi.advanceTimersByTime(1000); });
```

## Hooks

Test a hook through a rendered component, or `renderHook`, and assert the rendered result: a direct call
cannot exercise its dependencies or its cleanup.
