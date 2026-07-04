# Rust

Most of my Rust runs thread-per-core on glommio. The rules assume that. A repo's own glommio skill wins on concrete patterns.

## Thread-per-core

- One executor per core, state owned by the core that uses it. Do not reach for `Arc<Mutex<_>>` as a reflex; on thread-per-core the lock usually means the data is on the wrong core. Message-pass across cores instead.
- The reactor is single-threaded per core. Never call a blocking syscall on the executor. Use glommio's async I/O and Direct I/O.

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
