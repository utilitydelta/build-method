---
name: hierarchical-context-docs
description: How to write and maintain architecture docs that present a system to an agent in progressive detail, instead of dumping the whole codebase. Use when onboarding agents to a codebase, when grep and semantic search expose too much depth at once, or when reconstructing architecture is hard. A root file links down to subsystem docs, each level resting on the one above and tracing up.
---

# Hierarchical Context Docs

Grep and semantic search expose full depth with no shape: a thousand lines, no architecture. Give the agent a doc tree it descends root-first, following links into detail only when the task needs them. This is C4's zoom levels applied to prose.

The tree stops above the code. Code is the territory at the bottom and speaks for itself; the lowest doc level points into it and stops. Architecture is the middle band between system intent and source. Document that band, nothing the code already states.

## The shape

A tree of markdown, each level more detailed than the last, each linking down to the next.

- **L0 - root.** One file at the repo root. What the system is, what it is explicitly NOT, system-wide invariants, the map of subsystems, a link per subsystem. Read first; know the territory without reading code.
- **L1 - subsystem.** One file per major subsystem: its responsibility, its contract with the rest, its invariants, links to deeper design where it exists.
- **L2 and below - design detail.** The hard parts: a wire contract, a locking model, a failure-mode catalogue. Only subsystems that need this depth get it. Even here, stay above the code: name the file and the intent, do not transcribe the implementation.

The agent follows the links it needs and stops when it has enough. It never holds the whole codebase in context to understand one corner.

## Rules

- **Every level rests on the one above.** A reader of L1 already has L0's vocabulary. Do not redefine the system in each file.
- **Every level traces up.** A change or finding names the higher-level invariant or goal it serves. If it traces to nothing in L0, it is drift, reject it. This is what turns the doc tree from passive reference into an active filter on the work.
- **Link down, do not inline.** L0 names a subsystem and links to its L1. Depth is opt-in.
- **Invariants live as high as they hold, spread across the levels.** System-wide in L0, subsystem in its L1. Do not bury a load-bearing invariant three levels down, and do not herd them into one big invariants.md — an invariant lives at the level where it holds. Capture only the higher-level ones the code cannot show on its own; do not restate a constraint the code already enforces and makes obvious.
- **Map, not territory.** Point at code and state intent; never paste code, duplication drifts. Keep ruled decisions as ADR-style entries (context/decision/consequence) so rationale survives. These are not immutable: the doc reflects current architecture only. When a decision is reversed, rewrite or drop the entry — do not keep a superseded-decision trail. History lives in version control, not in the doc.
- **Current or deleted.** A stale architecture doc is worse than none, same as a stale comment. When a subsystem changes shape, fix its level.
- **One entry point.** L0 is where the agent starts. Make it discoverable: reference it from AGENTS.md / CLAUDE.md (or an llms.txt-style index) so the agent loads the root map first and descends from there, instead of grepping in cold.
