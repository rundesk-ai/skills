# Performance

Read this before making Rust faster, claiming a speedup, choosing release-profile settings, or when
builds are slow. The numbers are release-build medians measured on one Apple Silicon machine
(method in [sources](sources.md)); the ratios carry over, the absolute times do not. Several
popular optimizations measured as zero or negative, and they are listed with the rest.

## Measure first, and measure the right thing

1. **Never time a debug build.** Debug distorts the ranking as well as the speed: a faster hasher
   gained 1.4x in debug and 5.7x in release, and removing a clone 17x and 107x. A script that times
   `cargo run` without `--release` is measuring the wrong program.
2. **Profile before changing code.** Use samply or `cargo flamegraph` (`perf` on Linux, Instruments
   on macOS). Profile a build with symbols — a stripped binary shows bare addresses:

   ```toml
   [profile.profiling]
   inherits = "release"
   debug = "line-tables-only"
   strip = false
   ```

   Build with `cargo build --profile profiling`, adding `RUSTFLAGS="-C force-frame-pointers=yes"`
   for profilers that unwind by frame pointers. Code inlined into its caller is billed to the
   caller, so a hot `main` usually means a hot helper.
3. **Benchmark with a harness** (`criterion`, `divan`), with inputs passed through
   `std::hint::black_box`. **A loop that measures sub-nanosecond had its work deleted:** a discarded
   result timed 0 ms, and `(0..n).map(|x| x * 3).sum()` became a closed formula even with `n`
   black-boxed. Black-box the input, consume the output, and check the time scales with `n`.
4. **Compare against a saved baseline and ignore small deltas.** `cargo bench --bench <name> --
   --save-baseline before`, change one thing, then `--baseline before`. Criterion needs
   `harness = false` in the `[[bench]]` entry, and without `--bench <name>` the flag also reaches
   the library's libtest harness, which fails with "Unrecognized option". Criterion reported an unchanged
   rerun as a significant 1.7% "improvement"; treat changes under about 3% as noise.
5. **Interleave variants.** The same build measured 111 ms in one run and 65 ms over three
   interleaved rounds. Alternate A, B, A, B and report medians.
6. **Read the assembly before "fixing" bounds checks or vectorization.** `cargo asm` (cargo-show-asm)
   or `cargo rustc --release -- --emit asm`: an indexed loop the compiler had already vectorized
   gained 0% from re-slicing.
7. **Diff the output before and after.** A faster wrong answer is a regression.

## Lock in "no allocation" with a test

Allocation is the usual hidden cost, and a counting allocator makes "this path does not allocate" a
test that fails the day someone adds a `to_string()`. Put it in its own `tests/` file, since the
global allocator is process-wide:

```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::cell::Cell;

struct Counting;
thread_local! { static ALLOCS: Cell<usize> = const { Cell::new(0) }; }

unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 {
        let _ = ALLOCS.try_with(|c| c.set(c.get() + 1));
        // SAFETY: forwards the caller's layout unchanged to the system allocator.
        unsafe { System.alloc(l) }
    }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) {
        // SAFETY: `p` was allocated by `System` with this layout, in `alloc` or `realloc`.
        unsafe { System.dealloc(p, l) }
    }
    unsafe fn realloc(&self, p: *mut u8, l: Layout, n: usize) -> *mut u8 {
        let _ = ALLOCS.try_with(|c| c.set(c.get() + 1));
        // SAFETY: as for `dealloc`; `n` is the caller's new size.
        unsafe { System.realloc(p, l, n) }
    }
}

#[global_allocator]
static A: Counting = Counting;

fn allocs_during(f: impl FnOnce()) -> usize {
    let before = ALLOCS.with(Cell::get);
    f();
    ALLOCS.with(Cell::get) - before
}

#[test]
fn render_does_not_allocate_once_warm() {
    let rows: Vec<(u32, u32)> = (0..1000).map(|i| (i, i * 2)).collect();
    let mut out = String::new();
    mycrate::render_into(&mut out, &rows); // the first call grows the buffer
    assert_eq!(allocs_during(|| mycrate::render_into(&mut out, &rows)), 0);
}
```

## Release profile, measured

| Setting | Effect on a JSON, hashing and sorting workload | Decision |
|---|---|---|
| `codegen-units = 1` | −15% time; build time doubled | the first setting to try for a shipped binary |
| `lto = "thin"` | 0% | not worth it alone |
| `lto = "fat"` | −4%; nothing on top of `codegen-units = 1` | measure before keeping |
| `panic = "abort"` | another −7% | a behavior change: destructors stop running on panic and `catch_unwind` stops catching. Only with approval |
| `opt-level = 2` / `"s"` | 7% / 30% slower, binary barely smaller | keep 3 for speed; `"s"`/`"z"` only when size is the goal |
| `-C target-cpu=native` | 0% on Apple Silicon | and the binary may crash with an illegal instruction on another machine; never for a shipped binary |
| PGO (`cargo pgo`) | +8–12% when the profile was recorded under the same profile settings; −9% when reused from another | regenerate the profile whenever the profile settings change, and train on realistic input |
| `strip = true`, LTO, `opt-level = "z"`, `panic = "abort"` | binary 2.76 MB → 2.22 MB stripped → 1.25 MB with all four | for size, not speed |

A faster allocator (mimalloc) gained 1.4–1.65x on an allocation-heavy loop on macOS; the gap is
reported larger against musl's allocator. Reducing allocations comes first.

**`#[inline]` across crates** matters only without LTO, and only for a small public function that
contains an `assert!`, indexing or a call: adding it gave 2.6–4.5x. Tiny leaf functions are
already inlined across crates, and `lto = "thin"` closed every gap. `#[cold]` on an
error-formatting path gave 13%.

## Code changes, measured

| Instead of | Do | Measured |
|---|---|---|
| `clone()` of a `String` or `Vec` per item | borrow | 107x |
| `format!` per row; a new `Vec` per iteration | one buffer, `clear()`, `write!` / `extend` | 1.7x; 4.7x |
| `collect()` into a `Vec` only to iterate it again | keep the iterator lazy | 2.9x |
| `for line in reader.lines()` | `fs::read` then `memchr` over bytes; or `read_line` into one reused `String` | 6.5x; 1.4x. `BufReader` capacity changed nothing |
| `iter().position(|&b| b == x)`; `windows(n).any(..)` | `memchr`, `memchr::memmem::Finder` | 22x; 12x |
| `HashMap` with the default SipHash on keys an attacker does not choose | `FxHashMap` (`rustc-hash`) | 3.5x inserts, 5.7x `u64` lookups, 2.2x `String` lookups |
| `entry(word.to_string())` on a hit-heavy map | `get_mut(word)`, and insert an owned key only on a miss | 1.8x |
| `HashMap::new()` / `Vec::new()` when the size is known | `with_capacity` | 1.7x / 1.5x |
| a `Box<dyn Fn>` or `Box<dyn Trait>` per element | a generic `F: Fn`, or an enum | 13x (the dyn call blocked vectorization); enum vs `Box<dyn>`: 4.1x to build |
| an enum with one large variant | `Box` the large variant (`large_enum_variant` warns) | enum 264 → 16 bytes; 22x faster to iterate |
| an array of structs when the hot loop reads one field | a separate column (struct of arrays) | 15.5x for a sum |
| `Vec<Vec<T>>` grid | one flat `Vec` with a row stride, traversed row by row | 1.5x; column order was 2.2x slower |
| indexing `a[2 * i]`, `a[2 * i + 1]` | `chunks_exact(2)` | 3.7x, now vectorized; `get_unchecked` gained only 11% |
| one accumulator summing `f32` | 8–16 independent accumulators over `chunks_exact` | 7.9x, and less rounding error. `std::simd` was no faster; a single fused-multiply-add chain was slower |
| `sort_by_key` with an allocating key | `sort_by_cached_key` | 5x |
| `to_string()` / `write!` for numbers in a hot output path | `itoa`, `ryu` or `lexical-core` | 9.5x for integers, 4x for floats. Parsing gained nothing over std `parse` |
| a large error type inside `Result` | box the error (`clippy::result_large_err` reports it) | every `Result` is as large as its error, so the success path copies it too |
| `serde_json::Value` for data with a known shape | a typed struct | 2.6x. Borrowed `&str` fields gained 1.2x but fail on any escaped string; use `Cow<'a, str>` with `#[serde(borrow)]` |

**Sorting:** `sort_unstable` was faster on random data (55 vs 77 ms) and slower on nearly sorted
data (49 vs 31 ms). Measure on realistic input before switching. **Small collections:**
`SmallVec<[T; 4]>` was 3.6x faster than `Vec` for three items and slower than `Vec::with_capacity`
once it spilled to the heap; size the inline capacity from the real distribution, or use
`ArrayVec` when there is a hard bound.

## Concurrency, measured

- **Per-thread accumulation, not a shared counter.** A `Mutex` or atomic updated per item in a
  parallel loop was 280–630x slower than per-thread sums, and 45x slower than one thread; on this
  ARM machine a contended `fetch_add` was even 2.2x slower than a `Mutex`. Separate counters per
  thread still collide when they share a cache line: adjacent atomics took 1,687 ms, padded to 64
  bytes 76 ms, `crossbeam_utils::CachePadded` (128 bytes on Apple Silicon, where 64 is not enough)
  36 ms, a local accumulator written once 5.4 ms.
- **`Arc::clone` in a hot loop is a contended atomic.** Eight threads cloning one `Arc` per
  iteration were about 700x slower than passing `&T`. Clone once per task, borrow inside the loop.
- **Rayon on tiny work is slower than one thread.** `par_iter` over 1,000 cheap items was 255x
  slower than sequential; `with_min_len(1024)` fixed it. On 200,000 moderate items plain
  `par_iter` was already best.
- **Tokio: run the hot loop in a spawned task, not in `block_on`.** The `block_on` future runs
  outside the worker pool: a channel ping-pong ran 24–61x faster inside `tokio::spawn`. For
  connection-bound I/O, `current_thread` was 1.2x faster than the multi-threaded runtime; measure
  before assuming more threads help.
- JSON into a DOM: `sonic-rs` was 6.4x faster than `serde_json::Value`; into typed structs no JSON
  crate beat `serde_json` by more than 10%.

## Slow builds

- `cargo build --timings` writes an HTML report of which crates take the time; see
  [organization](organization.md) for shaping the crate graph.
- Generic functions at crate boundaries are compiled again in every caller. Keep a thin generic shim
  that converts its arguments and calls a non-generic inner function.
- Heavy procedural macros (`serde` derive, `syn`) low in the crate graph serialize everything above
  them. Keep them at the leaves.
- Debug builds of heavy dependencies make tests and tools slow:
  `[profile.dev.package."*"] opt-level = 3` made a SHA-256 loop 7.7x and a regex 3.1x faster while
  rebuilding your own crate stays fast. Generic code such as serde's is compiled in your crate's
  profile and gains little (1.3x).
- Alternating feature sets, `RUSTFLAGS` or lint flags between runs throws away the incremental
  cache. Keep one set of flags per target directory. Cargo 1.99 disables incremental compilation
  when `CI` is set.
- Do not run release builds when nobody asked for one; a debug check loop is much faster.
