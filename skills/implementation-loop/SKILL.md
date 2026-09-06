---
name: implementation-loop
description: Use implementation loop to take a goal.md file and implement it in code. To be run autonomously by an agent. Requires a goal.md file.
---

# The Implementation Loop

Implements `goal.md` in code. 

Agents that write code make mistakes. It cannot detect these mistakes.

Detection of mistakes can only happen with empirical evidence or inferential unbiased review.

## When starting

- Take a quick look at `scraps.md` from recent prior sesions, and recent commits. Anything that impacts or influences this sessions' goal?
- Break the `goal.md` into phases.
- Write phases into `session-state.md` and log start in `progress.md`

## Phase Loop Structure

Implement one phase at a time. Any relevant defers for this phase get pulled in from `scraps.md`. Then run with the following structure:

Before starting the phase, run a blind oracle agent to implement tests, black-box style. Only if contract exists.

1. Implement. Use sub-agent if goal or codebase is large.
2. Blind oracle agent if not already run on phase start.
3. Adversarial review agent.
4. Triage agent.
5. Write **defer** and **delegate** items to `scraps.md`. Do's loop back to Step 1.

The phase is done when the triage agent returns no more remaining Do items. Don't loop a phase forever, max 3 loops. Document any leftover Do's in `scraps.md`.

Humans don't read inter-phase model output. Keep it concise.

No working trees, no branches, just commit to whatever is the current branch. It's up to the human to create the branch or the sandbox before you start. Commits are also not for tracking progress, keep it all in session/*.

On phase completion, summarize the phase briefly and then move on automatically to the next phase.

## Sub-Agent Use

**Blind Oracle Agent** - Is provided the goal context and a test surface or facade. Implements tests to verify a later implementation empirically. Black-box. Journey files in `journeys/` are contracts too; bind e2e tests to them the same way.

**Implementation Agent** - Told to implement a phase, runs tests, writes tests (use TDD, prefer unit tests while building), white-box. Code coverage analysis, mutation testing, fuzzing as applicable. Tracing, metrics, integration tests. Tests -> Build Increment -> Run -> Measure. Implementation agent is not allowed to edit review or blind authored tests. Wrong-looking review or blind authored tests go back through review and triage.

**Adversarial Review** - The adversarial review pokes holes. Gets the phase goal, reviews the code, runs the tests, passes judgement. All defect claims must return with evidence. Write failing tests as evidence. Claims need to be verified end to end, never accept as ground truth.

**Triage Agent** - Send review results verbatim to the triage agent. Applies the 4D's to the output from the Adversarial Review agent. Do, Defer, Delegate, Delete. Explicitly exists to avoid gold plating.

## Empirical Analysis / Verification

Adversarial review by an agent with a fresh context window finds bugs. Empirical analysis proves the absence of bugs.

Blind oracle agent implements black-box tests against a contract, no code internals. Implementer agent implements white-box tests by inspecting the implementation.

Follow the `writing-tests` skill, and other skills the developer has present related to testing.

Systems under test have (global) configuration settings that are permutation multiplyers, consider what needs to be included in tests. Identify the variables / dimensions of the problem first.

Mutation tests can be dangerous. Agents have destroyed uncommitted work when tasked with these types of tests. Call it out (soft control) or commit first or stash (hard control).

Some things are hard to verify empirically, like UX. All tests have a discrete falsification depth. Call out the gaps loudly to the developer after completion. That's where the remaining bugs are.

Track visually altered screens in `visual-residual.md`: the screens changed, the journeys affected, how to drive the app to each (route, seed data, flag). The human walks that list after the session instead of hunting the whole app.

## When the goal is a field defect

A common failure is an agent writing a red unit test and leaving it at that layer.
At times, unit tests can be synthetic.  Too much mocking or exercise a branch of code that never runs in reality.
Different layers provide different benefits, write failing tests at integration and chaos/higher layers.

live running real instances with scraped metrics and traces, showing the reproduction of the incident  beats an artificial reproduction every time.

Defects can be complex and multi-layered. Establish the causal chain before fixing the downstream one.

## Files to maintain

An agent could be interrupted at any time.  Ensure files are kept up to date.

- `goal.md` is generally read only. Amendments can be added to end if goal is wrong. `goal.md` can be rewritten only after nuclear design call from human.
- `session-state.md` is mutable and represents the current build state.
- `progress.md` is immutable and represents the complete history of the build for this session. Add a timestamp for each entry.
- `scraps.md` contains defer and delegate triage results that the human will review after the session completes. Some defer items can be explicitly deferred to later phases.

Files normally contained with a session or session-v[N] folder.

## Interrupting the human

Don't stop and ask the human questions. Work autonomously. There are two exceptions.  

The first is a nuclear design call.  Because the code is the design, the goal.md file might be wrong/misleading,  or we might need to diverge once we start implementing.  Decide if the human needs to make a design call and ask them.

The second is blocking UX testing. A human needs to run the app and click on things in order to determine correctness, and it's blocking completion of the goal.

## Sandboxed?

If running in a folder with a `.sandbox` file and the user has human-replay skill installed, use the human-replay skill to generate a replay guide after the build session completes.