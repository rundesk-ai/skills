# Editions and versions

Read this before using a language feature, std API or Cargo option you are not certain the project's
floor allows, and when moving a crate between editions.

## Find the floor

The **edition** (`edition` in each member's `Cargo.toml`) changes what code means. The **toolchain
floor** is `rust-version` when declared, otherwise the toolchain CI pins in `rust-toolchain.toml`.
Code must compile at both. A newer toolchain on your machine hides a violation: Clippy's
`incompatible_msrv` lint catches std APIs newer than `rust-version`, but nothing catches syntax
except building with the floor itself — `cargo +<floor> check`.

## Features gated by version

| Feature | Needs |
|---|---|
| `let ... else` | 1.65 |
| `OnceLock` | 1.70 |
| native `async fn` in traits (static dispatch only) | 1.75 |
| `[lints]` and `[workspace.lints]` in `Cargo.toml` | 1.74 |
| `LazyLock`, `LazyCell` (replace `lazy_static` and `once_cell`) | 1.80 |
| `#[expect(lint, reason = "...")]` | 1.81 |
| `use<..>` precise capturing, `&raw const` / `&raw mut` | 1.82 |
| `cargo info` | 1.82 |
| resolver `"3"`, which prefers dependency versions compatible with `rust-version` | 1.84 |
| edition 2024; async closures (`async \|\| {}`) and the `AsyncFn` traits | 1.85 |
| let chains: `if let Some(x) = a && x > 0` | 1.88 and edition 2024 |
| `build.warnings = "deny"` / `CARGO_BUILD_WARNINGS=deny` | Cargo 1.97 |
| a member's `default-features = false` overriding a workspace dependency | 1.99 and edition 2024 |

The resolver is workspace-wide and ignored in dependencies. A virtual workspace (a root
`[workspace]` with no `[package]`) gets no edition default, so it must set `resolver` itself.

## What edition 2024 changes

Each of these compiles under one edition and fails or behaves differently under the other.

- **Return-position `impl Trait` captures every lifetime in scope.** A function taking `&Vec<u32>` and
  returning an owned `impl Iterator` now keeps the argument borrowed, so a later `v.push` fails with
  E0502. Write `-> impl Iterator<Item = u32> + use<>` to capture nothing. The old `Captures` trick is
  unnecessary.
- **`if let` drops its scrutinee's temporaries before `else`.** A read guard taken in the condition
  no longer blocks a write in the `else` branch. A `match` on the same expression still holds the
  guard across every arm, so the 2021 deadlock survives there. Bind the value first, then branch.
- **Tail-expression temporaries drop before the block's locals.** Some 2021 borrow errors disappear,
  and `{ &String::from("x") }.len()` starts failing; bind the value to a local.
- **`static mut` references are a deny-by-default error** (`static_mut_refs`), including implicit
  ones from `println!` or a method call. `X += 1` inside `unsafe` is not flagged and is still a data
  race. Use an atomic, a `Mutex` in a `static`, `LazyLock`, or `OnceLock`.
- **Unsafe operations inside an `unsafe fn` need their own `unsafe {}` block**
  (`unsafe_op_in_unsafe_fn` warns). `extern` blocks must be `unsafe extern`, and `no_mangle`,
  `export_name` and `link_section` become `#[unsafe(...)]`.
- **`std::env::set_var` and `remove_var` are `unsafe`**, because another thread reading the
  environment is undefined behavior. Call them before spawning threads, or pass configuration
  explicitly.
- **Never-type fallback is `!`, not `()`.** Code like `f()?` whose type was inferred through the
  fallback stops compiling; name the type with `f::<()>()?`.
- **`gen` is a reserved keyword.** Rename the identifier or write `r#gen`.
- Compatible doctests compile together into one binary; mark one `standalone_crate` if it depends on
  being alone.

## Migrate deliberately

`cargo fix --edition` is conservative: it rewrites only what keeps the meaning, and leaves lints for
the rest. Run it on a clean tree, then set the new edition, then run the full verification loop.
Treat a drop-order or capture change as a behavior change to review, not a formatting diff. Change
the edition, the `rust-version` or the resolver only with approval, since every downstream user
inherits the new floor.
