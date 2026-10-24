# Cargo and verification

Read this when changing `Cargo.toml`, a workspace, features, dependencies, a build script or lint
configuration, or when a check passes in one place and fails in another.

## Toolchain selection

`rust-version` never selects a toolchain; it only makes Cargo refuse an older one. A pinned
`rust-toolchain.toml` is installed automatically, so the first command in a pinned repository may
spend minutes downloading, and `cargo +1.80.0 check` silently installs a toolchain that is missing;
remove a floor toolchain you added only to check the floor.

## The full loop

Run cheapest first and stop at the first failure:

```sh
cargo fmt --all --check
cargo check --workspace --all-targets --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features            # includes doctests; never add --all-targets
cargo doc --workspace --no-deps                  # broken intra-doc links
```

- **Denying warnings.** From Cargo 1.97, prefer `CARGO_BUILD_WARNINGS=deny cargo clippy ...` or
  `[build] warnings = "deny"` in `.cargo/config.toml`. Passing `-D warnings` after `--`, or through
  `RUSTFLAGS`, changes the build fingerprint, so switching between a plain build and a deny build
  rechecks the workspace — and `RUSTFLAGS` rebuilds every dependency. Below 1.97, `-- -D warnings` is
  the only option: an older Cargo silently ignores `CARGO_BUILD_WARNINGS=deny` and reports green
  with the warning still there. Check `cargo -V` before relying on it.
- **`cargo test` stops at the first failing test binary.** Add `--no-fail-fast` to see every failure
  before deciding what broke.
- **Features.** `--all-features` alone misses breakage with defaults off and with single features.
  For a crate with features, add `cargo check --no-default-features` and, where installed,
  `cargo hack check --each-feature --no-dev-deps`.
- **In CI**, build with `--locked` so a stale `Cargo.lock` fails rather than being silently rewritten.
- **Code behind `cfg` for another target is never compiled on yours.** A `#[cfg(windows)]` branch
  can be broken for months. Check it with `rustup target add x86_64-pc-windows-msvc` and
  `cargo check --target x86_64-pc-windows-msvc`. Keep `unexpected_cfgs` (on since 1.80) at warn or
  deny, so a misspelled feature or cfg name is reported instead of silently compiling the code out;
  declare custom cfgs in `[lints.rust] unexpected_cfgs = { level = "warn", check-cfg = [...] }`.
- **The lower bound of a version requirement is never tested** by an ordinary build, which resolves
  the newest. Before publishing a library, check it with `cargo +nightly update -Z minimal-versions`
  then `cargo check`, or `cargo hack --version-range`.

## Features

Features must be **additive**: enabling one may add capability, never remove it or change behavior,
because Cargo builds each dependency once with the union of every feature any crate in the graph
asked for.

- `default-features = false` does not guarantee the defaults are off: any other crate enabling them
  wins. Find out who with `cargo tree -e features -i <crate>`.
- Mutually exclusive features break `--all-features` and unification. Prefer separate crates or a
  runtime choice; if unavoidable, fail the bad combination with `compile_error!`.
- Removing a feature, or making one non-additive, is a breaking change.

## Dependencies and the lockfile

- **Version requirements are caret ranges.** `"1.2"` means `>=1.2.0, <2.0.0`, and `"0.2"` means
  `<0.3.0`. Write all three components of the version whose API you actually use: depending on an
  API added in 1.2.5 while declaring `"1.2"` works with today's lockfile and breaks for a consumer who
  resolves 1.2.0.
- **`Cargo.lock` is committed by default, libraries included** — `cargo new` no longer ignores it.
  The older "libraries should not commit it" rule was withdrawn. Follow the repository's choice.
- Change one dependency at a time: `cargo update -p <crate> --precise <version>`. A bare
  `cargo update` rewrites the whole graph and turns a small change into an unreviewable one.
- `cargo tree -d` lists crates present in several versions; `cargo tree -i <crate>` shows who pulls
  one in. Each duplicate costs compile time and binary size.
- Where the project uses them, `cargo deny check` (advisories, licenses, bans) or `cargo audit`
  (RustSec advisories) belong in the loop after a dependency change.

## Workspaces

- **`[workspace.lints]` is not inherited implicitly.** Each member needs `[lints] workspace = true`, or
  it silently runs with defaults.
- Profiles are read only from the workspace root; a `[profile]` in a member or dependency is ignored.
- A virtual workspace must set `resolver`; see [editions and versions](editions-and-versions.md).

## Lints

- **Fix first.** When a lint is wrong for a specific line, use `#[expect(lint, reason = "...")]`: it
  warns once the lint stops firing, so a dead suppression cannot linger. Use `#[allow]` where the lint
  fires only under some features or `cfg`s, since an unfulfilled `#[expect]` is an error under
  `-D warnings`.
- Never enable Clippy's `restriction` group as a whole: its lints contradict each other. Projects
  commonly pick these from it in `[workspace.lints.clippy]`: `unwrap_used`, `dbg_macro`, `todo`,
  `print_stdout` (libraries), `clone_on_ref_ptr` (so `Arc::clone(&a)` shows the cheap copy),
  `undocumented_unsafe_blocks` and `large_futures`. `unwrap_used` and `print_stdout` also fire in
  tests unless `clippy.toml` sets `allow-unwrap-in-tests = true` and `allow-print-in-tests = true`.
- When enabling a group with exceptions in `[lints.clippy]`, give the group `priority = -1` so the
  single-lint entries override it.
- **Never put `#![deny(warnings)]` in source.** A new compiler or Clippy release adds warnings, so the
  crate's own build — contributors, CI, a fresh checkout — breaks on a toolchain upgrade with no code
  change. Deny warnings in CI with the flags above instead.
- Never weaken lint configuration, delete a test, or add `#[ignore]` to get green. Report the
  failure instead.

## Build scripts

Without `rerun-if-changed`, a build script reruns whenever any file in the package changes. After
the first `rerun-if-changed` it reruns **only** for the files it names, so an input it reads but does
not declare goes stale silently until `cargo clean`. Declare every input file and every environment
variable (`rerun-if-env-changed`), and write only into `OUT_DIR`. A `cargo::warning` line printed on a
later build does not prove the script reran: Cargo prints it again for a cached build too.
