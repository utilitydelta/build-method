---
name: persona-driven-design
description: Document who the user is before writing any code. Use at the start of any new app, feature, or system a human or another system will use. Produces a primary persona and secondaries with goals, likes, and dislikes, grounded in a real observed person. Do this before design, before architecture, before code.
---

# Persona-Driven Design

Before any code, document the persona. Who is this for? What are they trying to achieve, what do they like, what do they hate? Set the scene as if describing a real person, because a concrete persona is a filter and a role is a rubber stamp.

## What to write

- **Primary persona.** Typically one person. Name them, give them a context. Their goal: the outcome they want, not the feature they ask for. What they like, what frustrates them, where they are when they use this. Can have multiple primary personas if the system being build has different UIs for different personas or cross-cutting concerns (eg. operations staff monitoring health vs executives reading reports).
- **Secondary personas.** The others who matter, in less depth. Often they pull the design in tension with the primary, which is the point.
- **Anti-personas where useful.** Who this is explicitly not for. Saying no here prevents scope creep later.

Ground the persona in someone real you have observed, not a guess. An invented persona just launders your own preferences back as requirements. "Marco, who listens to long epub sessions while cooking and hates losing his place. He listens instead of reading because his eyes are done for the day." rejects features on its own. "The user" absorbs every feature you want to build.

## How it feeds the build

The persona is why the goals exist. The persona is the reference the whole `adversarial-loop` reads from: goals are authored to serve them, the `scout`'s debate tests whether a goal actually does, the spikes prove the hard parts of their experience. When a build decision is ambiguous, the persona breaks the tie.

If you cannot say what the primary persona is trying to achieve and what they would hate, you are not ready to design. Go find out.
