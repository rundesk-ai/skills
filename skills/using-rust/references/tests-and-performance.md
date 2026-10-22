# Tests and performance

Read this when writing or repairing Rust tests, when a test is flaky, when making a performance
claim, or when builds are slow.

## Where tests go

- **Unit tests** sit beside the code in `#[cfg(test)] mod tests` and can reach private items.
- **Integration tests** in `tests/` see only the public API, and each file compiles as its own crate
  and binary. Many files multiply link time; one `tests/<name>/main.rs` with modules is faster. Share
  helpers through `tests/common/mod.rs`. A binary-only crate cannot be tested by import — move its
  logic into `lib.rs`.
- **Doctests** run only for library targets, and only under plain `cargo test` or `cargo test --doc`.
  Mark an example `no_run` when it must compile but not execute, and give `ignore` a reason.

## Traps

**`#[should_panic]` without `expected`.** It passes on *any* panic, including an index out of bounds
before the code under test runs. Always write `#[should_panic(expected = "...")]`, or better, return
a `Result` and assert on the error.

**Tests that restate the code.** A test that asserts a constant equals itself, or that mirrors the
implementation line by line, passes whatever the code does. Assert on behavior a caller would notice.

**Shared state.** Tests in one binary run in parallel threads. Environment variables, the working
directory, fixed ports and fixed file paths make them order-dependent. `-- --test-threads=1` confirms
the diagnosis; the fix is a temporary directory, an ephemeral port, or passing configuration in.

**Snapshot tests.** With `insta`, review every changed snapshot (`cargo insta review`) instead of
accepting them wholesale. Accepting blindly turns a regression into the new expected output.

**Proof that a test works:** break the code under test and watch the test fail for the right reason,
then restore it. A test never seen failing has not been shown to test anything.

## Performance

- **Never time a debug build.** Release is often 10 to 100 times faster, and also drops overflow
  checks, so debug and release differ in behavior as well as speed. Measure with `--release` or a
  benchmark harness.
- **Measure before and after with the same tool**, one change at a time, and report both numbers. A
  benchmark that caches results or runs cases in parallel measures the harness, not the code.
- Allocation is the usual cost: hot-loop `clone`, `collect` into a `Vec` only to iterate again,
  `format!` in a loop, and growing a `Vec` without `with_capacity` when the size is known. Profile to
  find which one before changing code.
- `[profile.release]` options — `lto`, `codegen-units = 1`, a custom allocator, `target-cpu=native` —
  trade compile time or portability for speed. Benchmark each, and do not set `target-cpu=native`
  for a binary that ships to other machines. `panic = "abort"` is a behavior change, not a tuning
  knob: destructors stop running on panic and `catch_unwind` stops catching, so set it only with
  approval.

## Slow builds

- `cargo build --timings` writes an HTML report of which crates take the time.
- Generic functions at crate boundaries are compiled again in every caller. Keep a thin generic shim
  that converts its arguments and calls a non-generic inner function.
- Heavy procedural macros (`serde` derive, `syn`) low in the crate graph serialize everything above
  them. Keep them at the leaves.
- Alternating feature sets, `RUSTFLAGS` or lint flags between runs throws away the incremental cache.
  Keep one set of flags per target directory.
- Do not run release builds when nobody asked for one; a debug check loop is much faster.
