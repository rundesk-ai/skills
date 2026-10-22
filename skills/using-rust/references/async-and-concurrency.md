# Async and concurrency

Read this when code uses `async`, Tokio or another runtime, threads, locks or channels, or when a
spawn fails to compile with a `Send` or `'static` error.

## Defaults

- **`std::sync::Mutex`** (or `parking_lot`) for short critical sections, locked inside a non-async
  method. Tokio's own documentation calls reaching for `tokio::sync::Mutex` unconditionally "a common
  error"; use it only when the guard must be held across an `.await`, and prefer an actor even then.
- **An actor for an I/O resource**: one task owns the connection, others send it messages over a
  bounded `mpsc` channel with a `oneshot` for each reply. Avoid cycles of bounded channels — two
  actors waiting to send to each other deadlock.
- **Blocking work leaves the async worker.** Blocking I/O and short CPU bursts (one password hash)
  go to `spawn_blocking`; sustained CPU-heavy work to a thread pool such as rayon; an endless loop to
  its own thread.
- **Spawned tasks take owned or `Arc` data** through `async move`.

## Traps

**A lock guard across `.await`.**
*Symptom:* `tokio::spawn` fails with "future cannot be sent between threads safely ... `MutexGuard`
is not `Send`". `tokio::spawn` requires `Send` on every runtime flavor; where nothing does
(`spawn_local`, a `LocalSet`, a future passed straight to `block_on`), it compiles and can deadlock
once another task waits on the same lock.
*Cause:* the guard is alive at the suspension point.
*Replace:* end the guard's **scope** before the await. `drop(guard)` does not work: the compiler
decides whether a future is `Send` from scopes, so an explicitly dropped guard still counts as held.

```rust
// Bad: still !Send, even with the drop.
let guard = state.lock().unwrap();
let next = guard.next_id;
drop(guard);
client.send(next).await;

// Good: the temporary guard drops at the end of the statement.
let next = state.lock().unwrap().next_id;
client.send(next).await;

// Good: several reads under one lock; the guard's scope ends at the brace.
let (id, name) = {
    let s = state.lock().unwrap();
    (s.next_id, s.name.clone())
};
```

*Proof:* the spawn compiles and `cargo clippy --all-targets` reports no `await_holding_lock` or
`await_holding_refcell_ref`. The same rule applies to `Rc` and `RefCell` borrows.

**Blocking inside async.**
*Symptom:* latency spikes across unrelated requests; a timer fires late; throughput collapses under
load while CPU is idle.
*Cause:* `std::thread::sleep`, `std::fs`, a synchronous HTTP or database client, or a long loop with
no `.await` holds the worker thread. Aim for no more than 10–100 microseconds between awaits.
*Replace:* `tokio::time::sleep`, `tokio::fs` or `spawn_blocking`, the async client, or move the
computation to a thread pool. No default lint catches this; search async functions for those calls.

```rust
// Good: the hash runs on the blocking pool; the read yields while it waits.
let hash = tokio::task::spawn_blocking(move || argon2_hash(&password)).await??;
let body = tokio::fs::read_to_string(&path).await?;

// Bad: every task on this worker stalls for the whole hash and read.
let hash = argon2_hash(&password)?;
let body = std::fs::read_to_string(&path)?;
```

**`'static` and `Send` bounds on `tokio::spawn`.**
*Symptom:* "borrowed value does not live long enough" or "may outlive the current function".
*Replace:* `async move` with owned data or an `Arc`. Never `unsafe impl Send` to make a spawn
compile, and never `Box::leak` to satisfy `'static`.

**Cancellation in `select!`.**
Every branch that loses is dropped. Dropping `read_exact`, `read_to_end`, `read_to_string` or
`write_all` loses the bytes already moved; dropping `Mutex::lock`, `Semaphore::acquire` or
`Notify::notified` loses the place in the queue. `mpsc::Receiver::recv`, `TcpListener::accept`,
`AsyncReadExt::read` and `StreamExt::next` are safe to drop. Create a long-lived future once, pin it,
and select on `&mut`:

```rust
let deadline = tokio::time::sleep(timeout);
tokio::pin!(deadline);
loop {
    tokio::select! {
        _ = &mut deadline => break,
        Some(msg) = rx.recv() => handle(msg),
    }
}
```

Or move the non-cancel-safe work into its own task fed by a channel.

**Detached tasks.** Dropping a `JoinHandle` detaches the task; it keeps running. Cancel with
`abort()`, own a group with `JoinSet`, or pass a cancellation token. A `spawn_blocking` task cannot be
aborted. Under the default `panic = "unwind"`, a panic inside a spawned task does not crash the
process: it ends that task and comes back as the `JoinError` from awaiting its handle, so a detached
task's panic is only printed to stderr. Await the handles
(or the `JoinSet`) of tasks whose failure matters, and check the result.

```rust
// Good: every task is owned, told to stop on Ctrl-C, and drained so each error or panic is seen.
let token = CancellationToken::new();
let mut tasks = JoinSet::new();
for conn in conns {
    let token = token.clone();
    tasks.spawn(async move { serve(conn, token).await });
}
tokio::signal::ctrl_c().await?;
token.cancel();
let mut first_error = None;
while let Some(res) = tasks.join_next().await {
    // Drain every task: `res??` here would return early, drop the set and abort the rest.
    if let Err(e) = res.map_err(anyhow::Error::from).and_then(|r| r) {
        tracing::error!("task failed: {e:#}");
        first_error.get_or_insert(e);
    }
}
first_error.map_or(Ok(()), Err)

// Bad: detached tasks are cut off mid-write when main returns; errors and panics are lost.
for conn in conns {
    tokio::spawn(serve(conn));
}
tokio::signal::ctrl_c().await?;
```

To react to a task failing before the signal, `select!` on `ctrl_c()` and `tasks.join_next()` in a
loop. Dropping a `JoinSet` aborts every task still in it.

**A library picks no runtime.** `#[tokio::main]`, `Runtime::new` and `block_on` belong in the binary;
a library exposes `async fn` and lets the caller drive it. Calling `block_on` from inside a runtime
panics ("Cannot start a runtime from within a runtime").

**Cleanup.** There is no async `Drop`. Give a resource that needs async cleanup an explicit
`close().await`. Never block on a runtime inside `Drop`, and never rely on `Drop` running for
soundness — `mem::forget` is safe, and reference cycles leak.

## Threads and shared state

- `std::thread::scope` borrows locals from threads without `Arc` or `'static`.
- A shared counter or flag is an atomic, not a `Mutex<u64>`.
- Locking a std `Mutex` twice on one thread may deadlock or panic.
- A test that touches environment variables, the working directory or a fixed port is shared state:
  tests run in parallel threads inside one binary.
