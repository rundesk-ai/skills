# Rust source basis

Checked against the Rust 1.99 documentation. Behavior marked *observed* was reproduced on
rustc, Cargo and Clippy 1.91.1, and re-run on 1.99.0 where the claim concerns a newer release; an
October 2026 audit compiled every example under both. Measurements are release-build medians of 7
to 51 runs with `black_box`, on an Apple M4 Max under macOS, unless marked otherwise. Language and tool contracts come from the Rust project's own
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
  no FFI). Observed on nightly-2025-05-18: a dangling `Vec` pointer reported as "has been freed, so
  this pointer is dangling"; `transmute::<u8, bool>(2)` as "encountered 0x02, but expected a
  boolean"; a foreign call stopped the whole test binary with "can't call foreign function".
- Observed: a read through a pointer into a `Vec` after a push printed a stale value without
  crashing; `transmute::<u8, bool>(2)` printed `false`.

## Async

- Tokio tutorial, [shared state](https://tokio.rs/tokio/tutorial/shared-state) (std `Mutex` is
  preferred; `Send` is computed from scopes) and [spawning](https://tokio.rs/tokio/tutorial/spawning)
  (`'static` and `Send` bounds). Observed on 1.91.1 in both editions: `drop(guard)` before `.await`
  leaves the future `!Send`; ending the scope with a block, or locking in a single `let` statement so
  the temporary guard drops at its semicolon, makes it `Send`.
- Tokio API docs (1.54): [`select!`](https://docs.rs/tokio/latest/tokio/macro.select.html)
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
  observed passing under `--workspace` and failing under `-p` with E0425); [resolver](https://doc.rust-lang.org/cargo/reference/resolver.html);
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
- [async-std 1.13.2](https://github.com/async-rs/async-std/releases): discontinued in favor of smol
  ([RUSTSEC-2025-0052](https://rustsec.org/advisories/RUSTSEC-2025-0052)).
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
  falls from 56.1% to 32.5%, and behavior changes behind an unchanged signature fare worst; retrieval of current
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

## Production traps (observed unless marked)

- Configuration as input: [Cloudflare outage of 18 November 2025](https://blog.cloudflare.com/18-november-2025-outage/)
  (a generated feature file past a preallocated limit of 200 reached `Result::unwrap()` in the
  proxy; the remediation treats generated configuration like user input). The keep-last-good
  reload was run.
- Lock incidents: [Fly.io, parking_lot](https://fly.io/blog/parking-lot-ffffffffffffffff/) and its
  [infra log](https://fly.io/infra-log/2024-12-14/) (an `if let` lock guard deadlocking a proxy fleet).
- Futurelock: [Oxide RFD 609](https://rfd.shared.oxide.computer/rfd/0609); reproduced as a hang with
  a pinned future in `select!`, fixed by spawning.
- Poisoning: one panic under a std `Mutex` made every later `lock().unwrap()` panic;
  `PoisonError::into_inner` recovered the data.
- Floats: `partial_cmp(..).unwrap_or(Equal)` over 1,000 inputs with `NaN` panicked 518 times and
  misordered 361 on 1.91; on 1.80 all 1,000 misordered ([Rust 1.81 sort changes](https://blog.rust-lang.org/2024/09/05/Rust-1.81.0/)).
  `0.1f32` summed ten million times gave 1,087,937.
- A manual `Ord` with a derived `PartialOrd`: on 1.91 and 1.99 alike, `sort()` ordered two values
  by the derived field order while a `BTreeSet` and `max` used the manual `Ord`; Clippy's
  `derive_ord_xor_partial_ord` denies it. (An earlier report of a difference between 1.91 and 1.99
  did not reproduce.)
- A lock guard taken in a `while let` condition was still held inside the body under edition 2024
  (a `try_lock` there failed); taking the value in its own `let` released it.
- `Ordering::Relaxed` publishing data: 25–34% stale reads on the M4; zero with `Release`/`Acquire`.
- `#[tokio::test]` default runtime passed a race that lost 39,800 of 80,000 updates under
  `multi_thread`; `block_in_place` panicked there ([attribute docs](https://docs.rs/tokio/latest/tokio/attr.test.html)).
- `spawn_blocking` under `timeout`: the timeout fired at 101 ms, exit waited 3.16 s; pool cap 512
  (tokio 1.54.1 source). `interval` fired five ticks within 20 ms after a 550 ms stall (`Delay`: one)
  ([`MissedTickBehavior`](https://docs.rs/tokio/latest/tokio/time/enum.MissedTickBehavior.html)).
- Channels: an unbounded channel peaked at 744 MB RSS against 15 MB bounded (200,000 × 4 KiB);
  `broadcast` lag ended a `while let Ok` loop; `rx.iter()` hung while `tx` lived; a `Drop` that
  joined a worker while holding its `Sender` deadlocked.
- `dashmap` 6.2.1: `get` then `insert` on the same key hung ([docs](https://docs.rs/dashmap/6.2.1/dashmap/struct.DashMap.html)).
- `tracing` 0.1.44: `Span::enter` across `.await` misattributed another task's event;
  `#[instrument]` logged a password argument ([`Span` docs](https://docs.rs/tracing/latest/tracing/struct.Span.html)).
- A 3 MiB future overflowed the stack in a debug build; `Box::pin` fixed it.
- `process::exit` left a `BufWriter<File>` empty; `env::args` panicked on non-UTF-8; `read_dir`
  returned unsorted names on APFS; `Vec::with_capacity` with 2^58 elements aborted and with 2^61
  panicked "capacity overflow".
- JSON: Node read 9007199254740993 as ...992; `serde_json::Value` turned 18446744073709551616 into a
  float; an `untagged` enum took the first fitting variant and dropped a field.
- Proof gaps: `cargo check` passed a const-generic `assert!` that `cargo build` rejected (E0080); a
  `compile_fail,E0308` doctest passed on stable with E0499; nextest retries exit 0 on a flaky test
  ([retries](https://nexte.st/docs/features/retries/)); test capture missed `writeln!(io::stdout())`.
- Rust-SWE-bench ([arXiv 2602.22764](https://arxiv.org/abs/2602.22764)): reproducing the issue first
  mattered most for agents.

## Organization

- [The Reference, modules](https://doc.rust-lang.org/reference/items/modules.html) (`mod.rs`
  discouraged; E0761 observed); [Cargo SemVer guide](https://doc.rust-lang.org/cargo/reference/semver.html#item-new)
  (glob imports; E0659 observed); [API guidelines, naming](https://rust-lang.github.io/api-guidelines/naming.html);
  [`links`](https://doc.rust-lang.org/cargo/reference/build-scripts.html#the-links-manifest-key).
- Observed: `pub(crate)` restoring dead-code warnings; a `#[cfg(test)]` helper invisible to
  `tests/` (E0425) and the `test-util` feature fix; two versions of a public dependency's type
  (E0308); an optional dependency creating a public feature; the `Result<T, E = Error>` alias.
- [Large Rust Workspaces](https://matklad.github.io/2021/08/22/large-rust-workspaces.html),
  [cargo-xtask](https://github.com/matklad/cargo-xtask) (an `xtask ci` run observed),
  [Fast Rust Builds](https://matklad.github.io/2021/09/04/fast-rust-builds.html),
  [Inline in Rust](https://matklad.github.io/2021/07/09/inline-in-rust.html),
  [rust-analyzer architecture](https://rust-analyzer.github.io/book/contributing/architecture.html),
  [Microsoft Pragmatic Rust Guidelines checklist](https://microsoft.github.io/rust-guidelines/guidelines/checklist/index.html)
  (M-DONT-LEAK-TYPES, M-TEST-UTIL, M-FROM-ERROR, M-SMALLER-CRATES, M-NO-GLOB-REEXPORTS).

## Performance

All observed on the M4 Max, stable 1.91.1, unless marked; code in the benchmark sources of the audit.

- Workflow: discarded and constant-folded benchmark loops timed 0 ms; criterion reported a 1.7%
  "improvement" on unchanged code; one build measured 111 ms alone and 65 ms interleaved; a
  stripped binary profiled as bare addresses in Instruments. [Perf Book profiling](https://nnethercote.github.io/perf-book/profiling.html),
  [benchmarking](https://nnethercote.github.io/perf-book/benchmarking.html),
  [criterion baselines](https://bheisler.github.io/criterion.rs/book/user_guide/command_line_options.html).
- The counting-allocator test failed with 1,000 allocations when one `write!` became `to_string()`.
- Release profile on a serde_json, hashing and sorting workload: `codegen-units = 1` −15%; thin LTO
  0%; fat LTO −4%; `panic = "abort"` −7%; `opt-level = 2` +7%, `"s"` +30%; `target-cpu=native` 0%;
  PGO +8–12% matched, −9% mismatched ([rustc PGO](https://doc.rust-lang.org/rustc/profile-guided-optimization.html),
  [cargo-pgo](https://github.com/Kobzol/cargo-pgo)). Binary size 2.76 → 1.25 MB with strip, LTO,
  `panic = "abort"` and `opt-level = "z"` (a clap, serde_json and regex CLI). mimalloc 1.4–1.65x.
  [Perf Book build configuration](https://nnethercote.github.io/perf-book/build-configuration.html).
- `#[inline]` across crates without LTO: 4.5x for a function with `assert!`, none for a tiny leaf
  ([rust-lang/rust#116505](https://github.com/rust-lang/rust/pull/116505)); `#[cold]` −13%.
- Code: clone vs borrow 107x (17x in debug); Fx vs SipHash 5.7x (1.4x in debug); buffer reuse 1.7x
  and 4.7x; lazy iteration 2.9x; `fs::read` + `memchr` 6.5x over `lines()`; `memchr` 22x and
  `memmem` 12x; `get_mut`-then-insert 1.8x over `entry(to_string())`; `with_capacity` 1.7x/1.5x;
  `Box<dyn Fn>` 13x; boxed large variant 22x; struct of arrays 15.5x; flat grid 1.46x;
  `chunks_exact(2)` 3.7x; 16 `f32` accumulators 7.9x; `sort_by_cached_key` 5x; `lexical-core`
  9.5x for integer formatting; typed struct 2.6x over `Value`; `&str` fields 1.2x and the
  escaped-string failure ([serde lifetimes](https://serde.rs/lifetimes.html)); sort stability
  timings; `SmallVec` spill. [memchr](https://github.com/BurntSushi/memchr),
  [json-benchmark](https://github.com/serde-rs/json-benchmark).
- Concurrency: false sharing 1,687 / 76 / 36 / 5.4 ms ([`CachePadded`](https://docs.rs/crossbeam-utils/latest/crossbeam_utils/struct.CachePadded.html));
  shared `Arc::clone` about 700x; rayon 255x slower on 1,000 items, fixed by `with_min_len`;
  `block_on` hot loop 24–61x slower than in a spawned task ([Tokio preemption](https://tokio.rs/blog/2020-04-preemption));
  per-thread accumulation 280–630x faster than per-item `Mutex` or atomic; a contended atomic
  2.2x slower than a `Mutex`.
- `[profile.dev.package."*"] opt-level = 3`: sha2 7.7x, regex 3.1x, serde_json 1.3x
  ([Cargo profile overrides](https://doc.rust-lang.org/cargo/reference/profiles.html#overrides)).
  Cargo 1.99 disables incremental builds under `CI` ([cargo#17220](https://github.com/rust-lang/cargo/pull/17220)).
- stdout: one million lines by `println!` 0.4–1.5 s, locked about the same, `BufWriter` 16–19 ms.

## Versions 1.86–1.99

Each replacement in the version table compiled on 1.99.0; release notes from
[RELEASES.md](https://github.com/rust-lang/rust/blob/master/RELEASES.md) and [releases.rs](https://releases.rs/).
`CARGO_BUILD_WARNINGS=deny` was observed to be ignored on 1.91. `cargo +<version>` installed a
missing toolchain without asking.

## Added after an independent review

- [Criterion FAQ](https://bheisler.github.io/criterion.rs/book/faq.html): `harness = false`, and
  "Unrecognized option" when a libtest target receives Criterion's flags.
- [`unexpected_cfgs`](https://doc.rust-lang.org/rustc/check-cfg/cargo-specifics.html) and
  cross-target `cargo check`; [minimal versions](https://doc.rust-lang.org/cargo/reference/unstable.html#minimal-versions)
  and [cargo-hack](https://github.com/taiki-e/cargo-hack) `--version-range`.
- [`result_large_err`](https://rust-lang.github.io/rust-clippy/master/index.html#result_large_err);
  [winnow](https://docs.rs/winnow) and [nom](https://docs.rs/nom).
- Restriction lints and the `clippy.toml` test allowances were observed to fire and be silenced as
  described.

## Write it once

The write-once rules come from the cleanup history of a private multi-project C# simulation (2026-10), where about two dozen review rounds found formulas retyped in several files, a lookup copied three times with two tolerances, mirror-image methods, view code re-deriving model rules, outputs published with no reader, and replaced paths left behind, although its instructions already said to search before writing new logic. They are stack-neutral; the tooling line below is this language's.

- Observed with rustc 1.91.1 (2021 edition) on a library crate: an unused parameter and a never-read private field warned, an unused `pub(crate)` function warned, and an unused `pub` function did not.
