---
name: performance-discipline
description: Treat performance as a first-class invariant, measured empirically, not guessed. Use when building or reviewing anything on a hot path, when choosing a synchronization primitive or an allocation strategy, or when a performance claim is being made without a benchmark. Covers micro-benchmarks, flame graphs, and the per-decision cost choices.
---

# Performance Discipline

Performance is a first-class constraint, the same as correctness. It gets measured, not asserted. A performance claim with no benchmark behind it is a guess, and intuition about where time goes is usually wrong.

## Measure, do not reason

- Criterion-style micro-benchmarks for hot paths. A hot-path change ships with the benchmark that shows what it did.
- Profile before optimising. A flame graph (perf, cargo-flamegraph) tells you where time actually goes. Optimise what the profile points at, not what you assume.
- Performance is a sensor in the `adversarial-loop`: ship the change, run the benchmark, read the number back.

## The per-decision cost choices

The defaults are often wrong for a hot path.

- **Mutex or not.** A lock on a hot path serialises it. Reach for it deliberately. On thread-per-core, prefer a structure that does not need the lock at all.
- **Heap or stack.** Heap allocation on a hot path costs. Default to the stack; reach for the heap when the data outlives the frame or is large.
- **Hot path or cold path.** Know which you are on. Push allocation, logging, and formatting onto the cold path.
- **Batch, amortize, coordinate.** Do not pay a network hop, syscall, or lock per item when you can coordinate and pay it once for many. Often the single biggest win.
- **Secret state machine bloat** Compilers build a complex data structure to manage async/await boundary state machines. The hidden cost of async/await. Sometimes moving to the heap is a win here.

## The bar

- No "this should be fast enough" without a number.
- No optimising a path you have not shown is hot. Cold-path simplicity beats cold-path speed.
- A hot-path change with no benchmark is not finished.
