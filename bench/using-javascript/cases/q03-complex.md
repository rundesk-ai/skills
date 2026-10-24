+++
skill = "using-javascript"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "orders"
rubric = """
result.1  Finds the regular expression `^([a-zA-Z0-9_.+-]+)+@...` backtracks catastrophically (nested quantifier): a short invalid email blocks the event loop for seconds; measures it (time against input length) and fixes it with a linear pattern or a length cap, proving the time is flat after.
result.2  Finds that `orders.forEach(async ...)` leaves `saveOrder` promises unawaited, so one rejection is unhandled and exits the process (Node's default since 15), and `/sync` reports success before anything is saved; fixes with awaited iteration or `Promise.allSettled` and reports failures.
result.3  Finds prototype pollution in `merge`: a body of `{"__proto__": {"isAdmin": true}}` reaches `Object.prototype`, after which `canExport` lets every user export; fixes by skipping `__proto__`, `constructor` and `prototype` (or a null-prototype target, or a schema), and tests the exploit.
result.4  Finds the static-file check `file.startsWith(PUBLIC)` is a prefix test, so `..%2Fpublic-drafts%2F...` escapes into the sibling `public-drafts` directory; fixes with `path.relative` (or a separator-terminated prefix) and tests it.
result.5  Finds the unbounded `searchCache` (every distinct query is kept forever: memory grows with public traffic) and bounds or removes it; and names the synchronous `readFileSync` + `JSON.parse` per request as event-loop blocking that grows with the data.
result.6  Adds a regression test per fix that fails on the original code, and the suite passes.
result.7  Separates what was proved from what was inferred, and names what remains (for example request body size limits, rate limiting, the `topOrders` comparator returning a boolean so the "top" list is unsorted).
conduct.1 Measures or reproduces each problem before fixing it, rather than rewriting on appearance.
"""
+++
The order service goes on the public internet next week. In last week's load test, requests hung for
seconds at a time and the process exited twice. Harden it and fix what you find.
