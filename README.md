# build-method

The engineering method, as Claude Code skills. The things I would otherwise re-explain at the start of every build, written once and loaded everywhere.

Why does this exist? An agent left alone writes code that looks right, and looking right is not evidence. The method makes the agent prove its work empirically instead: a goal is validated by a scout before it costs anything, built autonomously under an implementation loop where every phase must survive its tests and a fresh-context adversarial review, and folded back into the shippable code by a human who replays every decision. The grind goes to the agents. The understanding stays with the human.

This is the cross-cutting layer. It sits above any one repo. It does not know about any one repo's domain or wire contracts - those live in the repos that need them. This is how I build, regardless of the stack.

![The build method](build-method.png)

## The skills

The keystone is `implementation-loop`. The rest feed it or check it.

| Skill | What it pins down |
|---|---|
| `implementation-loop` | The phase loop: blind oracle writes black-box tests, implement with TDD, adversarial review, 4D triage into `scraps.md`. Autonomous, max 3 loops per phase. |
| `scout` | Goal and journey validation: research, spikes, and debate in a throwaway repo. Output is a refined `goal.md`. |
| `writing-tests` | Which layer (unit, integration, DST, chaos), unit test rules, the mocking ladder, property/fuzz/mutation, UI and e2e checks without vision models. |
| `coding-rules` | Data-oriented, low-state, library restraint, comment rules. Per-language idioms and bans in `references/`. |
| `persona-driven-design` | Document a real persona before any code. Why the goals exist and who they serve. |
| `hierarchical-context-docs` | L0 to Lx architecture docs that disclose progressively instead of dumping the codebase. |
| `performance-discipline` | Performance as an invariant: benchmark, flamegraph, the per-decision cost choices. |
| `writing-style` | The prose rules for docs, comments, commits, and conversation. |
| `compressed-mode` | Get rid of the default LLM response prose to save your reading time and tokens. |

## Install

Inside of Claude Code run:

```
/plugin marketplace add utilitydelta/build-method
/plugin install build-method@build-method
```

Once installed, the skills load in every session regardless of which repo you launch from. No git-boundary problem, no global skills folder.

## Adjacent work

- [human-replay](https://github.com/utilitydelta/human-replay) - sandbox prep, replay-guide generation, and the VS Code replay extension. The method's prep and replay stages.
- [human-replay-vscode-extension](https://marketplace.visualstudio.com/items?itemName=UtilityDelta.human-replay) - make human replay fun, just hit `tab` and the magic happens.
- [debate-battle](https://github.com/utilitydelta/debate-battle) - the multi-agent debate engine the scout runs goals through.
- [react-mobx-mvvm](https://github.com/utilitydelta/react-mobx-mvvm) - my opinionated take at how to build front end with agents using MVVM.

## License

MIT. See [LICENSE](./LICENSE).
