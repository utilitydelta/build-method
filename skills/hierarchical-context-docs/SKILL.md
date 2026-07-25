---
name: hierarchical-context-docs
description: How to write and maintain architecture docs that present a system to an agent in progressive detail, instead of dumping the whole codebase. Agents implementing new code features or refactoring work may need to update these documents.
---

# Hierarchical Context Docs

Some code bases are too complex to search directly. Maintain a series of .md files in a `docs/` folder that has a hierarchical structure.

These are not architectural design records. They represent the current state of the system. Everything is in source control, ruthlessly prune out-of-date documentation.

## The shape

A tree of markdown files, each level more detailed than the last, each linking down to the next.

- **L0 - root.** - One `docs/ARCHITECTURE.md` file. What the system is, what it is explicitly NOT, system-wide invariants, the map of subsystems, a link per subsystem.
- **L1 - subsystem** - One file per major subsystem: its responsibility, its contract with the rest, its invariants, links to deeper design where it exists.
- **L2 - subsystem details** - Only subsystems that need this depth get it. Do not include the code. The code speaks for itself. The code is the design. .md files only exist to compress this information.

The agent follows the links it needs and stops when it has enough. It never holds the whole codebase in context to understand one corner.

## Rules

- Markdown files link down the tree. They never link back up to parents.
- Follow the `writing-style` skill. Preference `compressed-mode` if possible. You are writing for agents and a technical audience.
- Don't link to specific code files or line numbers. These change all the time.
- Place system invariants at the right level. Placing them too high in the document hierarchy creates noise. Placing them too low risks them not being discovered by agents.
- Only current system state. Do not include implementation phases, design history or anything that's no longer current state for the system. Delete anything that references old system state.