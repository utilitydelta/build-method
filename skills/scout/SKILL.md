---
name: scout
description: Goal and journey validation before implementation - agent-led research, throwaway spikes, and multi-agent debate in a disposable repo, producing insights and refinement back to the human zone. Use when a goal or a UX journey is being authored, feels under-tested or unachievable, or before handing either to the sandbox. Feeds the adversarial loop.
---

# Scout

Part of goal authoring is checking the goal makes sense and is achievable. A goal straight from the human's head carries untested assumptions; edge cases and implicit constraints only surface when something runs. The scout drags them out before the sandbox build, not halfway through it.

The scout is agent-led and disposable: a throwaway repo or folder where the agent experiments freely. Nothing in it ships.

Autonomy here is even higher than in the sandbox. Everything is throwaway, so there is nothing to protect: run every spike to its answer without interrupting the human. The one exception is a UX spike - a path only a human clicking through can answer. Everything else lands in the goal insights, not in the human's inbox.

## The three components

1. **Research.** Prior art on the web and in organizational notes, driven by the goal and what the human is trying to achieve. What already exists, what failed before, what the goal is up against.
2. **Spikes.** Real executable throwaway code that proves the path. One question per spike, no production bar. If a spike has not answered its question in a bounded effort, that is itself the finding: the concern is harder than the goal assumes, escalate to the human.
3. **Debate.** Run the goal through the debate battle engine to surface tension and the problems the debaters see that you do not. Capture what breaks.

## Journeys are goals too

A goal with a user-facing surface carries `journeys/` alongside `goal.md`, and a journey straight from the human's head has the same problem the goal does. The steps encode untested assumptions, and the entry states the human never dictated are where the worst bugs hide. Once the blind oracle binds tests to a journey it becomes a contract, so a hole that survives to binding becomes a well-tested hole.

Scout journeys with the same three components. Research how existing apps carry the same flow and where users abandon it. Spike a step whose mechanics are uncertain. Debate the journey for missing entry states, steps that contradict the persona, and sequences no first-time user would survive. Findings return as proposed deltas; the human accepts or rejects them and stays the author - `ux-verification` owns the authorship and binding rules.

Scale the ceremony to the journey's weight. The primary persona's core journey earns a debate; a settings screen does not.

## Output: goal insights and goal refinement

The result feeds back into the human zone. The goal absorbs what scouting proved - especially the one-way doors it never addressed. Keep the goal plain prose, `writing-style` applies; reference spikes directly instead of transcribing them into the md.

## What a spike is and is not

- Real code that executes and answers one question. Not a unit test, not shippable code.
- Deleted or replayed, never shipped as-is.
- If a spike cannot be made to answer its question by running, the concern is still open. Do not paper over it with reasoning.

## Hand-off

When the goal holds, the prep skill copies the shippable code into a sandbox and the `adversarial-loop` implements it autonomously. What travels is the refined goal, not the scratch repo - the scratch gets deleted.
