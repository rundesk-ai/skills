# React versions and migration

## Establish the version scope first

```sh
npm ls react react-dom
```

React and `react-dom` must be on the same major version. This skill targets React 19.x on the
stable `latest` channel.

Under React's versioning policy, the stable channel follows semver: patch for critical fixes and
security, minor for features and non-critical fixes, major for breaking changes. Four things are
explicitly excluded from that promise and must never become a production default: development-only
warnings, APIs prefixed with `unstable_`, canary and experimental builds, and undocumented
internals. Canary is offered for framework authors, not applications.

Do not record a "latest" version number in project guidance. Query the registry at review time.

## Apply the React 19 removals

Removed from `react`:

| Removed | Replacement |
|---|---|
| `propTypes` on function components | TypeScript, or runtime validation you own |
| `defaultProps` on function components | ES default parameters (class components keep it) |
| Legacy context: `contextTypes`, `getChildContext` | `createContext` |
| String refs (`ref="input"`) | Callback refs or `useRef` |
| Module pattern factories | A function returning JSX |
| `React.createFactory` | JSX |

Removed from `react-dom`:

| Removed | Replacement |
|---|---|
| `ReactDOM.render` | `createRoot` |
| `ReactDOM.hydrate` | `hydrateRoot` |
| `ReactDOM.unmountComponentAtNode` | `root.unmount()` |
| `ReactDOM.findDOMNode` | A DOM ref |
| `react-dom/test-utils` helpers (its `act` is a deprecated shim) | `act` from `react`; Testing Library for the rest |
| `react-test-renderer/shallow` | `react-shallow-renderer`, or move to Testing Library |

`propTypes` being ignored rather than erroring is the trap worth calling out: the code still runs
and the validation silently stops happening.

## Handle the behavior changes, not just the renames

Errors thrown during render are no longer re-thrown. An uncaught error goes to `window.reportError`
and an error caught by an error boundary goes to `console.error`. Reporting that relied on a global
`error` event will go quiet without failing; move it to the `onUncaughtError` and `onCaughtError`
options on `createRoot` or `hydrateRoot`.

`ref` is a regular prop for function components, so new code does not need `forwardRef`. Reading
`element.ref` is deprecated in favour of `element.props.ref`. UMD builds are gone; use an ESM CDN.

In TypeScript, `useRef` now requires an argument, ref callbacks may not return a value implicitly,
`ReactElement` props default to `unknown`, and the JSX namespace moved to `React.JSX`.

## Upgrade with evidence

1. Read the release notes for every major crossed, not only the newest.
2. Upgrade `react` and `react-dom` together, plus the renderer or framework that depends on them.
3. Run the official codemods where they exist, then read the diff rather than trusting it.
4. Search the codebase for every identifier in the tables above, plus `forwardRef`,
   `react-dom/test-utils`, and any global error reporting.
5. Run the test suite, then exercise a form submit, an error boundary, a ref-driven DOM read, and
   hydration if the app renders on the server.

Translate older advice only after checking it against the documentation for the installed version.
