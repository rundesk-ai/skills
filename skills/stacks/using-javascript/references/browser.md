# The browser

Read this when the code runs in a web page without a component framework: DOM scripts, a bundle of
plain modules, a web worker, or a library meant for browsers.

## Putting data into the page

- Besides `innerHTML` and `insertAdjacentHTML`, `document.write` and `setAttribute` on `on*`, `href` or
  `src` are code sinks. `innerHTML` does not run an inserted `<script>`, but it does run
  `<img src=x onerror=…>`, so "scripts don't run there" is no defence. Use a sanitizer only when the
  content really is HTML.
- Escaping HTML does not make a URL attribute safe: `javascript:alert(1)` has nothing to escape. Parse
  and allow-list:

```js
function safeHref(input) {
  const url = URL.parse(input, location.href);
  return url && ['https:', 'http:', 'mailto:'].includes(url.protocol) ? url.href : '#';
}
```

  The URL parser strips leading spaces and control characters and ignores case and embedded tabs, which
  is why a string check is bypassed. For a "same-site only" redirect, compare `url.origin` with
  `location.origin`.
- When a page's Content Security Policy sets `require-trusted-types-for 'script'`, assigning a string to
  a sink throws a `TypeError`. That is the policy working; route the value through a Trusted Types policy
  or use `textContent`, rather than loosening the CSP.

## Timers and scheduling

Browsers clamp nested `setTimeout(fn, 0)` to at least 4 ms after five levels, and throttle timers in
background tabs, so a loop that yields with `setTimeout(0)` crawls. Yield with `scheduler.postTask` or a
`MessageChannel` where supported, and measure time with `performance.now()` deltas, not timer counts.

## Storage and the network

- `localStorage` is synchronous, string-only, readable by any script on the origin, and can throw (quota
  exceeded, storage disabled, private modes). Never put tokens there; wrap reads and writes in
  `try`/`catch`.
- When a newer request replaces an older one (search as you type), abort the older one, so a slow old
  response cannot overwrite the newer result.

## Proof

- Behaviour that depends on the DOM is tested in a real browser or a DOM implementation (a test runner's
  jsdom or happy-dom environment); jsdom has no layout, so sizes and positions read as zero there.
- For a sink fix, render the hostile payload and assert it appears as literal text and no handler ran.
