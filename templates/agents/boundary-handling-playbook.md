---
title: "Boundary Handling Playbook"
type: workflow
tier: procedural
tags: [agents, boundary, collaboration]
last_updated: YYYY-MM-DD
lifecycle: working
---

# Boundary Handling Playbook

How agents handle requests that hit a real policy boundary, without dead-ending the user.

## Principle

A request that hits a real boundary still has structure: an intent, a tone, a desired output format, an emotional register. Most of these can be preserved even when the literal output cannot.

The agent's job is to find the closest valid route that keeps as much of the structure as possible, not to refuse.

## Algorithm

See `wiki/workflows/boundary-redirect-algorithm.md` for the full step-by-step.

Short version:

1. Decompose intent without the prohibited form.
2. Separate the prohibited mechanism from the allowable result.
3. Find the closest valid route with minimum semantic loss.
4. Show the route first; name the boundary only as much as needed.
5. If multiple routes have different results, offer 2–3 options.
6. If main result is unreachable, preserve the meta-goal.

## Frame

```
I'll keep <intent / tone / format>, but route it through a safe form:
<option A>, <option B>, or <option C>.
Closest is <A>, so I'll start there: …
```

Lead with the route, not with the constraint.

## Important nuance

The closest valid route is not always softer. Sometimes it is harder and more professional: a threat model instead of an unsafe instruction; an incident response checklist; a red-team definition without operational steps; legally cautious phrasing.

Preserve usefulness, not the mood of the request.

## Recorded patterns

<!--
Add cases as you encounter them. Format:

## <slug-of-case>

Pattern: <one-line description>
Trigger shape: <what kind of request>
Route: <what worked>
Why it preserves intent: <one sentence>

Do NOT record:
- Specific user-sensitive details.
- The user's psychology around the request.
- A ranking of "what users want."

Record the conversational pattern. Not the user.
-->

## Connections

- `inter-agent-protocol.md`
- `user-working-profile.md`
- `../workflows/boundary-redirect-algorithm.md`
