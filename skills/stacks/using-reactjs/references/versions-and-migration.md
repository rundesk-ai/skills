# React versions and migration

## Upgrading to React 19

Upgrade `react` and `react-dom` together, with the framework or renderer that depends on them, run the
official codemods and read their diff, then search for what React 19 removed or changed:

```sh
grep -rnE "propTypes|defaultProps|contextTypes|getChildContext|createFactory|ReactDOM\.(render|hydrate|unmountComponentAtNode|findDOMNode)|react-dom/test-utils|react-test-renderer|forwardRef|ref=\"[a-zA-Z]" src
```

- `propTypes` on a function component is ignored, not an error: the code still runs and the validation
  silently stops. `defaultProps` on a function component is ignored too; use default parameters.
- Errors thrown during render are no longer re-thrown. An uncaught error goes to `window.reportError` and
  one caught by an error boundary goes to `console.error`, so reporting that listened for a global
  `error` event goes quiet without failing. Move it to the `onUncaughtError` and `onCaughtError` options
  of `createRoot` or `hydrateRoot`.
- `ref` is a regular prop, so new code does not need `forwardRef`; reading `element.ref` is deprecated in
  favour of `element.props.ref`.
- In TypeScript, `useRef` requires an argument, a ref callback may not return a value implicitly,
  `ReactElement` props default to `unknown`, and the JSX namespace moved to `React.JSX`.

Then run the suite and exercise a form submit, an error boundary, a ref-driven DOM read, and hydration
if the app renders on the server.

## Changes within React 19

| Version | Change | What breaks |
|---|---|---|
| 19.2 | `useEffectEvent` and `<Activity>` are stable | a hidden `<Activity>` runs effect cleanups but keeps state and DOM, so anything not stopped in a cleanup (a playing video) keeps going |
| 19.2 | `useId` output changed from `:r:` (19.0) and `«r»` (19.1) to `_r_` | snapshots, CSS selectors and tests that match the old format |
| 19.3 | transitions render and commit independently instead of together | code that assumed two transitions land in one commit |
| 19.3 | the automatic form reset after an action fires `onReset` | side effects in `onReset` now run after every successful action |
| 19.3 | Strict Mode double-invokes effects during hydration too | effects that were only safe because hydration ran them once |
