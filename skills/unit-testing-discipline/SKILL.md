---
name: unit-testing-discipline
description: How to write unit tests - parameterized over many cases instead of many near-duplicate tests, decoupled from internals via shared helpers, each naming the invariant it proves with explicit pass and fail. Use whenever writing or reviewing unit tests. Encodes the mocking ladder and when to push a test up to integration.
---

# Unit Testing Discipline

The default agent behaviour is a pile of verbose, near-identical tests, each hardwired to internal implementation. Better tests are fewer, parameterized, and decoupled.

## One parameterized test, not twenty copies

- Cases that differ only in data are one test with a table or an internal loop, not twenty functions. The human reads the table and sees the whole behaviour; related cases change in one place.
- When a case fails, the message must name which row. A table that fails with "assertion failed" and no case identity is worse than twenty named tests.
- Reach for separate tests only when cases differ in structure, not just values.

## Decouple from internals with helpers

Tests hardwired to internals break every time the implementation moves, even when the contract held.

- Extract a helper that exercises the contract; every test calls it. When the contract changes, there is one place to update.
- A test reaching into private state to assert is a smell. The contract is what you test.

## Every test names its invariant

- Name the property the test holds, not the method it calls. Not "test login works" - "rejects an expired token".
- Assert the failure too, not just the happy path: what input must make it fail, and with which error.
- A test whose invariant you cannot name proves nothing.

## The mocking ladder

Mocking is usually a smell: the code is wired too tightly to its dependencies. Work down, top first:

1. **Redesign the code** so the dependency is not in the way. A seam, an injected service, a pure function. The right answer most of the time.
2. **If unavoidable, hand-build an intentional fake.** A small purpose-built stub you control and can read.
3. **Mocking frameworks come dead last.** They hide the seam and couple the test to call sequences.

Before any of that, ask whether it should be a unit test at all. If proving it needs the real collaborators wired together, push it to integration. See `test-taxonomy`.

Unit tests are the cheapest sensor in the `adversarial-loop`. They catch logic in isolation, not wiring, timing, or distributed failure. Do not stretch them to cover what integration and chaos exist to catch.
