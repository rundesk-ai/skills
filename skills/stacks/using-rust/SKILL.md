---
name: using-rust
description: Use when writing, reviewing, debugging, refactoring, organizing, optimizing, or building Rust, including compile errors such as borrow-checker, lifetime, trait-bound and `Send` errors, error handling and panics, traits and public APIs, module and workspace layout, async and Tokio, threads, atomics and channels, unsafe and FFI, Cargo features, choosing a crate, editions and toolchains, profiling, benchmarking and release-build performance, clippy, and cargo test. It supplies Rust defaults with paired do and do-not examples, measured performance trade-offs, traps that pass tests and fail in production, version-aware checks, and the commands that prove a change. Do not use it for another language that only calls Rust through bindings, or for merely installing a Rust-built tool.
---

# Use Rust

Fix the design the compiler is objecting to, not the error message; prove every change with the
checks the project itself runs; and never trust your memory of an API, a crate, or a version.

## Establish the environment before changing code

```sh
rustup show                                    # active toolchain, and which file pinned it
cargo -V
cargo metadata --no-deps --format-version 1    # members, edition, rust-version, features
```

Read the CI workflow too: CI is what "green" means for this repository.

The edition and `rust-version` decide which syntax and std APIs exist. Writing past the floor
compiles on your toolchain and breaks for everyone pinned below it. Do not raise the edition or
`rust-version` without approval. Read [editions and versions](references/editions-and-versions.md)
before using any feature you are not sure the floor allows.

## Work in this order

1. **Record a baseline** (`cargo check`, `clippy`, `test`) on the untouched tree, and reproduce the
   failure with the narrowest command (`cargo test -p <crate> <test_name>`). Without the baseline,
   "it was already failing" is a guess.
2. **Read the real API.** Your recall of a crate is versioned to your training, not to this
   `Cargo.lock`. Measured on real models, success on APIs that changed after the cutoff falls from
   56% to 33%, and same-signature behavior changes are the worst. Read the locked version's source under
   `$CARGO_HOME/registry/src` or build its docs with `cargo doc -p <crate>`.
3. **Do not reinvent a solved problem, and do not add a crate std already covers.** Reuse what
   `Cargo.toml` already depends on, then std, then the community's established crate for the job (read
   [ecosystem](references/ecosystem.md)); a hand-written argument parser, date calculation, retry
   loop or secret comparison repeats bugs those crates fixed. Verify a new crate exists first: `cargo info <crate>`, or let `cargo add <crate>` resolve the version. In one
   study about a fifth of crate names models produced did not exist, most within a few letters of
   a real one — a hallucinated or typo-squatted crate is a supply-chain risk, not a compile error.

## Verify with the commands that actually cover the code

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
```

Use the project's own scope and flags when CI defines them. Four traps waste a run or hide a failure:

- `cargo clippy` without `--all-targets` never lints `#[cfg(test)]` code, `tests/`, benches or
  examples.
- `cargo test --all-targets` **skips doctests** — it means lib, bins, tests, benches and examples.
  Plain `cargo test` runs them. A test runner other than Cargo's (nextest) never runs doctests either,
  so pair it with `cargo test --doc`.
- Features unify across a workspace: a test can pass under `--workspace` because a sibling crate
  enabled a feature, and fail under `-p <crate>` or when published. Check each publishable crate
  alone, and with `--no-default-features` when it has features.
- Only one Cargo process builds a target directory at a time. "Blocking waiting for file lock" is
  another build (often the editor's) holding it, not a hang — wait, or give a parallel job its own
  `CARGO_TARGET_DIR`. Killing it, or running cargo jobs concurrently in one tree, wastes the build.

Read [Cargo and verification](references/cargo-and-verification.md) for workspaces, features, the
lockfile, build scripts, lint configuration and CI.

## Defaults and the failures they prevent

| Prefer | Avoid | Failure prevented |
|---|---|---|
| Shorten the borrow, split the struct, `mem::take`, indices instead of references | `.clone()`, `Rc<RefCell<_>>`, `Arc<Mutex<_>>` added to silence the borrow checker | copies hiding a design error; `RefCell` turning a compile error into a runtime panic |
| Structs that own their data | lifetime parameters added to fix a borrow error | `'a` spreading through every type; values that cannot be returned or stored |
| `Result` and `?`; `expect("why this cannot fail")` only for an invariant | `.unwrap()` outside tests and prototypes | a malformed input crashing the process |
| A library's own error enum (`Send + Sync + 'static`) | `anyhow` or `Box<dyn Error>` in a library's public API | callers unable to match on failure kinds or send errors across tasks |
| `T::try_from(x)?`, `checked_*` or `saturating_*` arithmetic | `as` for narrowing casts; arithmetic that overflows | silent truncation; overflow that panics in debug and wraps in release |
| Iterators: `iter()`, `zip`, `enumerate`, `windows`, `chunks` | `for i in 0..v.len()` indexing `v[i]` | off-by-one panics and bounds checks the iterator never needs |
| An exhaustive `match` | a `_` arm on an enum you own | a new variant compiling with no handling |
| `let _guard = lock()`; `?` on a fallible call | `let _ = lock()` or `let _ = fallible()` | the guard dropping at once; an error discarded silently |
| Fix the code; `#[expect(lint, reason = "...")]` when a lint is wrong here | a bare `#[allow]` | a suppression that outlives its reason |
| End a lock guard's **scope** before `.await` | a guard alive across `.await`, or `drop(guard)` as the fix | a future that is not `Send`, or a deadlock |
| No `unsafe`; when needed, the smallest block with a `// SAFETY:` comment | `unsafe` to satisfy the compiler, `transmute`, `static mut` | undefined behavior that tests pass straight through |

Do not bring the shape of another language with you: inheritance hierarchies become enums or
traits (never `Deref` to a "parent" type, which fakes inheritance and leaks the parent's whole
API), getters and setters on every field become plain data, and null becomes `Option`.

## Traps that compile, pass tests, and fail in production

| Trap | Failure | Instead |
|---|---|---|
| `.unwrap()` on configuration, a feature file or any reloaded input "we generate ourselves" | one bad push panics every instance at once | treat it as input: return an error, keep serving the last good version |
| `lock().unwrap()` in a long-running service | after one panic under the lock, every later request panics | recover with `unwrap_or_else(PoisonError::into_inner)` where the data stays valid, or `parking_lot` |
| `sort_by(\|a, b\| a.partial_cmp(b).unwrap_or(Equal))` on floats | panics since 1.81 ("does not correctly implement a total order"), or silently misorders | `sort_by(f64::total_cmp)` |
| a hand-written `Ord` beside a derived `PartialOrd` | `sort()` and `<` use one order, `BTreeSet`, `max` and `cmp` the other | derive both, or `partial_cmp` returns `Some(self.cmp(other))` |
| `while let Some(x) = queue.lock().unwrap().pop()`, or `match` on a locked value | the guard lives for the whole body, in every edition; a second lock inside deadlocks | take the value in its own `let` statement, then branch |
| `Ordering::Relaxed` on the flag that publishes data | readers see the flag and stale data on ARM; x86 tests pass | `Release` to set, `Acquire` to read |
| `#[tokio::test]` for concurrent code | the default single-threaded runtime hides races and lost updates | `#[tokio::test(flavor = "multi_thread")]` |
| `select!` on a pinned future while another arm awaits | hangs forever under load | spawn it and select on the `JoinHandle` |
| `unbounded_channel` with a slow consumer | memory grows until the process is killed | a bounded channel |
| `process::exit` after writing through a `BufWriter` | the file is empty | return an `ExitCode` from `main`, or flush first |
| `Vec::with_capacity(n)` with `n` read from input | an abort `catch_unwind` cannot catch | check `n` against the bytes actually present |
| a `u64` ID sent as a JSON number to a browser | IDs above 2^53 change by one | serialize IDs as strings |

The rest are in the references below, each with its reproduction.

## Performance is measured, never assumed

Make Rust fast in this order: a release build, a profile that names the hot function, a
`black_box`ed benchmark against a saved baseline, one change at a time, both numbers reported and
the output diffed. The common wins, measured: stop allocating per item (reuse buffers, borrow
instead of `clone`, keep iterators lazy, read files as bytes); a faster hasher for keys an attacker
does not control; `codegen-units = 1`; data laid out for the loop that reads it; per-thread
accumulation instead of shared atomics. Several popular moves measured zero or worse on the
workload measured (`sort_unstable` on nearly sorted data, `par_iter` on small inputs, thin LTO, and
on Apple Silicon `target-cpu=native`), so measure each on yours. Read
[performance](references/performance.md) before claiming a speedup.

## Read only what the task needs

- Code for the defaults table above, or for the error and API rules — each as a do and a do-not
  pair: [idioms](references/idioms.md). Read it with the rule's own reference, not instead of it.
- Text, paths, files, stdout, child processes, floats, collections, time, or data from outside the
  program: [std edge cases](references/std-edge-cases.md).
- A job a crate may already solve (CLI, serialization, HTTP, dates, logging, shutdown, crypto, test
  tooling), or an old crate to replace: [ecosystem](references/ecosystem.md).
- A borrow, lifetime, error-type, trait or public API question: [ownership, errors and
  APIs](references/ownership-errors-and-apis.md).
- Adding a module, crate, workspace member, binary or feature, or a build slowed by the crate
  graph: [organization](references/organization.md).
- Async, Tokio, threads, locks, atomics or channels: [async and
  concurrency](references/async-and-concurrency.md).
- Any `unsafe`, FFI, raw pointers or `Send`/`Sync` impls: [unsafe](references/unsafe.md).
- Making code faster, profiling, benchmarking, release-profile settings, or slow builds:
  [performance](references/performance.md).
- Writing or repairing tests, or deciding what proves a change: [tests](references/tests.md).
- Auditing or updating a claim in this skill: [sources](references/sources.md).

## Report findings with evidence

Cite the compiler error, clippy lint, failing test, benchmark or Miri report that proves each
defect; a finding that is only "this looks wrong" goes last, labeled as such.
