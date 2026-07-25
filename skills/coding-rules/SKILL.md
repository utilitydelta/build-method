---
name: coding-rules
description: Use when writing or reviewing code in any language. Data-oriented design, minimal state, no temporal coupling, library restraint, comment rules. Per-language idioms and bans in references/ for Python, TypeScript/JavaScript, C#/.NET, Rust.
---

# Coding Rules

Cross-language defaults. Per-language idioms and bans live in `references/`, loaded only for the language in use:

- Rust - `references/rust.md`
- C# / .NET - `references/dotnet.md`

A repo's own skill overrides these where they disagree.

## Data-oriented design

- Lead with the shapes the data takes and the transformations over it, not the object hierarchy.
- Plain data plus functions over rich objects that hide state and behaviour together.
- Lay data out for how it is accessed on the hot path. See `performance-discipline`.

## Minimal state, no temporal coupling

- Minimize state held in classes. State is where bugs hide.
- No methods that only work in a specific order, no init-then-use-then-teardown dance. If order matters, the types enforce it.
- Construct objects fully formed. A half-initialised object is a trap.
- RAII over code that must remember to clean up at the end.

## Library restraint

- Use the smallest, most boring subset of a library that does the job. MobX is the standing example: kept to its boring subset because the clever features hide the data flow.
- A feature that saves five lines but makes the data flow non-obvious is a bad trade.
- Before adding a dependency for something small, wrap the platform instead.

## Comments

- A comment explains why, not what. If it restates the line below, delete it.
- A comment earns its place: the reason for an odd choice, an invariant held, a bug guarded against, a durable citation (RFC section, stable file:line mirror, invariant id).
- A wrong comment is worse than none; the reader trusts it. When you change a line, read the comment above it. Out of sync means fix or cut.
- Anchor comments to what changes slowly: invariants, contracts, intent. Not line behaviour.
- Before done, strip build scaffolding: phase numbers, spec references, plan TODOs, links into the session folder. Keep the durable citations. Do not strip those with the scaffolding.

## Banned constructs

A construct that makes code hard to reason about, hard to test in the dark, or that hides state and ordering goes on the language's banned list in `references/`.

Low-state, data-oriented code is cheap to test without a heavy harness. That is what the `implementation-loop` needs. The style exists to make verification cheap, not for aesthetics.
