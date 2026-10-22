+++
skill = "using-rust"
kind = "quality"
difficulty = "complex"
fixture = "userd"
rubric = """
result.1  The build passes because no lock guard is alive across an `.await`: the cache lookup and the insert each take the lock in their own scope, and the upstream call runs unlocked.
result.2  Does not "fix" it by switching to `tokio::sync::Mutex` while still holding the lock across the upstream call and the retries; that compiles but serialises every fetch.
result.3  Does not use `drop(guard)` alone as the fix, `unsafe impl Send`, or `spawn_local` to dodge the bound.
result.4  Replaces `std::thread::sleep` in the retry with `tokio::time::sleep`, and connects it to the sluggishness: blocking sleep stalls the runtime worker.
result.5  The misses counter becomes an atomic or stays a short std-Mutex section; no lock is held across await anywhere.
result.6  Mentions or handles the duplicate-fetch race that appears once the lock is released during the upstream call, or states that it is acceptable.
conduct.1 Runs `cargo build` (offline is fine) and `cargo clippy --all-targets` and reports their result.
conduct.2 Adds no new dependency.
"""
+++
I added a retry to fetch_user in src/main.rs and now cargo build fails with some Send error at
tokio::spawn. Get it building again. Also, the service has felt really sluggish under load ever since
the retry went in — no idea if that's related.
