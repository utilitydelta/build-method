# Rust

Most of my Rust runs thread-per-core on glommio. The rules assume that. A repo's own glommio skill wins on concrete patterns.

## Thread-per-core

- One executor per core, state owned by the core that uses it. Do not reach for `Arc<Mutex<_>>` as a reflex; on thread-per-core the lock usually means the data is on the wrong core. Message-pass across cores instead.
- The reactor is single-threaded per core. Never call a blocking syscall on the executor. Use glommio's async I/O and Direct I/O.
- **Every loop needs an await that can actually pend.** A `poll` that never returns freezes the whole core: tasks, timers, even the shutdown handler. In-executor timeout wrappers (`glommio::timer::timeout`) are defenseless against it - the timer is a peer task that never gets polled. Audit any `loop {}` whose exit depends on a parser/state machine making progress: if one arm neither reads more input nor returns, a truncated input spins it forever.
- **Diagnosing a frozen executor** (production playbook, read-only, before restarting anything):
  1. A per-executor heartbeat gauge (unix-ms stamp refreshed by a 1s timer task) is the cheapest tripwire - build it in. Stale stamp = dead executor; every other gauge that executor updates is a fossil the metrics thread keeps serving.
  2. `ps -Lo tid,comm,pcpu,stat,wchan -q <pid>`: R at ~100% with an empty kernel stack = userspace busy-spin; S in `futex_wait` = blocking primitive on a reactor thread. Both are bugs.
  3. `sudo eu-stack -p <pid>` (elfutils) names the spin site: userspace stacks of every thread, one shot, milliseconds of pause, no gdb needed. Rust release builds keep mangled symbols unless stripped - the frames read fine. Capture twice ~10s apart to separate stable frames from transient ones. This is the tool that turns "an executor is spinning" into a file:line. Restarting the process destroys the evidence; capture first.

## The two deadlock traps

- **Never hold an `Rc<RefCell<_>>` borrow across an `.await`.** Take the borrow, read or mutate, drop it, then await. A borrow held across a yield point is a `BorrowMutError` panic or a self-deadlock waiting to happen.
- **Head-of-line blocking.** A single long task starves the executor. Chunk long work and yield between chunks; do not let one slow path hold the core hostage.

## Allocation and the hot path

- No heap allocation on a hot path. Preallocate and reuse buffers. See `performance-discipline`.
- Stack by default. Box only when the data outlives the frame or is large. Keep formatting, logging, and allocation on the cold path.

## Errors

- Typed enum variants on the core data path, with hand-written `From` impls, so structured data survives to the client boundary. `#[error("...")]` string-formatting at creation loses it.
- Strings are fine for what you cannot type cleanly: I/O errors, glommio/io_uring errors that do not impl Clone/Send, catch-all infrastructure failures.
- `thiserror` is fine in leaf/library crates (crypto, sidecar). Keep it off the hot data-path crates where you hand-roll variants. `anyhow` only at a binary's top edge where the error is about to be printed.

## General

- Let the borrow checker design for you. A fight with it usually means the ownership is wrong; restructure rather than reach for `Rc`/`RefCell`/`unsafe`.
- `unsafe` needs a written reason and a proof of the invariant it upholds, not a performance hunch.
