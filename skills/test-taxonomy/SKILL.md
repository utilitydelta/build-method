---
name: test-taxonomy
description: The four test layers - unit, integration, DST, chaos - what each is for, what each runs against, and when to reach for which. Use when deciding where a test belongs, when a unit test is straining to cover wiring or timing, or when designing a test strategy for a new subsystem.
---

# Test Taxonomy

Four layers, each catching what the one below cannot. Pick the cheapest layer that can actually catch the failure, then stop.

## Unit tests

- Logic in isolation, embedded, microseconds.
- Catches pure logic, branches, boundaries. Misses wiring, real I/O, timing, anything cross-process.
- See `unit-testing-discipline`.

## Integration tests

- Runs out of a real binary, not embedded. One machine - the local box.
- Catches wiring between real components, real I/O, the contract between subsystems, config and startup.
- This is where most "unit tests with five mocks" actually belong. If proving it needs the real collaborators standing up, it is an integration test.
- Document what the suite covers and how to run it. A test runner with a category registry - run one category, list what exists - is the shape that works.
- External dependencies like cloud systems and auth: OSS versions in docker containers on the local box first. When the substitute would lie about the real platform's behaviour, run against a cloud non-prod environment instead.

## DST (deterministic simulation testing)

- The whole system on a simulated clock, disk, and network. A seeded scheduler drives concurrency and failure injection; any failure replays exactly from its seed.
- Catches concurrency and failure-ordering bugs at integration-test cost, with a free rewind chaos can never give.
- The price is architectural: the system must be built on the simulation substrate from day one (FoundationDB, TigerBeetle). Retrofitting is a rebuild. That founding decision is the only either/or here.
- DST and chaos are complements, not rivals - do both where the substrate allows. DST is artificial by construction: a fault model only surfaces the failures someone thought to model. Jepsen-style chaos on real hardware rolls the dice against real kernels and surfaces the stalls no model contains, at the cost of flaky repro and no rewind. A system built on the sim substrate still gets hammered on real machines.

## Chaos tests

- Runs on a real network: multiple nodes, real latency, multi-hop, real concurrency, failure injection.
- Different in kind, not degree: integration proves it works, chaos proves it survives.
- Catches the time-dimensioned and linux kernel bugs: sys calls, real networking, cluster co-ordination, split-brain, high load (cpu/memory/disk/network), network partitions, kernel stalls, SIGKILLs.
- Environments: RaspberryPis on the LAN, or cloud non-prod environments (e.g. EC2). Different network and hardware topologies; both useful.
- Method: hammer the system with extreme scenarios and inject failure, then assert correctness held.

## How to choose

- Pure function proves it? Unit. (1-10ms)
- Needs real components wired on one box? Integration. (1-100s)
- Concurrency or failure ordering, on a system built for simulation? DST. (integration cost, exact replay)
- Only appears under real latency, concurrency, failure, or scale? Chaos. (1-500s)
