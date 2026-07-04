---
name: comment-discipline
description: How to write code comments and keep them from rotting. Use whenever adding or editing comments, and when finishing a build driven from a spec. Stops the three failures - verbose narration, comment drift, and comments carrying build history with linkbacks to spec files that no longer exist.
---

# Comment Discipline

Agents comment like they narrate. Three failures to kill.

## 1. Verbose narration

- A comment explains why, not what. The code says what. If it restates the line below, delete it.
- Follow a human prose for comments. See `writing-style` skill.
- Earn it: the reason for an odd choice, an invariant held, a bug guarded against, a citation (an RFC section, the file:line this mirrors, an invariant id).

## 2. Comment drift

A wrong comment is worse than none, because the reader trusts it.

- When you change a line, read the comment above it. If the change moved it out of sync, fix it or cut it.
- Anchor comments to things that change slowly: invariants, contracts, intent. Not to line behaviour that will shift.

## 3. Build history and dead linkbacks

Agents building from a goal leave a trail: "implements Phase 3 of session/goal.md", "see spec 4.2". After fold-back the session/ folder with the goal and the other md artifacts is deleted and the comment links to nothing.

- Strip build scaffolding from shipped comments: phase numbers, spec references, plan TODOs.
- Keep durable citations. A dead build-plan linkback (`session/goal.md Phase 3`) gets stripped; a real citation (an RFC section, a stable `file:line` mirror, an invariant id) is a keeper. That distinction is the hard case: do not strip the citations with the scaffolding.

## The pass before done

One comment pass before done: cut narration, fix or cut drifted comments, strip every spec/plan linkback that is not a durable citation.
