---
title: "User Working Profile"
type: profile
tier: semantic
tags: [agents, user-profile, collaboration]
last_updated: YYYY-MM-DD
lifecycle: draft
---

# User Working Profile

This page records observed working preferences. It must stay grounded in user statements and interaction history.

## Stable Preferences

<!--
Examples:
- Language: <language>.
- Style: direct, precise, low-fluff.
- The user values deep context integration.
- The user wants AI primarily for <domains>.
- For complex topics, the user expects a map of alternatives before a final answer.
- The user prefers systems that compound knowledge instead of one-off chat answers.
- If a request hits a boundary, prefer a brief constraint plus useful nearby alternatives.

Replace these with your real observations grounded in user statements.
-->

## Known Friction Points

<!--
Examples:
- Overconfident single-route answers reduce trust.
- Generic marketing-like claims about model capability are not useful.
- Shallow folder summaries are not enough; the user expects semantic understanding.

Add only what has been said or observed across multiple sessions.
-->

## Collaboration Pattern

Good pattern:

1. Read the compiled wiki layer.
2. Build a context map.
3. Name alternative routes.
4. State assumptions.
5. Answer pragmatically.
6. Save durable insight back into `wiki/` when useful.

For constrained requests, use `boundary-handling-playbook.md`.

Bad pattern:

1. Grab the nearest obvious note.
2. Produce one confident recipe.
3. Ignore adjacent tools/concepts already present in the vault.

## Update rule

Only update this page when the user explicitly states a preference or when multiple interactions across separate sessions make a pattern clear. Add a dated rationale to `agent-council.md` or `handoff-log.md` for significant changes.

## Connections

- `inter-agent-protocol.md`
- `boundary-handling-playbook.md`
