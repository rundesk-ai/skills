# JavaScript source basis

The evidence behind the claims in this skill. Status: **observed** means reproduced in October 2026 on
Node 25.2.1 (V8 14.1), with Node 22.23 for comparisons, npm 11.6 and 12.2, pnpm 10.20, and TypeScript
7.0.2, 6.0.3 and 5.9.3; **documented** means a primary source; **community** means a widely cited write-up.
Timings are single-machine runs (Apple Silicon), median of several runs with each variant in its own
process; read them as ratios.

## Values

| Claim | Status | Source |
|---|---|---|
| `toFixed` exposes binary rounding; Intl rounds the same value differently; Intl prints `-0` | observed | [toFixed](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed), [Intl.NumberFormat](https://tc39.es/ecma402/#sec-intl.numberformat) |
| Integers above 2^53 lose precision in `JSON.parse`; the reviver's `context.source` recovers them | observed | [JSON.parse source text access proposal](https://github.com/tc39/proposal-json-parse-with-source) |
| Date-only strings parse as UTC, date-time strings as local | observed, documented | [Date time string format](https://tc39.es/ecma262/#sec-date-time-string-format), [Date.parse](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/parse) |
| Invalid ISO days roll over; months overflow; DST makes a day 23 hours | observed | |
| Temporal absent on Node 25 even with the harmony flag; on by default in Node 26 | observed (25), community (26) | [nodejs/node#58730](https://github.com/nodejs/node/issues/58730), [nodejs/node#57127](https://github.com/nodejs/node/issues/57127) |
| Default sort compares strings; boolean comparators leave arrays unsorted; sort is stable | observed, documented | [SortCompare](https://tc39.es/ecma262/#sec-sortcompare), [V8: stable sort](https://v8.dev/features/stable-sort) |
| Replacement strings interpret `$` patterns | observed | [String.prototype.replace](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace) |
| Plain-object dictionaries inherit keys; integer-like keys order first | observed | |
| Timer delays above 2^31 − 1 ms become 1 ms | observed, documented | [Node timers](https://nodejs.org/api/timers.html) |
| Spread into a call overflows the stack near 120,000 elements | observed | |
| Environment variables are strings; `JSON.stringify(new Error())` is `{}` | observed | |
| Graphemes, normalization, locale case mapping, `localeCompare` cost | observed, documented | [localeCompare performance](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare#performance) |
| `structuredClone` is 1.8 times slower than a JSON round trip on plain data | observed | community: [nodejs/node#50320](https://github.com/nodejs/node/issues/50320) |
| String `+=` is not quadratic on V8; `delete` and megamorphic shapes slow hot loops; holes cost about 7% | observed | [V8: fast properties](https://v8.dev/blog/fast-properties) |

## Async and Node

| Claim | Status | Source |
|---|---|---|
| Unhandled rejections exit with code 1 since Node 15, including "start both, await one by one" and `forEach(async)` | observed, documented | [--unhandled-rejections](https://nodejs.org/api/cli.html#--unhandled-rejectionsmode) |
| `Promise.all` leaves other work running and leaks what it opened; a small pool avoids `EMFILE` | observed | |
| `AbortSignal.timeout` rejects with `TimeoutError`; `fetch` has no total timeout | observed, documented | [AbortSignal.timeout](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal/timeout_static) |
| An unconsumed `fetch` body holds its connection | documented, not run | [undici: garbage collection and response bodies](https://undici.nodejs.org/#/?id=garbage-collection) |
| Dynamic `import()` of a Windows absolute path needs `pathToFileURL` | documented, not run | [ESM import specifiers](https://nodejs.org/api/esm.html#urls) |
| Large synchronous `JSON.parse` blocks the loop; `monitorEventLoopDelay` measures it | observed | [perf_hooks](https://nodejs.org/api/perf_hooks.html#perf_hooksmonitoreventloopdelayoptions) |
| Microtasks starve timers | observed | |
| Ignoring `write()` buffers without bound; `.pipe()` leaves the source open; `pipeline` destroys and rejects once | observed, documented | [Backpressuring in streams](https://nodejs.org/en/learn/modules/backpressuring-in-streams), [stream.pipeline](https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-options) |
| `process.exit()` truncates piped stdout; exit codes 1, 137, 143 | observed, documented | [A note on process I/O](https://nodejs.org/api/process.html#a-note-on-process-io), [Exit codes](https://nodejs.org/api/process.html#exit-codes) |
| `server.close()` closes idle keep-alive sockets and waits for in-flight requests | observed | [server.close](https://nodejs.org/api/http.html#serverclosecallback) |
| PID 1 gets no default signal handling | community | [Docker Node best practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md#handling-kernel-signals) |
| Default heap about 4 GB; `--max-old-space-size` sets old space only; percentage flag | observed, documented | [--max-old-space-size-percentage](https://nodejs.org/api/cli.html#--max-old-space-size-percentagepercentage) |
| Heap sized from the container limit | community, not run | [Node.js memory in containers](https://developers.redhat.com/articles/2025/10/10/nodejs-20-memory-management-containers) |
| Closures in one scope share a context | observed | community: [Grokking V8 closures](https://mrale.ph/blog/2012/09/23/grokking-v8-closures-for-fun.html) |
| `Map` cache leak against `WeakMap`; heap snapshot flags | observed, documented | [--heapsnapshot-signal](https://nodejs.org/api/cli.html#--heapsnapshot-signalsignal) |
| Worker start-up, clone and transfer costs; workers do not speed up one task | observed, documented | [worker_threads](https://nodejs.org/api/worker_threads.html) |
| `require(esm)` returns the namespace; top-level await throws `ERR_REQUIRE_ASYNC_MODULE` | observed, documented | [Loading ES modules with require](https://nodejs.org/api/modules.html#loading-ecmascript-modules-using-require) |
| `exports` hides deep paths; dual package hazard; `npm init -y` writes `"type": "commonjs"`; `node --run` skips hooks | observed | |
| Built-in test runner fails a file on a floating rejection; mock timers | observed, documented | [MockTimers](https://nodejs.org/api/test.html#class-mocktimers) |
| Permission model: network restricted on newer lines only; not a sandbox | observed (22 and 25), documented | [Permissions](https://nodejs.org/api/permissions.html) |
| Release schedule and end-of-life dates | documented | [Node releases](https://nodejs.org/en/about/previous-releases), [release schedule](https://github.com/nodejs/Release) |

## Dependencies

| Claim | Status | Source |
|---|---|---|
| `npx` without a terminal installs and runs a missing package; `npm exec --no` refuses a new download but runs a package already in npx's cache; without `--`, npm takes the tool's flags | observed | |
| npm 11 runs dependency install scripts; pnpm 10 and npm 12 block them (pnpm 12 is the current release) | observed | [pnpm settings](https://pnpm.io/settings), community: [npm 12 release coverage](https://www.infoq.com/news/2026/08/npm-12-released/) |
| `min-release-age` unknown to npm 11.6 and ignored; pnpm `minimumReleaseAge` picks an older version | observed | [pnpm dependency resolution settings](https://pnpm.io/settings/dependency-resolution) |
| `npm ci` refuses drift; `npm install` rewrites the lock | observed | |
| `npm audit` misses a fresh compromise; signatures and provenance | observed, documented | [Trusted publishers](https://docs.npmjs.com/trusted-publishers), [Provenance](https://docs.npmjs.com/generating-provenance-statements) |
| 2025 compromises: runtime payload live about two hours; token-stealing install-script worms | community | [Compromised popular packages, September 2025](https://thehackernews.com/2025/09/20-popular-npm-packages-with-2-billion.html), [Shai-Hulud](https://wiz.io/blog/shai-hulud-npm-supply-chain-attack) |
| `engines` is advisory | observed | |
| `npm pack --dry-run` lists the tarball's files; published versions cannot be republished | documented | [npm pack](https://docs.npmjs.com/cli/commands/npm-pack), [package.json files](https://docs.npmjs.com/cli/configuring-npm/package-json#files), [unpublish policy](https://docs.npmjs.com/policies/unpublish) |

## Security

| Claim | Status | Source |
|---|---|---|
| A naive merge pollutes through `__proto__` and `constructor.prototype`; `--disable-proto=delete` misses the second | observed | [OWASP Prototype Pollution Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html), advisories [GHSA-jf85-cpcp-j695](https://github.com/advisories/GHSA-jf85-cpcp-j695), [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) |
| `startsWith(root)` accepts a sibling; symlinks escape; `relative` after `realpath` confines | observed | |
| An uncapped request body is a memory exhaustion vector | documented | [OWASP Denial of Service](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html) |
| `exec` interpolation injects; `execFile` does not; DEP0190; Windows batch files | observed, documented | [DEP0190](https://nodejs.org/api/deprecations.html#DEP0190), [April 2024 security releases](https://nodejs.org/en/blog/vulnerability/april-2024-security-releases) |
| `(a+)+` doubles per character; the experimental linear engine runs it in linear time; `RegExp.escape` on 24 and later | observed | |
| URL parser normalises case, whitespace and control characters; `//host` and `/\host` are absolute | observed (Node's WHATWG parser) | |
| HTML sinks run event-handler attributes | documented, not run in a browser | [innerHTML security considerations](https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML#security_considerations), [OWASP DOM XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html) |
| Trusted Types enforcement through CSP | community | [Trusted Types](https://web.dev/trusted-types) |
| Browser timer clamping | documented | [HTML timers](https://html.spec.whatwg.org/multipage/timers-and-user-prompts.html#timers) |
| `timingSafeEqual` requires equal lengths | observed, documented | [crypto.timingSafeEqual](https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b) |

## TypeScript

| Claim | Status | Source |
|---|---|---|
| Node runs `.ts` without type checking; strip-only limits and non-erasable syntax | observed | [Node TypeScript support](https://nodejs.org/api/typescript.html) |
| Casts, `any` and `!` compile under strict and fail at run time | observed (TS 7.0.2) | |
| `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` report the crashing lines | observed (TS 7.0.2) | [TSConfig reference](https://www.typescriptlang.org/tsconfig/) |
| `bundler` resolution passes `tsc` and fails in Node; `nodenext` reports missing extensions | observed | [Module resolution](https://www.typescriptlang.org/docs/handbook/modules/reference.html) |
| `strict` on by default and TS5112 from TypeScript 6; `node10` deprecated in 6, removed in 7 | observed (5.9.3, 6.0.3, 7.0.2) | community: [TypeScript 7 release coverage](https://www.infoq.com/news/2026/08/typescript-7-released/) |
| `tsc file.ts` ignores the tsconfig on TypeScript 5 | observed (5.9.3) | |
| `verbatimModuleSyntax` and `erasableSyntaxOnly` catch what stripping rejects | observed (TS1484, TS1294) | |
| A solution tsconfig (`files: []` with `references`) makes `tsc --noEmit -p .` check zero files; `tsc -b` reports the error | observed (7.0.2) | [Project references](https://www.typescriptlang.org/docs/handbook/project-references.html) |
| `rewriteRelativeImportExtensions` emits `./helper.js` for `./helper.ts` | observed (7.0.2) | |
| A thrown string's `e.message` is `undefined`; a thrown `null` crashes property access | observed | |

## Judgments not stated by the sources

- Running date tests in two zones on opposite sides of UTC is the skill's own proof standard.
- "Ask whether the platform already does it" before adding a dependency is the skill's own order.
