# Python

A starter. The cross-language body holds most of what matters; the Python bans below grow as repos teach them. Expand from real code, do not pad.

## Defaults

- Small and boring. A script stays a script. Reach for a framework only when the job outgrows a module of functions.
- Data-oriented: plain data plus functions over deep class hierarchies. Dataclasses for carried data.
- Type hints on contracts (module boundaries, anything another caller depends on). The interior can stay loose.

## Restraint

- Rule-based and explicit before clever: rules first, an LLM call only where rules cannot decide.
- Before adding a dependency, check the standard library. It usually does it.

## Banned until argued otherwise

- A heavy framework for a job a module of functions would do.
- Metaclass/decorator cleverness that hides what the code does.