# Node

Read this when the code runs under Node: a server, a CLI, a script, a worker, or a package other code
installs.

## The event loop is shared by every request

Synchronous work blocks every request in the process, not just the one that caused it. Parsing an 18 MB
JSON body takes about 70 ms; a regular expression that backtracks can take seconds; `fs.*Sync`,
synchronous crypto and a long loop do the same. A chain of `await` or `queueMicrotask` with no real I/O
starves timers and sockets just as a `while` loop does.

Measure before moving work around:

```js
import { monitorEventLoopDelay } from 'node:perf_hooks';
const delay = monitorEventLoopDelay({ resolution: 10 });
delay.enable();
// ... run the load ...
console.log('max ms', delay.max / 1e6, 'p99 ms', delay.percentile(99) / 1e6);
```

Then stream or chunk the work, yield with `await new Promise((r) => setImmediate(r))` between chunks, or
move it to a worker pool. `node --cpu-prof` writes a profile that names the hot function.

## Streams and backpressure

- `readable.pipe(writable)` does not destroy the source when the destination fails: the source stays
  paused and its file descriptor or socket leaks. Use `pipeline` from `node:stream/promises`, which
  destroys every stream and rejects once:

```js
import { pipeline } from 'node:stream/promises';
import { createReadStream, createWriteStream } from 'node:fs';
import { createGzip } from 'node:zlib';
await pipeline(createReadStream('in.log'), createGzip(), createWriteStream('in.log.gz'));
```

- `write()` returns `false` when the buffer is full. Ignoring it buffered 125 MB in one test; waiting for
  `drain` held it at the high-water mark:

```js
import { once } from 'node:events';
for (const row of rows) {
  if (!out.write(row)) await once(out, 'drain');
}
```

- `pipeline` with `async function*` transforms and `for await` over a readable keep backpressure; they
  are the simplest way to process a large file one record at a time. A V8 string tops out near 512 MB,
  so `readFile(..., 'utf8')` followed by `JSON.parse` cannot handle a larger file at all.

## Process exit and shutdown

| Situation | Exit code |
|---|---|
| Uncaught exception, or an unhandled rejection (the default since Node 15) | 1 |
| `SIGTERM` with no handler | 143 |
| `SIGKILL`, including a container out-of-memory kill | 137, with no stack trace |

- `process.exit()` right after writing output truncates it when stdout is a pipe: 1 MB written, 64 KB
  arrived through `| cat`, all of it into a file. CI and other tools read through pipes. Set
  `process.exitCode` and let the process end.
- A fire-and-forget promise needs its own `.catch`, or one failure ends the process.
- Graceful shutdown: on `SIGTERM`, stop accepting connections with `server.close()` (since Node 19 it
  also closes idle keep-alive sockets and waits for in-flight requests), set a hard timeout with
  `setTimeout(...).unref()` that calls `server.closeAllConnections()`, and set `process.exitCode`.
  Running as PID 1 in a container, Node gets no default signal handling.

## Memory

- The default heap limit is not the machine's memory: about 4 GB on a 64-bit machine, and sized from the
  container limit inside one. `node -p "v8.getHeapStatistics().heap_size_limit / 2**20"` prints it.
- `--max-old-space-size=512` sets the old generation only (the heap limit came out at 704 MB), and
  buffers live outside the heap. A value at or above the container's limit turns a catchable heap error
  into a kill. `--max-old-space-size-percentage` sizes it from the available memory.
- Closures created in the same scope share one context: a small long-lived callback keeps alive whatever
  any sibling closure captured (2.7 MB grew to 41 MB in a test). Move the large value into its own
  function, or set it to `null` when done.
- A `Map` used as a cache keyed by request objects grew to 158 MB; a `WeakMap` held 3 MB. Key per-object
  data with a `WeakMap`; give a string-keyed cache a size limit.
- To find a leak: `node --heapsnapshot-signal=SIGUSR2 app.js`, then `kill -USR2 <pid>` twice some time
  apart and compare the snapshots' retainers in a browser's dev tools.
  `--heapsnapshot-near-heap-limit=1` writes one just before an out-of-memory crash.

## Worker threads

A worker keeps the main thread free; it does not make one task faster (a 14 ms computation took 13 ms in
a warm worker). Starting one costs about 10 ms, so use a fixed pool, never a worker per request. Sending
an object graph clones it on the sending thread (200,000 small objects took 62 ms, as long as parsing
them), so send raw bytes and parse in the worker. Transfer an `ArrayBuffer` instead of copying it (64 MB:
5.6 ms to copy, 0.02 ms to transfer), and do not touch it afterwards: the sender's copy is detached and
reads as empty.

## Modules

- A `.js` file is CommonJS unless the nearest `package.json` says `"type": "module"`. `npm init -y`
  writes `"type": "commonjs"`, so `import` in a fresh project fails until it is changed. `.mjs` and
  `.cjs` override the field.
- ES modules have no `__dirname`; use `import.meta.dirname` and `import.meta.filename`. Importing JSON
  needs `with { type: 'json' }`.
- `require()` of an ES module works on current lines and returns the namespace, so
  `const fn = require('esm-pkg'); fn()` fails: the default export is `.default`. Top-level `await`
  anywhere in that module's graph makes `require()` throw `ERR_REQUIRE_ASYNC_MODULE`, so adding one to a
  library is a breaking change for CommonJS consumers.
- A package's `exports` field hides every path it does not list (`ERR_PACKAGE_PATH_NOT_EXPORTED`); import
  only the documented entry points. Adding `exports` to your own package is a breaking change.
- A package that ships separate CommonJS and ESM builds loads twice when both are used in one process:
  `instanceof` fails across them and module-level singletons exist twice.
- `node --run script` skips `pre` and `post` scripts that `npm run` runs.

## Lockfiles and installs

- `npm ci` and `pnpm install --frozen-lockfile` refuse a lock that does not match `package.json`;
  `npm install` silently rewrites the lock. Use the frozen form in CI and in reproductions, and read the
  lockfile diff of any dependency change (count the new transitive packages).
- Dependency install scripts: npm 11 runs them silently; pnpm 10 and npm 12 block them unless the
  package is allowed (`pnpm approve-builds`; npm `allowScripts` in `package.json`). Allow only packages
  that need a native build. On npm 11, `--ignore-scripts` stops them.
- A release-age gate (pnpm `minimumReleaseAge`, npm 11.10 and later `min-release-age`, or
  `npm install --before=<date>`) skips versions published in the last day or so. Script blocking would not
  have stopped the 2025 compromise of widely used packages, whose payload ran at run time; a one-day
  gate would have, since the bad versions were live for about two hours.
- `npm audit signatures` verifies registry signatures; `npm view <pkg> dist.attestations` shows
  provenance.

## The permission model

`node --permission` with `--allow-fs-read=<dir>` denies file reads outside that directory and child
processes. It restricts network access only on newer lines (Node 22 let `fetch` through), follows
symlinks out of granted paths, and is not inherited by workers. It is a seat belt for your own code, not
a sandbox for untrusted code.

## Testing with the built-in runner

`node --test` runs `*.test.js` files without a dependency. A test that leaves a promise rejecting after it
ends fails its file ("asynchronous activity after the test ended"), which catches the floating rejections
above. Mock timers and the clock instead of sleeping:

```js
import test from 'node:test';
test('debounce fires once', (t) => {
  t.mock.timers.enable({ apis: ['setTimeout', 'Date'], now: new Date('2026-03-08T06:59:00Z') });
  // ... call the debounced function several times ...
  t.mock.timers.tick(1000);
});
```
