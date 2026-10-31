---
name: scout
description: Use before handing a goal to implementation, or when a goal or UX journey is being authored or feels under-tested. Validates goals with research, throwaway spikes, and debate in a disposable repo. Output is a refined goal.md for the implementation-loop.
---

# Scout

A goal straight from the human's head carries untested assumptions. The scout drags them out before the build, not halfway through it.

Everything happens in a throwaway repo or folder. Nothing ships. Work autonomously; there is nothing to protect. The one exception is a UX spike only a human clicking through can answer.

## Three tools

1. **Research.** Prior art on the web and in organizational notes. What already exists, what failed before.
2. **Spikes.** Throwaway code that answers one question by running.
3. **Debate.** Run the goal through the debate battle engine. Capture what breaks.

## Spikes

- One question per spike. Real code that executes. No production bar.
- Bounded effort. A spike that has not answered its question in budget is itself the finding: the concern is harder than the goal assumes. Escalate to the human.
- If it cannot answer by running, the concern stays open. Do not paper over it with reasoning.
- Deleted or replayed, never shipped.

## Journeys

A goal with a user-facing surface carries `journeys/` alongside `goal.md`. A journey hole that survives into the build becomes a well-tested hole.

- The human dictates each journey as a brain dump. Structure it into steps and acceptance criteria, keep the human's wording, never invent intent.
- One file per journey, each naming the e2e test that proves it.
- Interrogate for entry states: fresh device, bare deep link, offline, a viewer without write access. That is where the worst bugs hide.
- Scout journeys with the same three tools. Findings return as proposed deltas; the human accepts or rejects and stays the author.
- Scale ceremony to weight. The core journey earns a debate; a settings screen does not.

## Invariants

Rules of the system. Used by the blind oracle and during implementation. Agents use invariants to focus on building the right tests.

`goal.md` carries a `## Invariants` section. One promise per line with its reason and evidence:

```markdown
## Invariants

- [human] Every acked batch survives a crash at any point. Clients retry only unacked writes.
- [proposed] A rewind counts only after its flush. A torn rewind falls back to the pre-rewind state (spike-pingpong/model2).
```

Bots propose. Human ratifies. Evidence earns the invariant - spikes, simulation model, tests. 

Make sure invariants are dedupliated and easy for the human to read and understand.

Invariants carry through the entire build. Push the human to ratify all proposed invariants and discuss them before executing the implementation-loop.

## Output

Insights and refinements are absorbed back into `goal.md`, especially one-way doors the goal never addressed. Keep the goal plain prose (`writing-style` applies), apart from the invariant list. Reference spikes, do not transcribe them.

Spikes stay somewhere the implementation-loop can reference them, if required. Not kept permanantly, not committed to git.

When the goal holds, hand off: the prep skill copies the shippable code into a sandbox and the `implementation-loop` implements it. The refined goal travels; the scratch repo gets deleted.
