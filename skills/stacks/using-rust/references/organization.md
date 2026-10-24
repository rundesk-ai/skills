# Organization

Read this when adding a module, crate, binary, feature or workspace member, when moving code
between them, or when a build is slow because of how the crates are arranged. Each rule here has a
consequence beyond style: a compile error, a broken release, or a slower build.

## Modules

- **Follow the file layout the crate already uses.** For a new crate, use `src/net.rs` beside a
  `src/net/` directory rather than `src/net/mod.rs`, so the editor does not fill with tabs named
  `mod.rs`. Never create both: `E0761 file for module 'net' found at both "src/net.rs" and
  "src/net/mod.rs"`. Agents hit this when they add a submodule next to an existing file.
  `clippy::mod_module_files` enforces the choice.
- **Name imports; do not glob them.** `use crate::a::*; use crate::b::*;` compiles until `b` gains an
  item with a name `a` already has. Then it fails with `E0659 ... is ambiguous`. Cargo's SemVer rules
  let a dependency add an item in a minor release, so a glob import of another crate breaks on a
  `cargo update` you did not review. `use super::*` inside `mod tests` is the accepted exception.
- **`pub(crate)` for anything outside the public API.** A `pub fn` in a `pub mod` of a library never
  gets a dead-code warning, because the compiler assumes an outside caller exists. The same function
  as `pub(crate)` reports `function 'x' is never used`, so dead code becomes visible again.
- **One path per item.** Re-export deliberately (`pub use`) to build the public facade, and do not
  leave a second path to the same item behind after a move.

## Crates and workspaces

- **A crate is the unit of parallel and incremental compilation.** A chain of crates, each depending
  on the one before, builds one at a time. A wide graph builds in parallel: one small base crate of
  shared types, independent crates on top of it, and one leaf binary that ties them together.
  Confirm the shape with `cargo build --timings` before splitting crates for speed; the costs of
  generics and proc macros across crates are in [performance](performance.md).
- **Large workspaces: a virtual root manifest and a flat `crates/` directory**, each folder named
  exactly like its crate. A nested tree drifts out of shape as the code grows. Put shared metadata
  in `[workspace.package]` and `[workspace.dependencies]`, and have each member inherit it
  (`version.workspace = true`, `dep = { workspace = true }`, `[lints] workspace = true`).
  Internal crates get `publish = false`.
- **New project automation is a Rust crate (`xtask`)** when the repository has none; keep the
  Makefile or scripts a project already uses. An xtask is portable to Windows, needs no extra
  tools, and the compiler checks it. Add
  `[alias] xtask = "run --quiet --package xtask --"` to `.cargo/config.toml`, and from inside it run
  Cargo as `Command::new(env!("CARGO"))`.

## Public dependencies

**A dependency's type in your public API ties every caller to that dependency's major version.**
When `geo` takes `units::Meters` from units 1.x and the application uses units 2.x, the build fails
with `E0308 ... two different versions of crate 'units' are being used`. Wrap the type in a
newtype you own, or re-export the crate (`pub use units;`) so callers name the same version. A
semver-major bump of a public dependency is a semver-major change for you.

## Features

- **An optional dependency creates a public feature with its name.** `serde = { optional = true }`
  makes a feature `serde` that callers can enable. Removing or renaming it later is a breaking
  change. Name the feature yourself and refer to the crate as `dep:serde` inside it.
- **Name features for what they add:** `std`, never `use-std` or `with-std`. Never write a negative
  feature (`no-std`), because unification can only ever turn features on.
- **Test helpers other crates' tests need** are not visible under `#[cfg(test)]`, which applies only
  to this crate's own unit tests. `tests/` fails with `E0425`. Gate the helpers with
  `#[cfg(any(test, feature = "test-util"))]`, and enable that feature from
  `[dev-dependencies]` (`mycrate = { path = ".", features = ["test-util"] }`). The helpers then stay
  out of normal builds.

## Naming that changes behavior

- A `-sys` crate only declares the C items and links the library. Cargo allows one package per
  `links` value in a graph, so two crates linking the same C library conflict. Depend on the
  existing `foo-sys` rather than writing a second one.
- A crate-level `Result` alias keeps the error parameter open: `pub type Result<T, E = Error> =
  std::result::Result<T, E>;`. Without the default, any `Result<(), String>` in a module that
  imports the alias fails with `E0107`.
