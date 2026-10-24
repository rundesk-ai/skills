# Tests

Read this when writing or repairing Rust tests, when a test is flaky, or when deciding what proves
a change.

## Where tests go

- **Each file in `tests/` compiles as its own crate and binary**, so many files multiply link time;
  one `tests/<name>/main.rs` with modules is faster. A binary-only crate cannot be tested by import:
  move its logic into `lib.rs`. Helpers that `tests/` needs from the crate: see the `test-util`
  feature in [organization](organization.md).
- **Doctests** run only for library targets, and only under plain `cargo test` or `cargo test --doc`.
  Mark an example `no_run` when it must compile but not execute, and give `ignore` a reason.

## Traps

**`#[should_panic]` without `expected`.** It passes on *any* panic, including an index out of bounds
before the code under test runs. Always write `#[should_panic(expected = "...")]`, or better, return
a `Result` and assert on the error.

**Shared state.** Tests in one binary run in parallel threads. Environment variables, the working
directory, fixed ports and fixed file paths make them order-dependent. `-- --test-threads=1` confirms
the diagnosis; the fix is a temporary directory, an ephemeral port, or passing configuration in.

**Snapshot tests.** With `insta`, review every changed snapshot (`cargo insta review`) instead of
accepting them wholesale. Accepting blindly turns a regression into the new expected output.

**Output a test cannot see.** Test capture intercepts `println!` and `eprintln!` only: a
`writeln!(io::stdout())` or a child process writes straight to the terminal, so `--nocapture`
is not what decides whether it shows.

**A green retry is a hidden flake.** cargo-nextest retries mark a test `FLAKY` and still exit 0.
Pass `--flaky-result fail` in CI (nextest 0.9.131+), or fix the flake.

**`compile_fail` doctests check less than they say.** On stable, a ```` ```compile_fail,E0308 ````
block passes when the code fails with any error — it passed with E0499. Only nightly checks the
code. To test that misuse fails to compile for the right reason, use `trybuild`, which compares
the compiler's message.

**`cargo check` is not `cargo build`.** Errors raised during monomorphization, such as a
const-generic `assert!` on `N`, pass `cargo check` and fail `cargo build` with E0080. Before
reporting that generic or const code compiles, build or test it.

Async tests: see `#[tokio::test]` in [async and concurrency](async-and-concurrency.md).
