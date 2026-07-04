# TypeScript / JavaScript

The frontend is MVVM, local-first, and built to be tested in the dark: no browser, no DOM, no live system. [react-mobx-mvvm](https://github.com/utilitydelta/react-mobx-mvvm) is the reference implementation; this is the shape.

## MVVM

- **Views are thin.** A `*View.tsx` is an `observer()`-wrapped component that resolves a ViewModel and binds to it. No business logic, no fetching, no state machine in the component.
- **Logic lives in ViewModels.** A `*Store.ts` class holds presentation state and logic. This is what you test, with no DOM.
- If proving a behaviour needs a browser harness to render and click, the logic is in the wrong layer. Move it down to the ViewModel.

## MobX, kept simple

- Observable state, actions, computed. That is the whole vocabulary.
- Async store methods are auto-wrapped (Babel flow transform); use `runInAction` only for mutations in a callback that fires later. Do not sprinkle it: get it wrong and mutations silently fail to track.
- Avoid the clever surface: elaborate `reaction`/`autorun` webs, deep observable graphs, decorators-as-magic. They hide the data flow.

## Wrap the platform

- Browser APIs are injectable services, not libraries. Navigation, keyboard, connectivity, toasts: wrap `window.*` / `document.*` behind a service you own and inject.
- No `react-router`, no keyboard/toast/connectivity libraries. Each is a thin service over the platform. Wrapping is almost always cleaner and stays testable in the dark.

## DI

- The container is hand-rolled, ~40 lines, no decorators, no `reflect-metadata`, no third-party container. Register services and stores explicitly.

## Local-first and events

- IndexedDB event sourcing, PWA. State is local and durable first; sync is layered on top.
- A typed event bus (`AppBus`) for cross-object events. Choose dispatch deliberately: fire-and-forget, awaited-parallel, or awaited-sequential. Not global FIFO by default.
