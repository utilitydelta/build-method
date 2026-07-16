---
name: ux-verification
description: How an agent proves UX journeys still work without a browser or a vision model - human-dictated journey files bound to oracle-authored tests, telemetry and geometry assertions, and a visual-residual ledger handed back for human replay. Enables when the app repo has a journeys/ folder. Use when building or reviewing anything with a user-facing surface, when authoring journeys from a human brain dump, or when a UX regression slipped past green tests.
---

# UX Verification

An agent deep in code details loses the user. Journey docs alone do not stop it, and neither does a green e2e suite. A journey with no bound test is invisible to the loop, and human-found bugs cluster exactly there. An implementer that authors its own tests writes tests that confirm what it already believed.

No vision models anywhere in this skill. Screenshot-reading LLMs are slow, expensive, and wrong too often to gate anything. Every check below is deterministic or human.

## Journeys are human-authored, agent-structured

The human dictates each journey as a fluent brain dump. The agent turns it into steps and checkable acceptance criteria, keeps the human's wording, and never invents intent.

Then interrogate. Ask what happens on a fresh device, a bare deep link, offline, a viewer without write access. Prose journeys skip entry states unless prompted, and entry states are where the ugliest bugs hide. Record the answers in the journey file.

One file per journey in `journeys/`. Frontmatter carries id, persona, entry states, and bound test ids. A new or changed journey goes through the `scout` before the oracle binds tests to it - a hole that survives to binding becomes a well-tested hole.

## Binding, not vibes

- Every journey names the e2e test that proves it. `verify:journeys` fails on unbound journeys and dangling test ids, in the review phase and in CI. It proves binding, not adequacy.
- The blind oracle writes the journey's e2e tests from the journey file alone, in fresh context, before implementation. The journey file is the specification; the test is its proof. The implementer never edits oracle-authored tests; review rejects any diff that touches one.
- A bug fix ships with a new journey e2e test that covers it, or an existing one updated.
- E2e asserts what the user sees. Dev hooks serve setup and state reads; a `window.__` read inside `expect()` is lint-banned.

## What the agent can check without eyes

- End every journey test by asserting the expected bus-event sequence and that no invariant tripwire fired. Wiring and timing bugs hide behind a correct-looking DOM.
- When one state renders in two places, assert the id sets match across DOM, scene, and projection at journey checkpoints. Unit tests on each side stay green while the views disagree.
- Overlays get geometry sanity assertions. Width above a floor, inside the viewport, no page overflow. Plain `getBoundingClientRect` numbers catch the squished-menu class.
- `toHaveScreenshot` against a human-approved baseline is a byte diff, not image interpretation. Optional; skip it where baseline churn costs more than it saves.

## The visual-residual ledger

Some things only eyes catch. Mis-centered text, spacing, feel. The agent makes the call, keeps building, and banks the debt in `session/visual-residual.md` - each screen it visually altered, the journeys affected, and how to drive the app into that state (route, seed data, debug flag). Phase review checks the ledger moved when views did.

At replay the ledger is the walk list. These screens changed, check exactly these in the running app. A targeted pass, not a hunt.

## Flakes

A flaky bound journey test is never fixed by the implementer editing it - that is weaken-until-green. Quarantine and escalate. Mark the journey unbound, file a finding for human triage, keep the loop moving. Most flakes are test-side timing; the human decides which ones are product bugs.
