# Performance and memory

Read this when a script is slow, runs out of memory, or a worker's memory climbs. Measure first:
`hrtime(true)` for time, `memory_get_usage()` and `memory_get_peak_usage()` for memory, at two input
sizes. Time that quadruples when the input doubles is quadratic.

Numbers below were measured on PHP 8.4 (arm64, OPcache off unless stated); read them as ratios.

## Costs worth knowing

| Pattern | Measured | Instead |
|---|---|---|
| `$all = array_merge($all, $chunk)` in a loop | 21 ms at 2,000 chunks, 377 ms at 8,000 | collect the chunks, then `array_merge(...$chunks)` once (0.2 ms) |
| `in_array($id, $list)` inside a loop over 1,000 ids, 100,000 times | 60 ms | `isset($set[$id])` on `array_flip($list)`: 0.8 ms |
| Loading 10 million ints into an array to sum them | 257 MB peak | a generator (`yield`): 1 MB flat, about 20% slower per element |
| `array_key_exists` unqualified in a namespaced file | 1.7 times slower than `isset` | `\array_key_exists`, which the compiler optimizes, or `isset` when null is not a value |

Not worth changing: `.=` in a loop (equal to collecting and `implode`), and passing arrays by reference
(copy-on-write already avoids the copy).

## Large inputs

Read files and query results row by row: `fgetcsv` in a loop, `SplFileObject`, a generator over
`PDOStatement::fetch()`, rather than `file()` or `fetchAll()`. `memory_limit` defaults to 128 MB; an export
that "only fails in production" usually loaded everything into one array.

## Long-running processes

A request-per-process server frees everything after each request and hides leaks. A queue worker or a
persistent application server does not:

- A `static` or global cache keyed by id grew 16 MB per 10,000 entries of 1 KB and was never released.
  Bound it (size limit or LRU), clear it per job, or key per-object data with a `WeakMap`, whose entries
  disappear with the object (100,000 discarded objects left one entry).
- Reference cycles are freed by the cycle collector; with it disabled, 200,000 two-object cycles held
  145 MB until `gc_collect_cycles()`. Do not disable it.
- Request state stored in statics, singletons or globals is still there for the next request. Reset it
  at the start of each job.
- Log `memory_get_usage()` every N jobs: a flat line proves the fix. Restart workers after a fixed number
  of jobs as a backstop, not a fix.

## OPcache and JIT

OPcache is on for the web server and off on the command line by default (`opcache.enable_cli=0`), and
the JIT is disabled unless configured. Enabling the tracing JIT made a pure floating-point loop about ten
times faster and an array, JSON and sorting workload no faster at all; it helps CPU-bound numeric code,
not typical web or I/O work. Benchmark with the same OPcache settings production uses.
