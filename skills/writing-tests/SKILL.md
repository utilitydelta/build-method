---
name: writing-tests
description: Use when writing tests, changing tests, or implementing code that needs tests. Which test layer to pick (unit, integration, DST, chaos), how to write unit tests, when to mock, and when to use property tests, fuzzing, or mutation testing.
---

# Writing Tests

You already know how to test. This is the order, the defaults, and the bans.

## Pick the cheapest layer that catches the failure

1. **Unit** - pure logic, branches, boundaries. In-process, microseconds.
2. **Integration** - real components wired together on one machine. Real I/O, config, startup. Runs a real binary.
3. **DST** (deterministic simulation testing) - simulated clock, disk, network. Seeded scheduler, exact replay from seed. Catches concurrency and failure-ordering bugs. Only for systems built on a simulation substrate from day one; retrofitting is a rebuild.
4. **Chaos** - real machines, real network, failure injection. Split-brain, partitions, kernel stalls, SIGKILL, high load. DST does not replace chaos: a fault model only finds failures someone thought to model.

Prefer unit while building. Push a test up a layer only when the cheaper layer cannot express the failure.

A unit test needing several mocks is an integration test. Move it.

External dependencies: OSS substitute in docker on the local box. If the substitute lies about the real platform's behaviour, use a cloud non-prod environment.

## Unit test rules

- Cases that differ only in data are one parameterized test with a table, not many near-copies. The failure message must name the row.
- Separate tests only when cases differ in structure, not values.
- Exercise the contract through a shared helper, so a contract change means one place to update. Never assert on private state.
- Name the invariant, not the method. "rejects an expired token", not "test login works".
- Assert the failure path too: which input fails, with which error.

## Mocking

Mocking is a smell: the code is wired too tightly to its dependencies. In order:

1. Redesign so the dependency is out of the way - a seam, an injected service, a pure function. Usually the right answer.
2. Hand-build a small intentional fake.
3. Mocking frameworks last.

If proving it needs the real collaborators, it is an integration test.

## Generated inputs

Not a fifth layer. These run inside the layers above.

- **Property tests** - when the invariant holds over a whole domain, not a list of cases. State the law, let the generator write the rows. Commit the regression files and seeds so found counterexamples become permanent cases.
- **Fuzzing** - every surface that parses untrusted input. Fixed time budget during a build; continuous fuzzing belongs in CI.
- **Mutation testing** - grades the tests, not the code. Scope it to the current diff and the cheap layers, unit and fast integration.

## UI and e2e

- No screenshot-reading LLM as a gate. Every UI check is deterministic or human.
- Assert what the user sees. Dev hooks are for setup and state reads; a `window.__` read inside an assertion is banned.
- End each e2e test by asserting the expected event sequence. The DOM can look right while the wiring is broken.
- One state rendered in two places: assert the id sets match across the views. Unit tests on each side stay green while the views disagree.
- Overlays get geometry checks from `getBoundingClientRect`: width above a floor, inside the viewport, no page overflow.
- Screenshots are byte diffs against a human-approved baseline. Skip them where baseline churn costs more than it catches.
- Quarantine flaky tests and flag them for human triage. Most flakes are test-side timing; the human decides which are product bugs.

## Defect reproduction

A common failure is an agent writing a red unit test and leaving it at that layer.
At times, unit tests can be synthetic.  Too much mocking or exercise a branch of code that never runs in reality.
Different layers provide different benefits, write failing tests at integration and chaos/higher layers.

live running real instances with scraped metrics and traces, showing the reproduction of the incident  beats an artificial reproduction every time.

Defects can be complex and multi-layered. Establish the causal chain before fixing the downstream one.

- Do not assume the test harness is correct.
- Avoid using proxies to measure correctness.
- 

Common failure modes observed in agent led test writing include:
- Bugs in the harness itself. Trust nothing.
- using a proxy measure instead of a more direct measure to assert failure or correctness.
- After the fix, a green test doesn't mean every edge case is covered.  Mutate and check for failure.

## Order

Write the test first and watch it fail. A test that was never red proves nothing.

Document how to run each suite. A test nobody can run does not exist.
