# Using Rust validation

The current record for `using-rust`; the method is `prompts/benchmark-skill.md`, and the latest result
is in `bench/results/using-rust/`.

Each fixture's seeded defects were reproduced before its rubric was written:

- `wordtally` (easy): a CLI printing with `println!`; `wordtally sample.txt | head` panics with "failed
  printing to stdout: Broken pipe".
- `colorparse` (medium): `parse_rgb("300,0,0")` returns `Rgb(44, 0, 0)` through `as u8`; a garbage feed
  line and a too-short split panic; the public error is `Box<dyn Error>`; a wrong doctest fails only
  under plain `cargo test`, while `ci.sh` runs `cargo test --all-targets`, and a `#[should_panic]` test
  without `expected` passes on its own index panic; parameters are `&String`.
- `userd` (complex): a std `MutexGuard` held across `.await` fails `tokio::spawn` with the `Send` error;
  the retry sleeps with `std::thread::sleep`. Measured on 200 requests: switching to
  `tokio::sync::Mutex` while still holding it compiles and takes 2.7 s; scoping the lock takes 0.58 s,
  and 0.38 s with `tokio::time::sleep`; releasing the lock raises cache misses from 50 to up to 200.
- `logstat` (complex, performance): per-endpoint statistics over a generated 2-million-line log
  (`examples/gen.rs`). Seeded costs: a `String` per line from `lines()`, a regex parse, a `format!` key
  cloned twice into two maps, owned `Record` strings, cloning every map and latency vector for p95,
  unbuffered `println!` for 80,000 rows, and a `bench.sh` that times a debug build (11.7 s against
  1.24 s in release). A std-only rewrite produced byte-identical output in 0.29 s (4.3x).
- `pystats` (routing near miss): a Python division by zero beside an untouched Rust crate.
