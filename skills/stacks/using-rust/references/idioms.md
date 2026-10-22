# Idioms: do and do not

Read this for the code behind a rule: each pair shows a default from the skill's table, or a rule
from [ownership, errors and APIs](ownership-errors-and-apis.md), next to the version an agent writes
from habit and the failure that habit causes. The rules and their reasons live in those places; this
file only shows them. Every **Good** block compiles on stable Rust.

## Errors

```rust
// Good: callers can match on the kind; the cause is in `source()`, shown once.
#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
    #[error("failed to read config file {path}")]
    Read { path: PathBuf, #[source] source: io::Error },
    #[error("config is not valid TOML")]
    Parse(#[from] toml::de::Error),
}

pub fn load(path: &Path) -> Result<Config, ConfigError> {
    let text = fs::read_to_string(path)
        .map_err(|source| ConfigError::Read { path: path.to_owned(), source })?;
    Ok(toml::from_str(&text)?)
}

// Bad: a string error callers cannot match on, and a panic on a missing file.
pub fn load(path: &str) -> Result<Config, String> {
    let text = fs::read_to_string(path).unwrap();
    toml::from_str(&text).map_err(|e| format!("parse error: {e}"))
}
```

In an application, add context at each layer instead of defining types:

```rust
// Good: the context says what the program was doing; the error already names the file.
// Reported with `{:#}`: "loading settings: failed to read config file /etc/app.toml: No such file ..."
let cfg = load(&path).context("loading settings")?;

// Bad: the error says what failed but not where or why the program was doing it.
let cfg = load(&path)?;
```

## Unwrap, expect and discarded results

```rust
// Good: input failure is an error; only a true invariant panics, and says why.
let port: u16 = args.port.parse().context("port must be a number from 1 to 65535")?;
static VERSION: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"^\d+\.\d+\.\d+$").expect("the version regex literal is valid"));

// Bad: any malformed argument crashes the process with no hint why.
let port: u16 = args.port.parse().unwrap();
```

```rust
// Good: the error propagates, and the one failure that is acceptable says why.
match fs::remove_file(&lock_path) {
    Ok(()) => {}
    // Another process already cleaned the lock up.
    Err(e) if e.kind() == ErrorKind::NotFound => {}
    Err(e) => return Err(e.into()),
}

// Bad: every failure, including permission denied, silently ignored.
let _ = fs::remove_file(&lock_path);
```

## Signatures

```rust
// Good: accepts &String, &str, a literal, a slice of a Vec or an array.
fn total_len(names: &[String], sep: &str) -> usize { /* ... */ }
fn open_all(paths: impl IntoIterator<Item = impl AsRef<Path>>) { /* ... */ }

// Bad: forces callers to own a String and a Vec just to lend them.
fn total_len(names: &Vec<String>, sep: &String) -> usize { /* ... */ }
```

```rust
// Good: the call site says what it does.
pub enum Overwrite { Yes, No }
copy(&src, &dst, Overwrite::No)?;

// Bad: `true` at the call site means nothing to a reader.
copy(&src, &dst, true, false)?;
```

Take ownership (`String`, `Vec<T>`) only when the function stores the value; otherwise borrow.

## Conversions and arithmetic

```rust
// Good: an out-of-range value is an error, not a different number.
let red = u8::try_from(component).map_err(|_| ParseError::OutOfRange(component))?;
let total = price.checked_mul(quantity).ok_or(OrderError::Overflow)?;

// Bad: 300 becomes 44, and the multiplication wraps silently in release.
let red = component as u8;
let total = price * quantity;
```

## Iteration

```rust
// Good: no index arithmetic, no bounds checks, no off-by-one.
// `zip` stops at the shorter side, so state that the lengths match where they must.
assert_eq!(names.len(), scores.len(), "one score per name");
for (name, score) in names.iter().zip(&scores) { /* ... */ }
let pairs: Vec<_> = values.windows(2).map(|w| w[1] - w[0]).collect();
let parsed: Vec<u32> = lines.iter().map(|l| l.parse()).collect::<Result<_, _>>()?;

// Bad: indexing by hand, an underflow on empty input, and every parse error silently dropped.
for i in 0..names.len() { let score = scores[i]; /* ... */ }
for i in 0..values.len() - 1 { /* ... */ }   // underflows and panics on an empty Vec
let parsed: Vec<u32> = lines.iter().filter_map(|l| l.parse().ok()).collect();
```

`filter_map(... .ok())` is right only when skipping bad items is the specified behavior.

## Matching

```rust
// Good: adding a variant fails to compile here until it is handled.
match status {
    Status::Active => activate(),
    Status::Suspended | Status::Closed => deny(),
}

// Bad: a new `Status::Pending` silently takes the deny path.
match status {
    Status::Active => activate(),
    _ => deny(),
}
```

```rust
// Good
let Some(user) = find(id) else { return Err(Error::NotFound(id)) };

// Bad: the check and the unwrap drift apart in the next edit.
if find(id).is_none() { return Err(Error::NotFound(id)); }
let user = find(id).unwrap();
```

## Types and modules

```rust
// Good: plain data with public fields, or private fields behind a constructor that validates.
pub struct Email(String);
impl Email {
    pub fn parse(s: &str) -> Result<Self, InvalidEmail> { /* validate */ }
    pub fn as_str(&self) -> &str { &self.0 }
}

// Bad: Java-style accessors on an unvalidated field anyone can set.
pub struct User { email: String }
impl User {
    pub fn get_email(&self) -> &String { &self.email }
    pub fn set_email(&mut self, email: String) { self.email = email }
}
```

```rust
// Good: composition. The wrapper exposes exactly the API it means to.
pub struct Admin { user: User, permissions: Permissions }
impl Admin { pub fn user(&self) -> &User { &self.user } }

// Bad: fake inheritance. Every `User` method leaks through, and method lookup surprises readers.
impl Deref for Admin { type Target = User; fn deref(&self) -> &User { &self.user } }
```

```rust
// Good: bounds where they are used.
pub struct Cache<K, V> { map: HashMap<K, V> }
impl<K: Hash + Eq, V: Clone> Cache<K, V> { /* ... */ }

// Bad: every impl, function and type that names `Cache` must repeat both bounds.
pub struct Cache<K: Hash + Eq, V: Clone> { map: HashMap<K, V> }
```

## Lints

```rust
// Good: the suppression states why, and warns once it is no longer needed.
#[expect(clippy::too_many_arguments, reason = "mirrors the C API one to one")]
fn ffi_call(/* ... */) {}

// Bad: silences the lint forever, with no record of why.
#[allow(clippy::too_many_arguments)]
fn ffi_call(/* ... */) {}
```

## Binaries and libraries

```rust
// Good: main reports the error chain and sets the exit code; the logic lives in lib.rs.
fn main() -> anyhow::Result<()> {
    tracing_subscriber::fmt::init();
    let args = Args::parse();
    mycrate::run(&args)
}

// Bad: a library that prints, exits and installs the logger takes those choices from every caller.
pub fn run(args: &Args) {
    env_logger::init();
    if let Err(e) = work(args) { eprintln!("error: {e}"); std::process::exit(1); }
}
```
