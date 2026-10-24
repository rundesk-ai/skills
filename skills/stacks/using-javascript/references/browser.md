# The browser

Read this when the code runs in a web page without a component framework: DOM scripts, a bundle of
plain modules, a web worker, or a library meant for browsers.

## Putting data into the page

- `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, and `setAttribute` on `on*`, `href` or
  `src` are code sinks. `innerHTML` does not run an inserted `<script>`, but it does run
  `<img src=x onerror=…>`. Put text in with `textContent`; build structure with `createElement` and
  property assignment; use a sanitizer only when the content really is HTML.
- Escaping HTML does not make a URL attribute safe: `javascript:alert(1)` has nothing to escape. Parse
  and allow-list:

```js
function safeHref(input) {
  const url = URL.parse(input, location.href);
  return url && ['https:', 'http:', 'mailto:'].includes(url.protocol) ? url.href : '#';
}
```

  The URL parser strips leading spaces and control characters and ignores case and embedded tabs, which
  is why a string check such as `startsWith('javascript:')` is bypassed. For a "same-site only"
  redirect, compare `url.origin` with `location.origin`: `//evil.example` and `/\evil.example` are
  absolute URLs to another host.
- When a page's Content Security Policy sets `require-trusted-types-for 'script'`, assigning a string to
  a sink throws a `TypeError`. That is the policy working; route the value through a Trusted Types policy
  or use `textContent`, rather than loosening the CSP.
- `setTimeout('code', 0)` and `new Function` are `eval`; a CSP without `'unsafe-eval'` blocks them.

## Timers and scheduling

- Browsers clamp nested `setTimeout(fn, 0)` to at least 4 ms after five levels, and throttle timers in
  background tabs, so a loop that yields with `setTimeout(0)` crawls. Yield with `scheduler.postTask` or
  a `MessageChannel` where supported, and do not rely on timer precision for time measurement: use
  `performance.now()` deltas.
- A delay above 2^31 − 1 ms fires immediately here too, without a warning.
- Long synchronous work blocks input and painting. Split it into chunks that yield, or move it to a Web
  Worker and send `ArrayBuffer`s with a transfer list.

## Storage and the network

- `localStorage` is synchronous, string-only, readable by any script on the origin, and can throw (quota
  exceeded, storage disabled, private modes). Never put tokens there; wrap reads and writes in
  `try`/`catch`.
- `fetch` rejects only on network failure: a 404 or 500 resolves. Check `res.ok`. It has no timeout:
  pass `AbortSignal.timeout(ms)`, and abort the previous request when a newer one replaces it so a slow
  old response cannot overwrite a new one.
- A response body read as JSON is `any`: validate it before use.

## Proof

- Behaviour that depends on the DOM is tested in a real browser or a DOM implementation (a test runner's
  jsdom or happy-dom environment); jsdom has no layout, so sizes and positions read as zero there.
- For a sink fix, render the hostile payload and assert it appears as literal text and no handler ran.
