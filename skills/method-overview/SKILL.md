---
name: method-overview
description: The L0 map of the whole build method - how a goal travels from the human zone through the scout, into the adversarial loop (sandboxed by default), and back via human replay into shippable code. Load at session start, or whenever unsure which zone the current work is in and which skill governs it. Every other skill is one level down from this one.
---

# Method Overview

Three zones. The human zone owns intent and the shippable code. The scout validates goals before they cost anything. The adversarial loop builds them autonomously, in a sandbox by default. Sandboxed code re-enters the human zone only through human replay. This file is the map; every stage links down to the skill that owns its detail.

## The human zone

Where the human works and the shippable code lives. Four activities:

- **Goal authoring.** Goals are the artifact handed to agents. They exist to serve a persona - `persona-driven-design` is why the goals exist and who they are for.
- **Hierarchical context docs.** How agents onboard to the architecture without swallowing the codebase. See `hierarchical-context-docs`.
- **UX testing.** The gap no oracle can fill: a human clicking buttons and viewing screens. `ux-verification` shrinks that gap - human-dictated journeys bound to oracle-authored tests, and the agent's visual-residual ledger tells the human exactly which screens need eyes at replay.
- **Replay.** Folding sandbox work back into the shippable code, below.

## Scout

Part of goal authoring is checking the goal makes sense and is achievable. Agent-led and throwaway: research prior art, spike the risky paths in real executing code, debate the goal. Output is goal insights and goal refinement, fed back to the human zone. See `scout`.

## The sandbox

The default home for a refined goal is not the shippable code. The prep step copies it to a sandbox, and the implementer builds it there phase by phase under the `adversarial-loop`: a blind oracle sub-agent writes black-box tests against the phase's external surface first, then prove each phase against oracles (unit, integration, DST, chaos - `test-taxonomy`, `unit-testing-discipline` - underpinned by tracing and metrics), adversarial review from a fresh context, 4D triage into a do-list and session/scraps.md. Falsification depth bounds what the agent can build; the oracles must be able to prove the implementation wrong. The implementer holds the pen by default but can delegate a phase's implementation to a sub-agent when the run is long enough that context, not capability, becomes the constraint.

The work is autonomous: anything needing a human queues in scraps.md and surfaces at loop end. The agent interrupts mid-loop only for a nuclear, non-deferrable design fork or blocking UX testing. State lives in session/session-state.md, session/progress.md, and session/scraps.md.

The loop itself is location-agnostic - same phases, same oracles, same triage running directly in the real repo when the human chooses not to sandbox. What the sandbox buys is the replay step below; skip it and there is no replay-guide.md, the human owns the diff directly. Either way session/ never ships.

Code written anywhere is governed by `coding-style`, `comment-discipline`, and `performance-discipline`; prose by `writing-style`.

## Replay

When a sandboxed build's goal is implemented the loop stops and generates session/replay-guide.md. The human replays the sandbox build into the shippable code with that guide, questioning every decision. Divergence is expected: the human edits, or pushes the work back to the sandbox for another iteration. Sandboxed agent-led code never ships directly - a diff review of a finished build is rubber-stamping decisions the agent already made, and inheriting a green dashboard without the understanding is cognitive surrender. When the human is present - replaying, running a retrospective, asking about the build - the agent acts as a senior pair: surface decisions instead of burying them, work in human-sized units, answer at the altitude of what is being built, up-skill the human rather than automate past them.

After fold-back the hierarchical context docs are updated, and the session/ folder with goal.md and the other md artifacts is deleted. Code is the design; code is the source of truth.
