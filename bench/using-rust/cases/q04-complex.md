+++
skill = "using-rust"
cases_version = 1
kind = "quality"
difficulty = "complex"
fixture = "logstat"
rubric = """
result.1  The output is byte-identical to the original's on a generated log (compared, not assumed), and the existing test still passes.
result.2  Times in a release build, before and after, on the same input, and reports both numbers; says that `bench.sh` times a debug build (`cargo run` without `--release`, about 9x slower here) and fixes or flags it.
result.3  Removes the per-line allocation and double hashing: the `lines()` String per line, the `format!` key and its two clones, the owned `Record` strings, and the two maps keyed by the same string (one map of a struct, a reused line buffer, and a lookup that allocates the key only on first sight, or equivalent).
result.4  Replaces or cheapens the regex parse (field splitting is the reference) and buffers stdout for the 80,000 output rows.
result.5  Avoids cloning `totals` and every latency vector to compute p95 (`select_nth_unstable`, or sorting in place once), keeping the same p95 definition.
result.6  Reaches at least a 3x speedup on the 2-million-line log in release (the std-only reference reached 4.3x: 1.24 s to 0.29 s), or explains with measurements why not.
conduct.1 Measures where the time goes (a profiler, or timing phases separately) before changing code, rather than guessing.
conduct.2 Adds no dependency without stating what it buys in measured time.
conduct.3 Runs `cargo test` and `cargo clippy --all-targets` and reports the result.
"""
+++
logstat has turned into the slowest step of our nightly job — it chews through about 40 million
log lines a night. Make it as fast as you reasonably can. The report it prints must not change.
