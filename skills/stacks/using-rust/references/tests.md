# Tests

Read this when writing or repairing Rust tests, when a test is flaky, or when deciding what proves
a change.

## Where tests go

- **Each file in `tests/` compiles as its own crate and binary**, so many files multiply link time;
  one `tests/<name>/main.rs` with modules is faster. On macOS it is far worse: the system scans
  every freshly linked executable on its first run, and an edit relinks every test binary. With 42
  test files, an edit plus one test took 97 s, about 72 s of it the scan; merged into one crate
  plus one acceptance crate, 14 s. Adding the terminal or agent app under System Settings ›
  Privacy & Security › Developer Tools exempts what it starts (a 67 MB test binary's first start
  went from 0.40 s to 0.01 s); `spctl developer-mode enable-terminal` shows the pane, and the app
  needs a relaunch. That is the owner's machine setting: suggest it, never change it.
  A binary-only crate cannot be tested by import: move its logic into `lib.rs`. Helpers that `tests/` needs from the crate: see the `test-util`
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

**Two runs of `#[sqlx::test]` against one Postgres server destroy each other.** Each test's
database is named from a hash of the test's path, and an existing one of that name is dropped
first, so the owner's run and an agent's (or two agents') delete each other's databases mid-test and
fail with 23505 on `pg_database_datname_index`. Run the tests only through a project script that
takes one machine-wide lock first: `flock` on Linux; macOS has no `flock(1)`, so use perl's `flock`
on a file descriptor the shell holds open.

**cargo-llvm-cov's per-file summary can report a covered line as missed.** Each test binary and
each generic instantiation is a separate copy of a function, and the summary counts, per function,
the best-covered copy, so a line run only in another copy shows as missed while the lcov output and
`--show-missing-lines` list nothing. Cover the line within one binary, ideally with a unit test in
the same module.

Async tests: see `#[tokio::test]` in [async and concurrency](async-and-concurrency.md).
