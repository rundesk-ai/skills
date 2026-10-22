# Rust source basis

Checked against the Rust 1.99 documentation. Behavior marked *observed* was reproduced on
rustc, Cargo and Clippy 1.91.1. Language and tool contracts come from the Rust project's own
documentation; traps come from maintainers, tool documentation and published measurements of model
output. Read this when a claim in the skill is challenged or a new Rust release may have changed it.

## Language, editions and std

- [Rust Edition Guide, 2024](https://doc.rust-lang.org/edition-guide/rust-2024/index.html): 2024 is
  stable from 1.85; RPIT lifetime capture and `use<..>`; `if let` and tail-expression temporary
  scopes (observed: `match` still holds a guard across arms); `static_mut_refs` denied (observed);
  `unsafe_op_in_unsafe_fn`; `unsafe extern`; unsafe attributes; `set_var` and `remove_var` unsafe;
  never-type fallback; `gen` reserved; merged doctests.
- [The Rust Book, ch. 9.3](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html) for
  when to panic and how `expect` states an invariant; [ch. 3.2](https://doc.rust-lang.org/book/ch03-02-data-types.html)
  for overflow panicking in debug and wrapping in release (observed); [ch. 15.5](https://doc.rust-lang.org/book/ch15-05-interior-mutability.html)
  for `RefCell` panicking at runtime.
- [The Rust Reference](https://doc.rust-lang.org/reference/): `as` numeric semantics (observed:
  `300u64 as u8` is 44, `NaN as i32` is 0); `#[non_exhaustive]`; dyn compatibility, formerly object
  safety.
- std docs: [`Error`](https://doc.rust-lang.org/std/error/trait.Error.html) (the source goes in
  `source()` or `Display`, not both); [`transmute`](https://doc.rust-lang.org/std/mem/fn.transmute.html)
  ("the absolute last resort") and its alternatives; [`forget`](https://doc.rust-lang.org/std/mem/fn.forget.html)
  (destructors are not guaranteed); [`Mutex`](https://doc.rust-lang.org/std/sync/struct.Mutex.html)
  (poisoning, the unwrap idiom); [`thread::scope`](https://doc.rust-lang.org/std/thread/fn.scope.html).
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/): C-GOOD-ERR, C-SEND-SYNC,
  C-CALLER-CONTROL, C-STRUCT-PRIVATE, C-CUSTOM-TYPE, C-NEWTYPE, C-GETTER, C-CONV, C-CONV-TRAITS,
  C-COMMON-TRAITS, C-DEBUG, C-STRUCT-BOUNDS, C-FAILURE, C-EXAMPLE.
- [thiserror README](https://github.com/dtolnay/thiserror): typed errors for library-like code,
  anyhow for application-like code. The comparison is in thiserror's README, not anyhow's docs.
- Rust blog: [1.45](https://blog.rust-lang.org/2020/07/16/Rust-1.45.0/) (float-to-int `as`
  saturates); [async fn in traits](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)
  (the `Send` problem and `impl Future + Send`); [1.81](https://blog.rust-lang.org/2024/09/05/Rust-1.81.0/)
  (`#[expect]`, observed to error when unfulfilled under `-D warnings`); [1.84](https://blog.rust-lang.org/2025/01/09/Rust-1.84.0/)
  (MSRV-aware resolver); [1.85](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/) (edition 2024).
- [Common Rust Lifetime Misconceptions](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md):
  `T: 'static` means owned; `&'a mut self` with the struct's lifetime locks it.
- [Rust Design Patterns: clone to satisfy the borrow checker](https://rust-unofficial.github.io/patterns/anti_patterns/borrow_clone.html)
  and [`mem::take`](https://rust-unofficial.github.io/patterns/idioms/mem-replace.html); anti-patterns
  [`#![deny(warnings)]`](https://rust-unofficial.github.io/patterns/anti_patterns/deny-warnings.html)
  and [`Deref` polymorphism](https://rust-unofficial.github.io/patterns/anti_patterns/deref.html).

## Unsafe

- [The Rustonomicon](https://doc.rust-lang.org/nomicon/): unsafety is non-local and privacy is the
  boundary ("Working with Unsafe"); hand-written `Send` and `Sync` ("Send and Sync").
- [std-dev-guide safety comments](https://std-dev-guide.rust-lang.org/policy/safety-comments.html):
  `// SAFETY:` on every block, `# Safety` on every `unsafe fn`.
- [Miri](https://github.com/rust-lang/miri): what it detects, and its limits (only executed paths,
  no FFI). Miri was not available on the auditing machine; its claims rest on its documentation.
- Observed: a read through a pointer into a `Vec` after a push printed a stale value without
  crashing; `transmute::<u8, bool>(2)` printed `false`.

## Async

- Tokio tutorial, [shared state](https://tokio.rs/tokio/tutorial/shared-state) (std `Mutex` is
  preferred; `Send` is computed from scopes) and [spawning](https://tokio.rs/tokio/tutorial/spawning)
  (`'static` and `Send` bounds). Observed on 1.91.1 in both editions: `drop(guard)` before `.await`
  leaves the future `!Send`; ending the scope with a block, or locking in a single `let` statement so
  the temporary guard drops at its semicolon, makes it `Send`.
- Tokio API docs (1.53): [`select!`](https://docs.rs/tokio/latest/tokio/macro.select.html)
  cancellation safety and the pinned-future pattern; [`Mutex`](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html);
  [`JoinHandle`](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html) detaching on drop
  and returning a task's panic as `JoinError`; [`spawn`](https://docs.rs/tokio/latest/tokio/task/fn.spawn.html)
  requiring `Send` on every runtime flavor;
  [`spawn_blocking`](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).
- Alice Ryhl, [Async: what is blocking?](https://ryhl.io/blog/async-what-is-blocking/) (10–100µs
  between awaits; `spawn_blocking` versus rayon) and [Actors with Tokio](https://ryhl.io/blog/actors-with-tokio/)
  (actor shape; cycles of bounded channels deadlock).

## Cargo, Clippy and tests

- The Cargo Book: [`cargo test`](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
  (`--all-targets` excludes doctests, observed; stops at the first failing binary);
  [features](https://doc.rust-lang.org/cargo/reference/features.html) (additive, unification —
  observed passing under `-p` and failing under `--workspace`); [resolver](https://doc.rust-lang.org/cargo/reference/resolver.html);
  [specifying dependencies](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)
  (caret ranges; member `default-features` from 1.99); [lints](https://doc.rust-lang.org/cargo/reference/lints.html)
  and the [manifest `[lints]` table](https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section)
  (workspace lints are opt-in per member, observed); [profiles](https://doc.rust-lang.org/cargo/reference/profiles.html)
  (root only); [build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html)
  (`rerun-if-changed` narrows reruns, observed); [`build.warnings`](https://doc.rust-lang.org/cargo/reference/config.html#buildwarnings)
  (Cargo 1.97); [CI guide](https://doc.rust-lang.org/cargo/guide/continuous-integration.html);
  [FAQ](https://doc.rust-lang.org/cargo/faq.html) and the [2023 lockfile post](https://blog.rust-lang.org/2023/08/29/committing-lockfiles/).
- [rustup overrides](https://rust-lang.github.io/rustup/overrides.html) and [rustup 1.28.1](https://blog.rust-lang.org/2025/03/04/Rustup-1.28.1/)
  (automatic toolchain install restored).
- [The Clippy book](https://doc.rust-lang.org/clippy/) and [usage](https://doc.rust-lang.org/clippy/usage.html):
  lint groups, `restriction` never wholesale, `build.warnings` recommended over `-Dwarnings` because
  the latter invalidates caches (observed). Observed defaults on 1.91.1: `ptr_arg`, `borrowed_box`,
  `await_holding_lock` warn and `not_unsafe_ptr_arg_deref` denies; `unwrap_used`,
  `undocumented_unsafe_blocks`, `cast_possible_truncation` and `redundant_clone` are off. Clippy
  without `--all-targets` skipped a test module (observed).
- [cargo-nextest](https://nexte.st/docs/running/) (no doctests); [cargo-hack](https://github.com/taiki-e/cargo-hack);
  [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks) (and what it misses);
  [cargo-deny](https://embarkstudios.github.io/cargo-deny/); [RustSec](https://rustsec.org/);
  [insta](https://insta.rs/docs/quickstart/).
- [rust-analyzer configuration](https://rust-analyzer.github.io/book/configuration.html):
  `cargo.targetDir` to stop the editor holding the build lock. Two concurrent builds in one project
  were observed to block on the lock.
- Observed: `#[should_panic]` without `expected` passed on an unrelated index panic.
- [The Rust Performance Book](https://nnethercote.github.io/perf-book/build-configuration.html):
  release versus debug speed; LTO and codegen units; [heap allocations](https://nnethercote.github.io/perf-book/heap-allocations.html).
- matklad, [Fast Rust Builds](https://matklad.github.io/2021/09/04/fast-rust-builds.html) (generic
  shims, proc macros at the leaves; its `RUSTFLAGS` advice is superseded) and
  [Delete Cargo Integration Tests](https://matklad.github.io/2021/02/27/delete-cargo-integration-tests.html)
  (one integration binary).

## Idioms, edge cases and the ecosystem

- Every **Good** block in [idioms](idioms.md), [std edge cases](std-edge-cases.md) and the async
  reference was compiled under `cargo clippy --all-targets -- -D warnings` on 1.91.1 (observed),
  with thiserror 2, anyhow 1, toml 1, regex 1, clap 4, tokio 1 and tokio-util current in October 2026.
- Observed on 1.91.1: `Path::new("/data").join("/etc/passwd")` is `/etc/passwd` and Clippy warns
  `join_absolute_paths`; `"é".len()` is 2 and `&s[0..1]` panics; `-7 % 3` is `-1`, `rem_euclid` 2;
  `read_to_string` keeps the newline; `extension()` of `archive.tar.gz` is `gz`; a `spawn` with no
  `wait` warns `zombie_processes`; `println!` piped into `head` panics with "Broken pipe".
- std docs: [`Child`](https://doc.rust-lang.org/std/process/struct.Child.html) (no `Drop`, zombies,
  pipe deadlock), [`BufWriter`](https://doc.rust-lang.org/std/io/struct.BufWriter.html) (errors on
  drop are ignored), [`f64::total_cmp`](https://doc.rust-lang.org/std/primitive.f64.html#method.total_cmp),
  [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html) (random order, SipHash),
  [`SystemTime`](https://doc.rust-lang.org/std/time/struct.SystemTime.html) (not monotonic),
  [`Path::join`](https://doc.rust-lang.org/std/path/struct.Path.html#method.join).
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/) idioms: borrowed types for
  arguments, `mem::take`, constructors, `Default`; and [blessed.rs](https://blessed.rs/crates) for
  the community's established crate per job.
- [async-std 1.13.1](https://github.com/async-rs/async-std/releases): discontinued in favor of smol.
  [RUSTSEC-2025-0068](https://rustsec.org/advisories/RUSTSEC-2025-0068) (`serde_yml` unsound and
  archived) and RUSTSEC-2025-0067 (its `libyml` dependency); `serde_yaml` was deprecated by its author
  in 2024. Unmaintained: `dotenv` RUSTSEC-2021-0141, `backoff` RUSTSEC-2025-0012, `instant`
  RUSTSEC-2024-0384, `proc-macro-error` RUSTSEC-2024-0370, `rustls-pemfile` RUSTSEC-2025-0134.
  `tempfile` 3.27 `persist` renames without syncing (read in its source).
- [tokio-util `CancellationToken`](https://docs.rs/tokio-util/latest/tokio_util/sync/struct.CancellationToken.html)
  and Tokio's [graceful shutdown](https://tokio.rs/tokio/topics/shutdown) guide.

## How models fail at Rust

- [Crate hallucination study](https://arxiv.org/abs/2606.08444): 22% of crate references across six
  models did not exist, most within five edits of a real name, many treating std modules as crates;
  self-refinement barely helped, so verification has to be by tool.
- [RustEvo²](https://arxiv.org/abs/2503.16922): success on APIs changed after the training cutoff
  roughly halves, and behavior changes behind an unchanged signature fare worst; retrieval of current
  docs recovers part of the gap.
- [Translation compile-error study](https://arxiv.org/html/2505.10708v2) and
  [repair study](https://arxiv.org/html/2504.15254v3): trait, type and invented-method errors dominate
  (E0277, E0308, E0599); borrow errors (E0499, E0502) are common; compiler feedback repairs most of
  them, and `unsafe` appeared despite instructions, mostly for global mutable state.
- Practitioner reports: [users.rust-lang.org](https://users.rust-lang.org/t/using-ai-to-generate-rust-code/128758)
  (clone and unwrap, outdated dependencies, degradation under loops of fixes) and the
  [axum 0.8 release](https://tokio.rs/blog/2025-01-01-announcing-axum-0-8-0) as an example of a
  major-version API change recalled wrongly.
- Agent rules files read for recurring rules: [Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/agents/index.html)
  (re-exports under old paths, tautological tests, other languages' shapes, `#[expect]`);
  [uv](https://github.com/astral-sh/uv/blob/main/AGENTS.md) (never assume a failure was already there;
  precise updates; exhaustive matches); [rust-analyzer](https://github.com/rust-lang/rust-analyzer/blob/master/AGENTS.md)
  (new `pub` items and dependencies are design decisions); [Zed](https://github.com/zed-industries/zed/blob/main/.rules)
  (`let _ =` on fallible calls); [Codex at commit 4875084](https://github.com/openai/codex/blob/4875084025582f9443afeb907e2aa20644241dda/AGENTS.md)
  (scoped commands, waiting on the Cargo lock, `bool` parameters).
