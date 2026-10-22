# Ecosystem: solved problems

Read this before writing code for a job the Rust community has already solved: parsing arguments,
config or data formats, dates and time zones, HTTP, databases, logging, retries, shutdown,
cryptography, or test tooling. It names the established default for each job so the work starts from
a proven solution instead of a hand-rolled one.

## Choose in this order

1. **What the project already depends on.** Read `Cargo.toml`; `cargo tree -i <crate>` shows why
   a crate is in the lockfile. A crate present only as another crate's dependency is not a vetted
   choice to build on. A second crate for a
   job one already does doubles the compile time and splits the code's conventions.
2. **std, when it covers the job completely.** `std` now holds `LazyLock`, `OnceLock`,
   `IsTerminal`, `thread::scope`, `available_parallelism` and `io::Error::other`. Each replaces a
   crate that older code still pulls in.
3. **The established crate below.** Hand-rolling a parser, a date calculation, a retry loop with
   jitter, a constant-time compare or a TLS setup re-creates bugs those crates fixed years ago.
4. **Verify before adding** with `cargo info <crate>`: confirm the name, recent releases and that the
   repository is not archived. Then run `cargo deny check advisories` or `cargo audit` if the project
   has them. These defaults are a starting point. They are not proof that a crate is still
   maintained.

Read the locked version's `[features]` before writing a feature list: names change between major
versions (reqwest 0.13 made rustls its default TLS and dropped `rustls-tls`), and
`default-features = false` also removes defaults the code may rely on. Enable only what is used;
`tokio = { features = ["full"] }` in a library forces every feature on every user.

## Defaults by job

| Job | Default | Notes |
|---|---|---|
| Serialization | `serde` with `serde_json`, `toml` | `#[serde(deny_unknown_fields)]` for config, so a typo fails instead of being ignored; `#[serde(default)]` for optional fields |
| CLI arguments | `clap` with `derive` | gives help, `--version`, errors and shell completion; never parse `env::args` by hand |
| Errors | `thiserror` (libraries), `anyhow` (applications) | see [ownership, errors and APIs](ownership-errors-and-apis.md) |
| Logging and tracing | `tracing` with `tracing-subscriber`; `log` in a small library | a library emits events, only the binary installs the subscriber |
| Async runtime | `tokio`; `smol` where the project already uses it | `async-std` is discontinued; migrate rather than extend it |
| Retries with backoff | `backon`; `tower::retry` inside a tower stack | `backoff` is unmaintained |
| Graceful shutdown | `tokio::signal` with `tokio_util::sync::CancellationToken` and `TaskTracker` | `ctrlc` for a synchronous binary |
| HTTP client | `reqwest` | reuse one `Client`: it holds the connection pool |
| HTTP server | `axum` with `tower` and `tower-http` middleware | timeouts, limits, CORS and tracing come from `tower-http`; do not hand-write them |
| Database | `sqlx` (compile-checked queries) or `diesel` | `rusqlite` for embedded SQLite; never build SQL with `format!` |
| Data parallelism | `rayon` | `par_iter()` replaces hand-made thread pools for CPU work |
| Channels beyond std | `crossbeam-channel`, or `tokio::sync` in async | |
| Dates and time zones | `jiff`; `chrono` or `time` where already used | DST-aware arithmetic and the time-zone database are not hand-written |
| Regex | `regex` | linear time, so no catastrophic backtracking; compile once in a `LazyLock` |
| Randomness | `rand`; `getrandom` for raw OS bytes | |
| IDs | `uuid` | |
| Temporary files, atomic writes | `tempfile` | `NamedTempFile::persist` renames atomically; `sync_all` first, since it does not |
| Directory walking | `walkdir`; `ignore` to respect `.gitignore` | |
| User directories | `directories` or `dirs` | never assemble `~/.config` by hand; it differs on every platform |
| Bit flags, enum helpers | `bitflags`, `strum` | |
| Small-vector and arena storage | `smallvec`, `slotmap`, `typed-arena` | `slotmap` gives graph nodes stable, generation-checked keys |
| Bytes for networking | `bytes` | |
| Unicode text | `unicode-segmentation`, `unicode-width` | for user-perceived characters and terminal columns |
| Terminal colour | `anstream` with `anstyle` | `anstream` strips colour when output is not a terminal; `owo-colors` does only through `if_supports_color` |
| TLS | `rustls` | |
| Cryptography | RustCrypto crates (`sha2`, `hmac`, `aes-gcm`), `ring`, `argon2` for passwords | never write a primitive, a password hash or a comparison of secrets yourself |
| Secrets in memory | `secrecy`; `subtle` for constant-time comparison | `==` on a token leaks its length and prefix through timing |
| Property tests | `proptest` | |
| Snapshot tests | `insta` | |
| Testing a CLI | `assert_cmd`, `trycmd` | |
| Mocking HTTP | `wiremock` | |
| Benchmarks | `criterion` or `divan` | |
| Fuzzing | `cargo fuzz` | for parsers and anything taking untrusted bytes |
| Testing lock-free or atomic code | `loom` | it explores thread interleavings; plain tests cannot |

## Replaced crates

An agent recalling older code reaches for these. Each has a successor:

| Instead of | Use |
|---|---|
| `lazy_static`, `once_cell` | `std::sync::LazyLock`, `OnceLock` (see the version table) |
| `atty` | `std::io::IsTerminal` (1.70) |
| `structopt` | `clap` derive |
| `failure`, `error-chain` | `thiserror`, `anyhow` |
| `async-std` | `tokio` or `smol` |
| `tempdir` | `tempfile` |
| `dotenv` | `dotenvy` |
| `backoff` | `backon` |
| `instant` | `web-time` |
| `proc-macro-error` | `proc-macro-error2` |
| `rustls-pemfile` | `rustls-pki-types` (`PemObject`) |
| `serde_yaml`, `serde_yml` | no clear successor: `serde_yml` carries RustSec advisories. Prefer TOML or JSON for new config; for YAML, check RustSec before choosing a fork |
| `ansi_term` | `anstyle`, `owo-colors` |
| `async-trait`, for static dispatch | native `async fn` in traits (1.75) |
