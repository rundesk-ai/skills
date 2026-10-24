+++
skill = "using-rust"
cases_version = 1
kind = "quality"
difficulty = "easy"
fixture = "wordtally"
rubric = """
result.1  Names the cause: Rust ignores SIGPIPE, so once `head` exits the next `println!` gets EPIPE and `println!` panics on a write error.
result.2  Fixes it so `wordtally sample.txt | head` exits quietly with status 0 and no panic message, by writing through a locked, buffered stdout with `writeln!`/`?` and treating `ErrorKind::BrokenPipe` as a normal end (restoring the default SIGPIPE disposition is acceptable if the trade-off is stated).
result.3  Other write errors (not BrokenPipe) are still reported with a non-zero exit, not swallowed.
result.4  Output to a terminal or file is unchanged, and the existing test still passes.
conduct.1 Reproduces the panic with a pipe before the fix and shows the same command clean after it.
conduct.2 Runs `cargo test` and `cargo clippy --all-targets` and reports their result.
"""
+++
Running `wordtally sample.txt | head` prints the top words and then a scary
"failed printing to stdout" panic. Users see it every time they pipe the output. Make it stop.
