# Ownership, errors and APIs

Read this when a borrow or lifetime error resists a first fix, when choosing an error type, or when
adding or changing anything `pub`.

## Borrow errors are design feedback

**Symptom:** E0499, E0502 or E0505 ("cannot borrow ... because it is also borrowed"), answered with
`.clone()`, `Rc<RefCell<_>>` or `Arc<Mutex<_>>`.
**Cause:** a borrow lives longer than the work needs, or the data has two owners where one would do.
**Replace, in this order:**

1. End the borrow before mutating: compute the value into a local, then mutate.
2. Borrow disjoint fields separately, or split the struct so they can be.
3. Move out of a `&mut` with `std::mem::take` or `mem::replace` instead of cloning.
4. Refer to graph or tree nodes by index or ID into one owning collection, not by reference.
5. Only then share ownership — and only when the data genuinely has several owners.

```rust
// E0502: `self.add` borrows all of `self` mutably while `self.items` is borrowed.
fn recompute(&mut self) {
    for price in &self.items { self.add(*price); }
}

// Bad: copy the whole list so the borrows no longer overlap.
for price in self.items.clone() { self.add(price); }

// Good: borrow only the field the helper touches; the borrows are disjoint.
fn add(total: &mut u32, price: u32) { *total += price; }
for price in &self.items { add(&mut self.total, *price); }
```

**Proof:** it compiles without the clone or the `RefCell`. `RefCell` only moves the borrow check to
runtime, where a violation panics. Clippy will not find these for you: `redundant_clone` sits in the
unfinished `nursery` group and is off by default.

Cloning is right when the copy is cheap and wanted — a small `Copy`-like value, or data handed to a
thread or task that must own it. Clone right before the hand-off, not at the top of the function.

## Lifetimes

- **A struct owns its data.** A lifetime parameter on a struct is for a short-lived view such as a
  parser or iterator, chosen deliberately. Added to fix a borrow error, it spreads `<'a>` through
  every type that holds the struct.
- **Never write `&'a mut self` where `'a` is the struct's own lifetime.** It borrows the value
  mutably for the rest of its life.
- **`T: 'static` means "owns its data", not "lives forever".** A `String` is `'static`. Satisfy
  `thread::spawn` or `tokio::spawn` by moving owned data in, not with `Box::leak` or a global. To
  borrow locals from threads, use `std::thread::scope`.

## Errors

| Code | Error type |
|---|---|
| a library, or a module other code matches on | a crate-owned enum implementing `std::error::Error + Send + Sync + 'static`, often derived with `thiserror`; `#[non_exhaustive]` when variants will grow |
| an application's top level, a CLI, a test helper | `anyhow::Result` (or `Box<dyn Error + Send + Sync>`) with context added at each layer |

- Panic only for a broken invariant — a bug — never for bad input, I/O or a missing file. `expect`
  states the invariant: `.expect("the regex literal is valid")`. Unwrapping a `Mutex::lock` result is
  the std idiom, except in a long-running service (see poisoning in [async and
  concurrency](async-and-concurrency.md)).
- **An error is shown once.** The wrapped error belongs in `source()` *or* in the outer `Display`,
  not both, or a chain reporter prints "failed to load config: no such file: no such file". With
  thiserror, `#[error("failed to load config")] Load(#[source] io::Error)`, not `{0}` in the message.
- Display messages are lowercase with no trailing period, so they compose in a chain.
- Convert a lower error into yours with a `From` impl (`#[from]` in thiserror), so `?` does it;
  repeated `.map_err(...)` at every call site is noise that drifts. Keep `map_err` for adding
  context the source error lacks, such as the path.
- **Overflow panics in debug and wraps in release.** Tests built in debug never see the release
  behavior. Use `checked_*` and turn `None` into an error, `saturating_*` where clamping is right, or
  `wrapping_*` where wrapping is the intent. For arithmetic whose correctness matters in production,
  set `overflow-checks = true` in `[profile.release]`.
- **`as` never fails.** `300u64 as u8` is 44, `-1i32 as u32` is 4294967295, `f64::NAN as i32` is 0.
  Widen with `T::from(x)` and narrow with `T::try_from(x)?`; keep `as` for intentional truncation,
  with a comment. Clippy's `cast_*` lints are in `pedantic`, off by default.

## Public API

Every `pub` item, re-export and dependency is a commitment other code builds on. Treat adding one
as a design decision to state, not a side effect of making something compile.

- **The narrowest visibility that works.** `pub(crate)` for what only this crate uses; `pub` only
  for what callers outside it need. Making an item `pub` to get past a privacy error is an API
  change, not a fix.
- **Private fields, validating constructors.** A public field pins the representation. A private
  field behind a constructor makes an invalid value impossible to build.
- **Types, not flags.** An enum or newtype says what `true` or a bare `u64` cannot: `Visibility::Hidden`,
  `UserId(u64)`. Prefer them over `bool` and `Option` positional parameters.
- **Generics or `impl Trait` arguments by default; `dyn Trait`** for heterogeneous collections and
  plugin boundaries. A `dyn` trait must be dyn-compatible: no generic methods, no `Self` returns, no
  `async fn`, unless the method is bounded `where Self: Sized`.
- **Follow the naming conventions.** Getters are `name()`, not `get_name()`; conversions are
  `as_*` (free, borrowed), `to_*` (costly, or borrowed to owned) and `into_*` (consuming). The
  one obvious, lossless conversion between two types is a `From` impl, which also gives `Into`; a
  named `from_*` constructor is right when the input needs a meaning such as units
  (`Duration::from_secs`). Callers guess names from
  these. Clippy's `wrong_self_convention` checks only private items by default, so a public
  `to_*` that consumes `self` goes unflagged.
- **Comparison traits must agree.** `Ord`, `PartialOrd`, `Eq` and `Hash` describe one order and one
  equality. A hand-written `Ord` beside a derived `PartialOrd` compiles, but `<` and `sort()` use
  `PartialOrd`, so they follow the field order, while `cmp`, `max` and `BTreeSet` follow your rule:
  the same two values came out in opposite orders from `sort()` and from a `BTreeSet`. Derive all of them, or write `Ord` and implement
  `partial_cmp` as `Some(self.cmp(other))`. Clippy denies the mismatch
  (`derive_ord_xor_partial_ord`), which is one reason to run it. Sorting with an inconsistent
  order panics since 1.81.
- **The common traits.** Every public type implements `Debug`. Derive `Clone`, `PartialEq`, `Eq`,
  `Hash`, `Default` and `Copy` where they mean something for the type — a caller cannot add them
  later. Put trait bounds on `impl` blocks and functions, not on the struct definition, where every
  `impl` and every generic user must repeat them and adding one later breaks callers — unless a
  field needs the bound (`T::Item`).
- **`#[must_use]`** on a function whose result is the point, such as one returning a new value
  instead of mutating, so a dropped result warns.
- **Document the contract.** A public function that returns `Result` says when in `# Errors`; one
  that can panic says when in `# Panics`. An example in the doc comment is a doctest that keeps it
  true.
- **A library never prints or exits.** It returns errors, logs through `log` or `tracing` and leaves
  the subscriber, `println!` and `process::exit` to the binary. `process::exit` also skips every
  destructor still on the stack.
- **`#[non_exhaustive]`** on a public enum or struct that will grow, so adding a variant is not a
  breaking change. Not on one whose exhaustiveness callers rely on.
- **`async fn` in a public trait** warns (`async_fn_in_trait`) because callers cannot require the
  returned future to be `Send`. Declare `fn get(&self) -> impl Future<Output = T> + Send;`
  (implementors may still write `async fn`); use the boxing `async-trait` crate only for `dyn` use.
- Run `cargo semver-checks` before releasing a published library. It misses some breakage — changed
  field and parameter types, generics, features — so review those by hand.
