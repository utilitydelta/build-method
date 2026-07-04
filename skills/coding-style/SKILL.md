---
name: coding-style
description: Cross-language code-craft preferences - data-oriented design, minimal state in classes, no temporal coupling, restraint with powerful libraries, and the per-language idioms and bans. Use when writing or reviewing code in Python, JavaScript, TypeScript, C#/.NET, or Rust. Body sets the cross-language defaults; load the matching references/<lang>.md for the stack you are in.
---

# Coding Style

The same preferences hold across Python, JavaScript, TypeScript, C#/.NET, and Rust. This body sets the cross-language defaults. Per-language idioms and bans live in the reference files, loaded only when you are in that language:

- Rust - `references/rust.md`
- TypeScript / JavaScript - `references/typescript.md`
- C# / .NET - `references/dotnet.md`
- Python - `references/python.md`

A repo's own skill, if it has one, overrides these where they disagree.

## Data-oriented design

- Model the data and the transformations over it. Lead with the shapes the data takes, not the object hierarchy.
- Prefer plain data plus functions over rich objects that hide state and behaviour together.
- Lay data out for how it is actually accessed, especially on a hot path. See `performance-discipline`.

## Minimal state, no temporal coupling

- Minimize state held inside classes. State is where bugs hide and reasoning gets hard.
- Kill temporal coupling: methods that only work in a specific order, objects with an init-then-use-then-teardown dance. If order matters and the types do not enforce it, it will be got wrong.
- Construct a thing fully formed over building it up across calls. A half-initialised object is a trap.
- Follow RAII patterns instead of code that must 'remember' to call certain functions at the 'end' of a routine

## Library restraint

- Use the smallest, most boring subset of a library that does the job. MobX is the standing example: capable of a lot, kept to its boring subset because the clever features hide the data flow.
- A feature that saves five lines but makes the data flow non-obvious is a bad trade.
- Before pulling a dependency for something small, ask whether wrapping the platform is cleaner. Often it is.

## Banned lists

Some constructs are too sharp and go on the per-language banned list in the references. The principle is constant: if a construct makes the code hard to reason about, hard to test in the dark, or hides state and ordering, it is a candidate for the ban.

## Why this shape

Decoupled, low-state, data-oriented code is structurally easy to test without a heavy harness, including in the dark with no browser. That is what the `adversarial-loop` needs. The style is what makes the verification loop cheap, not aesthetic preference.
