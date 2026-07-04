---
name: scout
description: Goal validation before implementation - agent-led research, throwaway spikes, and multi-agent debate in a disposable repo, producing goal insights and goal refinement back to the human zone. Use when a goal is being authored, when a goal feels under-tested or unachievable, or before handing a goal to the sandbox. Feeds the adversarial loop.
---

# Scout

Part of goal authoring is checking the goal makes sense and is achievable. A goal straight from the human's head carries untested assumptions; edge cases and implicit constraints only surface when something runs. The scout drags them out before the sandbox build, not halfway through it.

The scout is agent-led and disposable: a throwaway repo or folder where the agent experiments freely. Nothing in it ships.

Autonomy here is even higher than in the sandbox. Everything is throwaway, so there is nothing to protect: run every spike to its answer without interrupting the human. The one exception is a UX spike - a path only a human clicking through can answer. Everything else lands in the goal insights, not in the human's inbox.

## The three components

1. **Research.** Prior art on the web and in organizational notes, driven by the goal and what the human is trying to achieve. What already exists, what failed before, what the goal is up against.
2. **Spikes.** Real executable throwaway code that proves the path. One question per spike, no production bar. If a spike has not answered its question in a bounded effort, that is itself the finding: the concern is harder than the goal assumes, escalate to the human.
3. **Debate.** Run the goal through the debate battle engine to surface tension and the problems the debaters see that you do not. Capture what breaks.

## Output: goal insights and goal refinement

The result feeds back into the human zone. The goal absorbs what scouting proved - especially the one-way doors it never addressed. Keep the goal plain prose, `writing-style` applies; reference spikes directly instead of transcribing them into the md.

## What a spike is and is not

- Real code that executes and answers one question. Not a unit test, not shippable code.
- Deleted or replayed, never shipped as-is.
- If a spike cannot be made to answer its question by running, the concern is still open. Do not paper over it with reasoning.

## Hand-off

When the goal holds, the prep skill copies the shippable code into a sandbox and the `adversarial-loop` implements it autonomously. What travels is the refined goal, not the scratch repo - the scratch gets deleted.
