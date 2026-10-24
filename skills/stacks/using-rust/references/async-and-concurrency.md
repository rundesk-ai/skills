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
compile, and never `Box::leak` to satisfy `'static`. The compiler's note "has type `...` which is
not `Send`" names the value held across the await; a `Box<dyn Error>` without `+ Send + Sync` is a
common one.

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

**A pinned future that stops being polled while it holds a place in a queue.**
*Symptom:* the task hangs forever, with no error and no CPU, usually under load.
*Cause:* `select!` on `&mut fut` where another arm wins and then awaits something. `fut` has already
queued for a Tokio `Mutex` (or semaphore, or bounded-channel slot). The fair lock is handed to `fut`,
which nothing polls again, so the other arm waits behind it forever. The same happens to the
futures left in a `FuturesUnordered` while the loop body awaits.
*Replace:* spawn the operation, so it is polled by the runtime whatever the select does, and select
on its `JoinHandle`. Use a `JoinSet` instead of `FuturesUnordered` when the body awaits. A larger
channel only moves the hang.

```rust
// Good: op1 runs in its own task; awaiting op2 here cannot starve it.
let mut first = tokio::spawn(op("op1", lock.clone()));
tokio::select! {
    _ = &mut first => {}
    _ = sleep(Duration::from_millis(100)) => op("op2", lock.clone()).await,
}

// Bad: op1 queued for the lock, then is never polled while this arm awaits op2. Hangs.
let first = op("op1", lock.clone());
tokio::pin!(first);
tokio::select! {
    _ = &mut first => {}
    _ = sleep(Duration::from_millis(100)) => op("op2", lock.clone()).await,
}
```

*Proof:* the bad shape reproduces as a hang under a timeout; the spawned shape completes.

**Unbounded channels.** A slow consumer turns `unbounded_channel` into memory growth. 200,000
messages of 4 KiB peaked at 744 MB RSS unbounded, and at 15 MB through `channel(1024)` in the same
time. Use a bounded channel so the producer waits, or `try_send` and return an error where it must
not wait.

**`broadcast` lag is an `Err`, not the end.** A receiver that falls more than the capacity behind
gets `RecvError::Lagged(n)` once, then the newer messages. `while let Ok(v) = rx.recv().await`
treats the lag as a closed channel and stops. Match `Lagged` (log the count) and stop only on
`Closed`.

**`interval` bursts after a stall.** The default `MissedTickBehavior::Burst` fires every missed tick
at once: after a 550 ms stall, a 100 ms interval fired five ticks within 20 ms (`Delay`: one). Set
`MissedTickBehavior::Delay` (or `Skip`) for work that must not stampede.

**Large futures.** An `async fn` holding a big local (a 64 KiB buffer, a large array) makes a future
that size. Passed by value to `tokio::spawn` in a debug build, a 3 MiB one overflowed the stack.
`clippy::large_futures` reports the size; `Box::pin` the future, or put the buffer in a `Vec`.

**Tracing across `.await`.** `let _e = span.enter();` held across an await attaches other tasks'
events to this span: an unrelated task logged as `req{id=1}:req{id=2}`. Use `.instrument(span)` or
`#[instrument]` for async code, and `span.in_scope(|| ..)` for sync code. `#[instrument]` records
every argument through `Debug`, passwords and whole buffers included. Write
`#[instrument(skip_all, fields(user = %user))]` and name what you want recorded.

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

**`spawn_blocking` outlives its timeout.** `timeout` stops waiting, not the closure: the timeout
fired at 100 ms, but the process could not exit for another three seconds while the blocking
closure finished. The blocking pool holds up to 512 threads by default, so blocking calls that
queue behind each other wait for each other. Make the blocking work itself bounded (a socket
timeout, a cancellation flag it checks).

**`#[tokio::test]` runs on a single-threaded runtime.** A race that
`flavor = "multi_thread"` exposed (39,800 of 80,000 increments lost) passed under the default, and
`block_in_place` panics there. Test concurrent code with
`#[tokio::test(flavor = "multi_thread", worker_threads = 4)]`.

## Threads and shared state

- `std::thread::scope` borrows locals from threads without `Arc` or `'static`.
- **Accumulate per thread, merge once** (rayon's `fold` and `reduce`, or a local sum per thread). A
  shared `Mutex` or atomic updated per item in a parallel loop is hundreds of times slower; the
  numbers are in [performance](performance.md). An atomic is right for a flag or an occasional
  counter, not for a hot loop.
- **`Ordering::Relaxed` does not publish data.** Writing data, then setting a flag with `Relaxed`, let
  a reader see the flag and stale data in 25–34% of reads on an ARM machine; x86 tests hide it.
  Set the flag with `Release` and read it with `Acquire`, or use a `Mutex` or channel. `Relaxed` is
  only for counters nobody reads data through. Test lock-free code with `loom`.
- **Poisoning.** After one panic while a std `Mutex` is held, every later `lock().unwrap()` panics,
  so in a long-running server one bad request disables the lock for good. Where the protected data
  stays valid after a panic, recover with `lock().unwrap_or_else(PoisonError::into_inner)`, or use
  `parking_lot`, which does not poison. Elsewhere, unwrapping is the std idiom.
- Locking a std `Mutex` twice on one thread may deadlock or panic. A `RefCell` borrowed while a
  callback runs panics with "already borrowed" when the callback re-enters the same object (an
  observer that subscribes while being notified). Collect the work, release the borrow, then call
  out.
- **A sharded map (`dashmap`) deadlocks when you hold a reference and write.**
  `if let Some(n) = map.get(k) { map.insert(k, *n + 1) }` hangs. Use `entry`, or end the read
  (`map.get(k).map(|r| *r)`) before writing.
- **Channel loops end only when every sender is gone.** `for msg in rx` hangs while `main` still holds
  the original `tx`; `drop(tx)` after spawning the producers. In a `Drop` that joins a worker
  thread, drop or `take()` the `Sender` first: fields drop only after the body returns, so the
  worker never sees the channel close and the join waits forever.

