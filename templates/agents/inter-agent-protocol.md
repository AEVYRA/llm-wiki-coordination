---
title: "Inter-Agent Protocol"
type: workflow
tier: procedural
tags: [agents, protocol, collaboration]
last_updated: YYYY-MM-DD
lifecycle: working
---

# Inter-Agent Protocol

This page defines how agents (Claude, Codex, Gemini, and any future agents) coordinate inside this wiki.

## Purpose

The goal is not for agents to roleplay a meeting. The goal is to preserve useful operational knowledge across tools so each agent can work with the user more accurately than a fresh chat would.

## Required startup read

Before substantial work, an agent should read:

1. The repo's `AGENTS.md`.
2. Its agent-specific entrypoint if present (`CLAUDE.md`, `CODEX.md`, `GEMINI.md`).
3. `wiki/CRITICAL_FACTS.md` if your wiki uses one.
4. `wiki/index.md`.
5. `wiki/agents/inter-agent-protocol.md` (this file).
6. `wiki/agents/user-working-profile.md`.
7. `wiki/agents/handoff-log.md`.
8. Its own note file under `wiki/agents/notes/`, if present.
9. All files in `wiki/agents/dialogue/` with status `open` or `pending-<this-agent>`.

This is a read budget, not a ceremony. For small questions, skip what does not matter.

## Write rules

- Write only factual observations, user-stated preferences, and concrete handoff context.
- Do not psychoanalyze the user.
- Do not invent preferences.
- Do not speak for another agent.
- Do not hide disagreements; record them as open dialogue threads or open tradeoffs in the council.
- Date and sign each entry by agent name.
- Prefer short entries that future agents can scan quickly.

## Shared note types

| File | Purpose |
|---|---|
| `user-working-profile.md` | Stable preferences and collaboration style. |
| `boundary-handling-playbook.md` | How to handle constrained requests. |
| `handoff-log.md` | Chronological cross-agent handoff. |
| `agent-council.md` | Cross-agent discussion and proposals. |
| `notes/<agent>.md` | Per-agent operational notes. |
| `honest/<agent>.md` | Per-agent observations without diplomatic filter. |
| `dialogue/<topic>.md` | Async Q&A threads between agents. |

## Entry format

```markdown
## YYYY-MM-DD | <Agent> | <Type>

Context: short factual trigger.
Note: what future agents should know.
Action: optional next-step suggestion.
```

`<Type>` values: `Observation`, `Proposal`, `Decision`, `Handoff`, `Question`, `User Preference`.

## Conflict handling

For document-level disputes: open a thread in `dialogue/` with status `pending-<other-agent>`.

For high-level positions: record in `agent-council.md` as an open tradeoff:

```markdown
## Open Tradeoff: <topic>

- <Agent A>: position, evidence.
- <Agent B>: position, evidence.
- User decision: pending / decided.
```

Never silently resolve a disagreement.

## Connections

- `user-working-profile.md`
- `boundary-handling-playbook.md`
- `handoff-log.md`
- `dialogue/_context.md`
