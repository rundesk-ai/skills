# Unsafe

Read this before writing or reviewing any `unsafe` block or `unsafe fn`, FFI, raw-pointer code, or a
hand-written `Send` or `Sync` impl.

## When unsafe is justified

For FFI, and for a measured hot path with no safe equivalent. Never to satisfy the borrow checker,
and never to make a type `Send`. Undefined behavior does not reliably crash: a read through a
dangling pointer can print a plausible stale value, and `transmute::<u8, bool>(2)` can print `false`.
Tests pass straight through it, which is why the checks below exist.

## Rules

1. **The smallest block, inside a module whose privacy protects the invariant.** Soundness depends on
   the safe code around the block as well: changing `<` to `<=` in a safe bounds check can make the
   unsafe code beside it unsound. Keep the fields that carry the invariant private, so only that
   module can break it.
2. **Every `unsafe` block has a `// SAFETY:` comment** stating why each precondition holds here. In a
   safe function, the reason may depend only on correctly constructed values, not on what the caller
   promised. If it depends on the caller, the function must be `unsafe fn`.
3. **Every `unsafe fn` has a `# Safety` doc section** listing the caller's obligations, and in
   edition 2024 each unsafe operation inside it still needs its own `unsafe {}` block.
4. **A public function that dereferences a raw-pointer argument is `unsafe fn`.** Clippy denies the
   safe version (`not_unsafe_ptr_arg_deref`).
5. **Mirror std's bounds on a hand-written `Send` or `Sync`:** `unsafe impl<T: Send> Send for Wrapper<T>`.
   A blanket impl over a raw pointer is how a data race ships.

## Replacements

| Instead of | Use |
|---|---|
| `mem::transmute` between integers, floats and bytes | `from_le_bytes` / `to_le_bytes` (and `_be`, `_ne`), `f32::from_bits` / `to_bits` |
| `transmute` between pointer types | `ptr.cast::<U>()`; `&*ptr` to reborrow |
| `transmute` of a `Vec` or a struct | an explicit conversion — their layout is unspecified unless `#[repr(C)]` |
| `static mut` | an atomic, a `Mutex` in a `static`, `LazyLock` or `OnceLock`; `&raw mut X` at an FFI boundary |
| `unsafe impl Send` to fix a spawn | restructure so the non-`Send` value is not held across an await |
| a raw pointer into a `Vec` kept across a push | an index; a push may reallocate and leave the pointer dangling |

## Prove it

```sh
cargo clippy --all-targets -- -W clippy::undocumented_unsafe_blocks -W clippy::multiple_unsafe_ops_per_block
rustup +nightly component add miri
cargo +nightly miri test
```

Miri interprets the tests and reports undefined behavior that native runs miss: out-of-bounds and
use-after-free access, invalid values, aliasing violations and data races. It checks only the paths
the tests execute, cannot call foreign functions, and is slow, so run it on the tests that exercise
the unsafe code. If the installed nightly has a dated name, use that name instead of `nightly`. A
Miri report is a defect, never noise to silence.

FFI: declare foreign items in `unsafe extern "C" { ... }`, mark items that are genuinely safe to call
as `safe fn`, give every type that crosses the boundary `#[repr(C)]`, and never let a panic unwind
across it.
