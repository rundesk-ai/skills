# std edge cases

Read this when code handles text, paths, files, floats, collections, child processes, stdout or
time. Each item below compiles, passes a happy-path test and then fails on input the community has
learned to expect.

## Text

- **`str` is UTF-8 bytes.** `"é".len()` is 2, and `&s[0..1]` panics: "byte index 1 is not a char
  boundary". Slice at indices that came from `find`, `char_indices` or `split_at` on a boundary, or
  use `s.get(a..b)`, which returns `None`. Truncating to "n characters" with byte slicing is a panic
  waiting for the first non-ASCII input.

  ```rust
  // Good: cuts on a char boundary.
  fn truncate(s: &str, max_chars: usize) -> &str {
      match s.char_indices().nth(max_chars) {
          Some((i, _)) => &s[..i],
          None => s,
      }
  }

  // Bad: panics on "héllo" with max 2, because byte 2 is inside 'é'.
  fn truncate(s: &str, max: usize) -> &str { &s[..max.min(s.len())] }
  ```
- **A `char` is not a visible character.** `chars().rev()` breaks combining marks and emoji. Use
  `unicode-segmentation` for graphemes and `unicode-width` for terminal columns.
- **Lines keep their terminator.** `BufRead::read_line` leaves `\n` (or `\r\n`) on the string. Use
  `lines()`, which strips both, or `trim_end_matches(['\r', '\n'])`. Do not use `trim()`, which also
  removes meaningful whitespace.
- **`split(' ')` yields empty strings** between repeated spaces. Use `split_whitespace` for words.
- **Case-insensitive comparison:** `eq_ignore_ascii_case` for protocols and identifiers;
  `to_lowercase` for human text. Neither is full Unicode case folding.

## Paths and the environment

- **`Path::join` with an absolute path replaces the base.** `Path::new("/data").join("/etc/passwd")`
  is `/etc/passwd`. A user-supplied component can therefore escape the base directory, and so can
  `..`. Reject absolute paths and any `Component::ParentDir`, or canonicalize and check
  `starts_with(base)`. Clippy warns on a literal (`join_absolute_paths`), never on runtime input.

  ```rust
  // Good: only plain names; `/`, `..`, `.` and drive prefixes are refused.
  fn safe_join(base: &Path, user: &Path) -> Option<PathBuf> {
      if user.components().any(|c| !matches!(c, Component::Normal(_))) {
          return None;
      }
      Some(base.join(user))
  }

  // Bad: "/etc/passwd" or "../../etc/passwd" reads outside the upload directory.
  let file = uploads_dir.join(&request.filename);
  ```
- **Paths are not strings.** A file name can be non-UTF-8. Keep `Path` and `OsStr` until display,
  then use `path.display()`. `to_str().unwrap()` panics on a valid file. `camino` gives UTF-8 paths
  where the project can require them.
- **`extension()` is only the last part:** `archive.tar.gz` gives `gz`.
- **`fs::canonicalize` on Windows** returns a `\\?\` path that many tools reject. `dunce` returns the
  normal form.
- **`env::args()` panics on a non-UTF-8 argument**, such as a file name from an old archive. Use
  `args_os()`, or let `clap` take `PathBuf` arguments.
- **`read_dir` order is whatever the file system returns** — not sorted, and different between
  machines. Sort the entries before output, hashing or numbering anything from them.
- **`env::var` fails on unset and on non-UTF-8 values.** Match on `VarError::NotPresent` to apply a
  default, and use `var_os` for paths.

## Files and output

- **`BufWriter` swallows the last error on drop.** Call `flush()?` (or `into_inner()?`) before it
  goes out of scope, or the final write's failure is lost.
- **Successful writes are not durable writes.** A crash after `write` can leave a truncated file.
  Write to a temporary file in the same directory, `sync_all`, then rename it over the target.
  `tempfile::NamedTempFile::persist` does the atomic rename but **not** the sync: call
  `tmp.as_file().sync_all()?` before `persist`, and on Unix also sync the parent directory when the
  file must survive a power loss.
- **`println!` panics on a closed pipe, and is slow in a loop.** Rust ignores `SIGPIPE`, so
  `mycli | head -1` ends with "failed printing to stdout: Broken pipe". And stdout flushes at every
  newline whether or not it is locked: one million `println!` lines took 0.4–1.5 s, locking alone
  saved under 5%, and a `BufWriter` over the lock took 16–19 ms. A CLI writes through a
  `BufWriter` with `writeln!(..)?`, flushes at the end (where a broken pipe also surfaces), and
  treats `ErrorKind::BrokenPipe` as a normal exit. Output a person watches live, such as progress,
  needs an explicit `flush()`.

  ```rust
  // Good
  fn write_lines(items: &[String]) -> io::Result<()> {
      let mut out = BufWriter::new(io::stdout().lock());
      for item in items {
          writeln!(out, "{item}")?;
      }
      out.flush()
  }
  fn main() -> ExitCode {
      match write_lines(&items()) {
          Ok(()) => ExitCode::SUCCESS,
          Err(e) if e.kind() == ErrorKind::BrokenPipe => ExitCode::SUCCESS,
          Err(e) => { eprintln!("error: {e}"); ExitCode::FAILURE }
      }
  }

  // Bad: panics with "failed printing to stdout: Broken pipe" under `| head`, and flushes per line.
  for item in items() { println!("{item}"); }
  ```
- **`print!` does not flush.** A prompt without a newline needs `io::stdout().flush()?` before
  reading input.

## Child processes

- **No shell.** `Command::new(prog).arg(x)` passes `x` as a single argument. Building `sh -c` with
  `format!` from input is command injection.
- **A dropped `Child` is neither killed nor reaped.** It keeps running, and once it exits it stays a
  zombie until someone calls `wait`. Clippy warns (`zombie_processes`). Call `wait`, `output` or
  `status`, and after `kill()` still `wait()`.
- **Piped stdout and stderr can deadlock.** Reading one to the end while the child blocks writing
  the other, with its pipe buffer full, hangs both processes. Use `output()`, or read the pipes on
  separate threads.
- **A non-zero exit is not an `Err`.** `output()?` succeeds when the program fails. Check
  `status.success()` and report the exit code and stderr.

```rust
// Good: separate arguments, the child is waited on, and failure is checked.
// `--end-of-options` stops a branch named "--output=x" from being read as a flag.
let out = Command::new("git").args(["log", "--oneline", "--end-of-options", branch]).output()?;
if !out.status.success() {
    bail!("git log failed ({}): {}", out.status, String::from_utf8_lossy(&out.stderr).trim());
}

// Bad: shell injection through `branch`, and a failing git returns empty output as success.
let out = Command::new("sh").arg("-c").arg(format!("git log --oneline {branch}")).output()?;
let log = String::from_utf8_lossy(&out.stdout);
```

## Numbers

- **Floats have no total order.** `sort_by(|a, b| a.partial_cmp(b).unwrap())` panics on `NaN`, and
  the usual "fix", `.unwrap_or(Ordering::Equal)`, is worse: over 1,000 inputs containing `NaN`,
  Rust 1.91 panicked on 518 ("the comparison function does not correctly implement a total
  order", checked since 1.81) and left 361 more out of order; 1.80 left all of them misordered,
  silently. Use `v.sort_by(f64::total_cmp)`, which orders every value, `NaN` included. A float
  cannot be a `HashMap` key or derive `Eq`; `ordered-float` wraps it when one must be. The same
  panic comes from any comparator that is not a total order, so `Ord` must agree with `PartialOrd`,
  `Eq` and `Hash` (see [ownership, errors and APIs](ownership-errors-and-apis.md)).
- **`f32` accumulates error fast.** Adding `0.1f32` ten million times gave 1,087,937, not 1,000,000.
  Accumulate in `f64`, or use compensated (Kahan) summation where the total matters.
- **`%` keeps the sign of the dividend:** `-7 % 3` is `-1`. Use `rem_euclid` for indices and
  wrap-around. Integer division by zero panics; `checked_div` returns `None`.

## Collections

- **`HashMap` iteration order is random, seeded per map.** Output, snapshots, hashes or signatures built
  by iterating one change from run to run. Use `BTreeMap`, `indexmap`, or sort before emitting.

## Data from outside

- **A length read from input decides an allocation.** Beyond the abort and the "capacity overflow"
  panic, an overcommitting OS may let a huge `with_capacity` succeed and fail later, far from the
  cause. Check `n` against the bytes actually present, and cap it, before allocating.
- **JSON numbers:** `serde_json::Value` silently turns integers above `u64::MAX` into floats, and
  JavaScript readers lose precision above 2^53, so IDs travel as strings.
- **`#[serde(untagged)]` takes the first variant that fits** and drops the fields that variant does
  not have, with no error, and its error message names no variant when nothing fits. Prefer
  `#[serde(tag = "type")]`.

## Ownership at runtime

- **Reference cycles leak.** Two `Rc` or `Arc` values pointing at each other are never freed. The
  back-pointer, such as a parent link or an observer, is a `Weak`.
- **Recursion and deep `Drop` overflow the stack.** A long `Box` linked list, or a deeply nested
  tree, overflows when it drops. A recursive parser does the same on adversarial nesting. Iterate
  with an explicit stack, write an iterative `Drop`, and cap the nesting depth on untrusted input.
- **`#[derive(Debug)]` prints secrets.** A token or password field ends up in logs through `{:?}`.
  Wrap it in `secrecy::SecretString`, or write a `Debug` impl that redacts it.

## Time

- **`Instant` for elapsed time, `SystemTime` for wall-clock time.** `SystemTime` can jump backwards,
  so `duration_since` returns `Err` and must not be unwrapped in a timeout or rate limiter.
