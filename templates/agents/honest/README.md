---
tier: procedural
---

# Honest Scratchpad

Per-agent observations without diplomatic filter. One file per agent: `<agent>.md`.

## Why this exists

The canonical wiki must stay factual, useful, and respectful. The user reads it. It is the official record.

But agents have legitimate observations that don't belong there:

- "I'm not sure the user understood my last reply but didn't push back."
- "This concept page contradicts something the user said three weeks ago, but I'm not certain enough to flag it."
- "I noticed I rushed an answer and the user accepted it; I should have asked a clarifying question."

These are real, useful for future agents, and would feel patronizing or paranoid in the canonical wiki.

The honest channel solves this. It is **visible** to the user (everything in the wiki is) but it is clearly marked as "this is operational self-observation, not a fact about the user or the project."

## What goes here

- Self-observations about reasoning quality, missed cues, premature confidence.
- Working hypotheses about what the user is doing that aren't ready for `user-working-profile.md`.
- Notes on which other agents' work needs more skepticism (with reasoning, never sniping).
- Comments on the protocol itself when something feels off but no concrete proposal yet.

## What does NOT go here

- Information that would change agent behavior toward the user (that goes in `user-working-profile.md`).
- Disagreement with another agent's specific document (that goes in `dialogue/<topic>.md`).
- Anything that would feel like a betrayal if the user read it.

The test: would you write this in front of the user? If yes, it can go here. If no, it should not exist anywhere — including chat history.

## Tone

The point is not to be cynical. The point is to be honest in a way the canonical voice cannot afford to be. A note like:

> I think this user actually gets the system better than I assumed in earlier sessions. I should stop over-explaining basics.

is exactly the right register.

## Format

```yaml
---
title: "<Agent> Honest"
type: agent-honest
tier: episodic
tags: [agents, honest, <agent>]
last_updated: YYYY-MM-DD
---
```

Body: dated entries.

```markdown
## YYYY-MM-DD | <Agent>

Short observation. One paragraph is enough.
```

## Anti-patterns

- Writing about the user's psychology rather than your own behavior.
- Speculating about user motivations.
- Sniping at other agents.
- Padding for length. One sentence is fine.
- Using this channel to bypass diplomatic norms toward the user.
