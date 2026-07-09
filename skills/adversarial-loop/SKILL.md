---
name: adversarial-loop
description: The central operating loop for autonomous sandbox build-out - empirical plus adversarial. The implementer takes a goal and builds it phase by phase - holding the pen itself or delegating a phase to a sub-agent when context runs short - proving every change against oracles (unit/integration/DST/chaos tests, underpinned by tracing and metrics); a blind oracle sub-agent black-box tests the contract first; an adversarial review attacks each phase; a triage agent 4Ds the findings into do, session/scraps.md, or dropped. Ends by generating session/replay-guide.md, never by shipping. Use whenever building autonomously in a sandbox. Read before starting any non-trivial build.
---

# The Adversarial Loop

An agent that writes code and reads it back is flying blind: the model wrote the diff to look right, and looking right is not evidence. The same failure repeats one level up - an agent reviewing its own code confirms it, because author and reviewer share a context that already believes the code is correct. The loop fixes both. Correctness is proven empirically against oracles, and the review comes from a fresh context that did not write the code.

## The loop

The input is the goal: authored in the human zone, refined by the `scout`, living at `session/goal.md` in the sandbox. The implementer builds it phase by phase, not all in one go. Each phase:

```
blind oracle writes contract tests (fresh context, surface only) -> run them: red
   -> implement the phase -> prove against the oracles -> adversarial review (fresh context)
   -> triage agent (4Ds) -> fix the do-list -> review again
   -> only nits left? next phase
```

Four agents, four jobs. The implementer writes code and proves it works. The blind oracle tests the contract without ever seeing the code. The adversarial review pokes holes. The triage agent decides which holes are worth filling. Collapse any two of them into one context and that job stops working.

## Topology

The implementer is the root agent. The blind oracle, the adversarial review, and the triage agent are sub-agents, spawned fresh each phase.

Why not a neutral orchestrator over four sub-agents? Context. The implementer is the only role that benefits from history - the goal, the scout's insights, what was tried and rejected. Fresh context is the other roles' feature and would be the implementer's handicap. A stateless orchestrator holds no role of its own and pays handoff cost in both directions for nothing.

The leak to guard is the implementer holding the pen on what the other roles see. Findings travel through files, never through the implementer's paraphrase: the adversarial review writes findings to a file, the triage agent reads the code and that file directly, and the implementer receives only the triaged do-list. An implementer summarising the review for triage is the author filtering its own review.

## Who holds the pen

The root agent implements by default, per the topology above. But it can farm a phase's implementation to a fresh sub-agent and keep only orchestration: plan the phase, write the brief, spawn the implementer, route the triaged do-list back. Decide per phase, not per run.

Delegate when context pressure demands it. Long multi-phase runs die by compaction when the root writes the code itself - the diffs, the test output, the dead ends all accumulate in the one window that also has to survive to generate session/replay-guide.md. A delegated phase costs the root a brief and a result summary instead of the whole trail. If the projection is that the remaining phases plus the replay guide do not fit in the current window, stop holding the pen.

Delegation also buys role hygiene by construction instead of by discipline. With a sub-agent implementer, raw adversarial findings cannot reach the pen even by accident: triage filters first, gold-plating dies in `session/scraps.md` or in the Delete bin, and the implementation context only ever contains the goal, the phase brief, and the do-list.

The cost is real: a sub-agent implementer reads the goal fresh and explores the code fresh, every phase. For work that fits comfortably in the root's window, that re-onboarding is pure overhead and the root should keep the pen. This is the same trade the Stopping section makes for the replay guide - hot context is an asset, spend it while it holds.

## Prove, don't trust

The implementer does not get believed, it gets asked for evidence. A code path is not finished when it compiles. It is finished when it emits evidence: the test that proves it, the span that shows it ran, the metric that moves when it fires.

- Every behaviour ships with the oracle that would catch its absence.
- Trust the run, not the diff. No green test, no log line, no moved metric - nothing was verified.
- "The code looks correct" is the implementer grading its own work. Reject it as evidence.

## The oracles

Pick the cheapest oracle that can falsify the claim being made:

- **Unit tests** - logic in isolation, microseconds. See `unit-testing-discipline`.
- **Integration tests** - a real binary on one machine. Catches wiring units miss.
- **DST** - deterministic simulation testing: seeded concurrency and failure schedules with exact replay, if the system is built for it.
- **Chaos tests** - real network, real latency, failure injection. Catches time-dimensioned bugs.

See `test-taxonomy` for the layers and when to reach for which. Mocking is an anti-pattern, used sparingly - the ladder is in `unit-testing-discipline`.

Underpinning all of them: tracing and metrics, the always-on sensor that definitively proves the internal behaviour of the system. Assertions cover what you predicted; observability covers what you did not.

- A meaningful path emits a span: it ran, with what inputs, how long.
- A metric is an oracle only if you can state, before the run, which way it moves and by how much. Otherwise it is decoration.
- Logging is structured and on the cold path. Default INFO; no INFO on the hot path, it drowns the signal and fills the context window.
- If you cannot observe the path, that is the first bug. Fix the observability, then trust the result.

Keep emission off the hot path; sample where volume is high. See `performance-discipline`.

## The environment

Oracles rely on a realistic test environment. Run each in the cheapest environment that keeps it honest:

- **Local box** - unit and integration tests, OSS substitutes for external dependencies in docker where they behave like the real thing.
- **RaspberryPis on the LAN** - real machines, real network topology. Where chaos tests live.
- **Cloud non-prod environments** - actual platform services, when a local substitute would lie about the real thing's behaviour.

## Falsification depth

The quality of the code the implementer can write is directly proportional to the falsification depth of the oracles. The oracles must be able to prove what the implementer wrote is wrong - that is the only feedback that corrects code mistakes. Unit tests falsify logic. Integration falsifies wiring. Only DST or chaos falsifies a fencing race. Ask an agent to build past the depth of its oracles and it will: the code will look right, pass everything available, and carry the bugs nothing could catch.

So before implementing, ask: can the current oracles falsify the failure modes of this phase? If they can and do not exist yet, the oracle is the first deliverable, not the feature. If the behaviour is unfalsifiable by any oracle - UX, the feel of a screen - that is not a missing sensor to build, it is UX testing: queue it for the human.

## The blind oracle

The implementer's tests inherit the implementer's assumptions. The context that wrote the bug writes the tests that check for it, and both share the same blind spot: the tests verify the code as built, not the contract as promised.

The blind oracle is a fresh sub-agent handed only the external surface - the public API, the goal's contract, whatever a consumer of the system would get - and told to write tests against it. Unit, integration, DST, or chaos, whichever layers the contract demands. It never reads the implementation. Black box, fresh context.

It writes the first tests, before the implementation exists. As soon as a phase's surface settles - the API shape, not the code behind it - the blind oracle writes the contract tests and they run red. The implementer builds to green; the phase is not proven until the blind set passes. The implementer still writes its own tests on top - seeing the internals is a privilege the oracle deliberately lacks, and it reaches edge cases, error paths, and invariants invisible from outside. Two complementary test sets: the blind oracle proves the promise, the implementer proves the mechanism.

The leak to guard: an oracle that peeks at the implementation is the author's test suite with extra steps. Give it the interface and the test scaffolding, not the implementation source.

The reverse leak matters as much: the implementer does not edit blind-authored assertions. A blind test that looks wrong is a finding - route it through triage. A wrong contract test is possible; a quietly rewritten one is the author grading its own work again, with extra steps.

## Red before green

A test is evidence only after it has been seen to fail. Born green, it either cannot fail or tests what already worked - it proves nothing.

Changed behaviour: predict the breakage. Before implementing, record in session/progress.md which existing tests will break and how. Failing as predicted is the change landing. Failing off-list, or surviving when it should have broken, is a finding - not churn. Append-only keeps the prediction honest; it cannot be rewritten to match the outcome.

## The adversarial review

A fresh sub-agent with no memory of writing the code, told to break it. It can run the oracles, or read the code directly and judge it against the goal. The separation is most of the value: the author context defends its decisions, the fresh context attacks them. Often this pairing alone is enough to produce good code.

- Prefer a non-agent oracle where one exists - a conformance suite, reference tests, an invariant checker. It cannot be flattered.
- Do not tell the review the code is fine. Tell it to find what is wrong.
- Attack the layer below the safety claim. When the code justifies itself by citing an invariant or an existing mechanism ("rides the existing X", "reuses Y"), that citation is where the author stopped thinking. Price the resource underneath: how often does the new work fire under load, how long does it hold the resource, and who queues behind it.

## The triage agent: 4Ds

Adversarial review output never goes straight back to the implementer. An adversarial agent finds something wrong with everything, because there always is. Loop that raw and every finding becomes a fix-order; find and fix both add, nothing subtracts, and complexity ratchets into a gold-plated monster.

The triage agent sits between them, reads the goal, the code, and the findings file, and disposes each finding:

- **Do** - breaks correctness or the goal. Fix in this phase.
- **Defer** - real, not this phase. Into `session/scraps.md`.
- **Delegate** - needs a call the loop cannot make: a critical design decision, or UX testing. Into `session/scraps.md`, flagged for the human.
- **Delete** - hardening past the goal. Gold-plating. Dropped, not carried anywhere; its disposition line in session/progress.md is the only trace.

"Correct but not worth it" is a real verdict the adversarial review cannot reach, because it has no cost model. Triage does.

One verdict triage cannot reach on its own: closing a performance finding. A perf finding closes only against a measurement from a healthy instrument. "Noise is large" and "the threshold is miscalibrated" are claims about the instrument, and an oracle that fails on unmodified main indicts the environment or the threshold, not nothing. Until a clean-instrument run decides which, the finding is a Defer with its re-verify condition attached, not a close.

## Scraps

`session/scraps.md` is the backlog of Defer and Delegate leftovers - findings triage judged real but not worth implementing in the current phase. It is mutable and it has readers:

- At the start of each phase, the implementer reads it and picks up anything that now traces to the goal.
- At loop end, whatever is unconsumed surfaces to the human zone with the delegations, then dies with the other md artifacts at fold-back.

## Interrupting the human

Sandbox work is autonomous; the human does not want to hear from the agent. The default route for anything needing a human - including every triage Delegate - is `session/scraps.md`, surfaced at loop end. Interrupt mid-loop only when the loop genuinely cannot proceed:

1. A **nuclear design call** - a genuine fork the goal never anticipated, that cannot be deferred, where building on would commit the work to one arm of the fork.
2. **Blocking UX testing** - a click-through that cannot be deferred, or that the implementer must see to know the path forward.

"Would like the human's opinion" is not an interrupt. If work remains that is unblocked, build that and leave the question in session/scraps.md.

## Resumability

Autonomous runs die: context compaction, a crashed session, a cap resumed tomorrow. The loop survives through its docs, kept current as the work happens, not as end-of-session housekeeping. Every session-generated doc - the goal, the loop docs, the guide - lives in `session/` at the sandbox root, and the whole folder dies at fold-back.

- **session/session-state.md - mutable.** Where the build is right now: current phase, the step in flight, next action, open questions. Overwritten freely. A fresh context reads this to resume.
- **session/progress.md - append-only.** What happened: phases completed, decisions and their why, findings and their 4D dispositions. Never edited, only appended. This is the audit trail - a disposition recorded here cannot be quietly rewritten when the implementer later disagrees with it.
- **session/scraps.md - mutable.** The backlog, above. The one loop doc that is a legitimate input to later phases.

If session/session-state.md does not say what to do next, it is stale, and stale is worse than absent.

session/session-state.md and session/progress.md record the walk, not the destination. The sandbox path is gradient descent - wrong turns, backtracks, dead spikes. Anything derived from the build (session/replay-guide.md, docs, PR text) reads the settled final code, never the trail. The trail exists to resume the loop and audit dispositions, nothing else.

## Stopping

The loop stops when the goal is implemented and a phase's review returns only nits. Then, before completing - while the full build context is still hot - the implementer generates `session/replay-guide.md`: the ordered path the human replays into the shippable code. Do not leave the guide for a later session; a cold context reconstructing the build produces a worse guide than the agent that just walked it.

Read the replay guide generation skill first, then decide: build the guide directly (the default - the hot context is the asset), or sub-agent the generation when the remaining context cannot hold the skill plus the guide. Either way the guide reads the settled final code, not the trail, and sandboxed agent-led code never ships directly.

Cap iterations per phase so a review still finding marginal nits at 10x the cost halts on spend. A phase still holding blockers at its cap means the goal was under-scoped: delegate back to the human, do not grind.

## The periphery

This is the internal loop; the other skills feed it or check it.

- Feed: `persona-driven-design` (why the goals exist, who they are for), `scout` (goal refinement and insights), `hierarchical-context-docs` (how the agent onboards to the architecture).
- Check: `unit-testing-discipline` and `test-taxonomy` (how the oracles are built), `performance-discipline` (the performance oracle).
- Govern the output: `coding-style`, `comment-discipline`, `writing-style`.

The replay of the sandbox build into the shippable code belongs to the human - the loop proves behaviour, it does not replace the human walking the territory. See `method-overview` for how the zones connect.
