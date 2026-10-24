# Node

Read this when the code runs under Node: a server, a CLI, a script, a worker, or a package other code
installs.

## The event loop is shared by every request

Synchronous work blocks every request in the process, not just the one that caused it: parsing an 18 MB
JSON body took about 70 ms, during which nothing else ran. A chain of `await` or `queueMicrotask` with no
real I/O starves timers and sockets just as a `while` loop does.

Measure before moving work around:

```js
import { monitorEventLoopDelay } from 'node:perf_hooks';
const delay = monitorEventLoopDelay({ resolution: 10 });
delay.enable();
// ... run the load ...
console.log('max ms', delay.max / 1e6, 'p99 ms', delay.percentile(99) / 1e6);
```

Then stream or chunk the work, yield with `await new Promise((r) => setImmediate(r))` between chunks, or
move it to a worker pool. `node --cpu-prof` writes a `.cpuprofile` that names the hot function; open it in
a browser's dev tools.

## Streams and backpressure

- `readable.pipe(writable)` does not destroy the source when the destination fails: the source stays
  paused and its file descriptor or socket leaks. Use `await pipeline(source, ...transforms, destination)`
  from `node:stream/promises`, which destroys every stream and rejects once.
- `write()` returns `false` when the buffer is full. Ignoring it buffered 125 MB in one test; waiting for
  `drain` held it at the high-water mark:

```js
import { once } from 'node:events';
for (const row of rows) {
  if (!out.write(row)) await once(out, 'drain');
}
```

- A V8 string tops out near 512 MB, so `readFile(..., 'utf8')` followed by `JSON.parse` cannot handle a
  larger file at all. Process it a record at a time with `for await` over a stream, or `pipeline` with
  `async function*` transforms, which keep backpressure.

## Process exit and shutdown

- `process.exit()` right after writing output truncates it when stdout is a pipe: 1 MB written, 64 KB
  arrived through `| cat`, all of it into a file. CI and other tools read through pipes. Set
  `process.exitCode` and let the process end.
- Exit code 137 is `SIGKILL`, usually a container's out-of-memory kill: no stack trace, no heap error.
  143 is `SIGTERM` with no handler, which an orchestrator may count as a failure.
- Graceful shutdown: on `SIGTERM`, stop accepting connections with `server.close()` (since Node 19 it
  also closes idle keep-alive sockets and waits for in-flight requests), set a hard timeout with
  `setTimeout(...).unref()` that calls `server.closeAllConnections()`, and set `process.exitCode`. As PID
  1 in a container Node gets no default signal handling, so a missing handler means the container is
  killed after its grace period; register the handler, or run under an init process (`docker run --init`).

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

- `npm init -y` writes `"type": "commonjs"`, so `import` in a `.js` file of a fresh project fails until
  it is changed to `"module"` (or the file is renamed `.mjs`).
- `require()` of an ES module works on current lines and returns the namespace, so
  `const fn = require('esm-pkg'); fn()` fails: the default export is `.default`. Top-level `await`
  anywhere in that module's graph makes `require()` throw `ERR_REQUIRE_ASYNC_MODULE`, so adding one to a
  library is a breaking change for CommonJS consumers.
- A package's `exports` field hides every path it does not list (`ERR_PACKAGE_PATH_NOT_EXPORTED`); import
  only the documented entry points. Adding `exports` to your own package is a breaking change.
- A package that ships separate CommonJS and ESM builds loads twice when both are used in one process:
  `instanceof` fails across them and module-level singletons exist twice.
- Dynamic `import()` takes a URL, so an absolute Windows path (`C:\…`) fails; convert with
  `pathToFileURL(path).href` from `node:url`.
- `node --run script` skips the `pre` and `post` scripts that `npm run` runs.

## Installs and publishing

- Dependency install scripts: npm 11 runs them silently. pnpm from version 10 and npm from version 12
  block them unless the package is allowed (`pnpm approve-builds`; `allowScripts` in `package.json` for
  npm). Allow only packages that need a native build, and never switch the policy off. On npm 11,
  `--ignore-scripts` stops them.
- A release-age gate skips versions published in the last day or so: pnpm `minimumReleaseAge`, npm
  `min-release-age` from 11.10, or `npm install --before=<date>` on any version. On pnpm it silently picks
  an older version rather than failing. Script blocking would not have stopped the 2025 compromise of
  widely used packages, whose payload ran at run time; a one-day gate would have, since the bad versions
  were live for about two hours.
- When a dependency change adds many transitive packages to the lockfile, say how many and why.
- Before publishing, `npm pack --dry-run` lists every file the tarball will contain. Without a `files`
  allow-list in `package.json`, tests, fixtures and a stray `.env` ship, and a published version cannot
  be taken back.

## The permission model

`node --permission` with `--allow-fs-read=<dir>` denies file reads outside that directory and child
processes. It restricts network access only on newer lines (Node 22 let `fetch` through), follows
symlinks out of granted paths, and is not inherited by workers. It is a seat belt for your own code, not
a sandbox for untrusted code.

## Testing

`node --test` needs no dependency. Mock the clock instead of sleeping:
`t.mock.timers.enable({ apis: ['setTimeout', 'Date'], now })`, then `t.mock.timers.tick(ms)`.
