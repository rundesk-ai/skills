---
name: using-rust
description: Use when writing, reviewing, debugging, refactoring, or building Rust, including borrow-checker and lifetime errors, error handling and panics, traits and public APIs, async and Tokio, unsafe and FFI, Cargo workspaces, features, choosing a crate, editions and toolchains, clippy, and cargo test. It supplies Rust defaults with paired do and do-not examples, the established crate for each common job, std edge cases, version-aware checks to run before trusting a change, and the traps agents characteristically fall into. Do not use it for another language that only calls Rust through bindings, or for merely installing a Rust-built tool.
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

Then read `rust-toolchain.toml`, the root `Cargo.toml` (`[workspace]`, `resolver`,
`[workspace.dependencies]`, `[workspace.lints]`, `[profile.*]`), each touched member's `edition`,
`rust-version` and `[features]`, any `clippy.toml`, `rustfmt.toml`, `deny.toml` or
`.cargo/config.toml`, and the CI workflow — CI is what "green" means for this repository.

The edition and `rust-version` decide which syntax and std APIs exist. Let chains need edition 2024
and Rust 1.88; `#[expect]` needs 1.81; edition 2024 itself needs 1.85. Writing past the floor
compiles on your toolchain and breaks for everyone pinned below it. Do not raise the edition or
`rust-version` without approval. Read [editions and versions](references/editions-and-versions.md)
before using any feature you are not sure the floor allows.

## Work in this order

1. **Record a baseline.** Run `cargo check`, `cargo clippy` and `cargo test` on the untouched tree
   first. Without it you cannot tell a failure you caused from one that was already there, and the
   tempting assumption that a failure was "pre-existing" is how regressions get waved through.
2. **Reproduce** the failure with the narrowest command: `cargo test -p <crate> <test_name>`.
3. **Read the real API.** Your recall of a crate is versioned to your training, not to this
   `Cargo.lock`. Measured on real models, APIs that changed after the cutoff fail about twice as
   often, and same-signature behavior changes are the worst. Read the locked version's source under
   `$CARGO_HOME/registry/src` or build its docs with `cargo doc -p <crate>`.
4. **Fix the cause** (see the defaults below), then run the verification loop.
5. **Do not reinvent a solved problem, and do not add a crate std already covers.** Reuse what
   `Cargo.toml` already depends on, then std, then the community's established crate for the job (read
   [ecosystem](references/ecosystem.md)); a hand-written argument parser, date calculation, retry
   loop or secret comparison repeats bugs those crates fixed. Verify a new crate exists first: `cargo info <crate>`, or let `cargo add <crate>` resolve the version. In one
   study about a fifth of crate names models produced did not exist, most within a few letters of
   a real one — a hallucinated or typo-squatted crate is a supply-chain risk, not a compile error.
   Update one crate with `cargo update -p <crate> --precise <ver>`, never the whole lockfile.

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
| `&str`, `&[T]`, `&T`, `&Path` parameters | `&String`, `&Vec<T>`, `&Box<T>` | callers forced to allocate |
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

## Read only what the task needs

- Code for the defaults table above, or for the error and API rules — each as a do and a do-not
  pair: [idioms](references/idioms.md). Read it with the rule's own reference, not instead of it.
- Text, paths, files, stdout, child processes, floats, collections or time: [std edge
  cases](references/std-edge-cases.md).
- A job a crate may already solve (CLI, serialization, HTTP, dates, logging, shutdown, crypto, test
  tooling), or an old crate to replace: [ecosystem](references/ecosystem.md).
- A borrow, lifetime, error-type, trait or public API question: [ownership, errors and
  APIs](references/ownership-errors-and-apis.md).
- Async, Tokio, threads, locks or channels: [async and concurrency](references/async-and-concurrency.md).
- Any `unsafe`, FFI, raw pointers or `Send`/`Sync` impls: [unsafe](references/unsafe.md).
- Writing or repairing tests, measuring performance, or slow builds: [tests and
  performance](references/tests-and-performance.md).
- Auditing or updating a claim in this skill: [sources](references/sources.md).

## Report findings with evidence

```text
[HIGH] std MutexGuard held across .await makes the handler future !Send
Location: src/server/session.rs:142
Evidence: `cargo check` fails at tokio::spawn with "future cannot be sent between threads safely".
Fix: read the value inside a block so the guard's scope ends before the await.
Check: the spawn compiles, and `cargo clippy --all-targets` reports no await_holding_lock.
```

Separate defects from preferences. Cite the compiler error, clippy lint, failing test or Miri
report that proves a defect; a finding that is only "this looks wrong" goes last, labeled as such.
