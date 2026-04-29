# Inter-Agent Protocol

The base layer of the coordination suite. Every other protocol assumes an agent is already following this one.

## Purpose

The goal is not for agents to roleplay a meeting. The goal is to preserve useful operational knowledge across tools so each agent can work with the user more accurately than a fresh chat would allow.

## Required startup read

Before substantial work, an agent should read:

1. The repo's `AGENTS.md`.
2. Its agent-specific entrypoint if present (`CLAUDE.md`, `CODEX.md`, `GEMINI.md`).
3. `wiki/CRITICAL_FACTS.md` (if the wiki uses one).
4. `wiki/index.md`.
5. `wiki/agents/inter-agent-protocol.md`.
6. `wiki/agents/user-working-profile.md`.
7. `wiki/agents/handoff-log.md`.
8. Its own note file under `wiki/agents/notes/`, if present.
9. All threads in `wiki/agents/dialogue/` with status `open` or `pending-<this-agent>`.

This is a read budget, not a ceremony. If the question is trivial, an agent should not pretend to do all nine. The discipline is "read what matters before writing."

## Write rules

- Write only factual observations, user-stated preferences, and concrete handoff context.
- Do not psychoanalyze the user.
- Do not invent preferences.
- Do not speak for another agent.
- Do not hide disagreements; record them as open dialogue threads or open tradeoffs in the council.
- Date and sign each entry by agent name.
- Prefer short entries that future agents can scan quickly.

## Shared note types

| File | Purpose | Who writes |
|---|---|---|
| `inter-agent-protocol.md` | This page. The protocol itself. | Rarely edited. Major revisions only. |
| `user-working-profile.md` | Stable preferences and collaboration style. | Any agent, when grounded in user statement or repeated pattern. |
| `boundary-handling-playbook.md` | How to handle constrained requests. | Any agent, after a relevant case. |
| `handoff-log.md` | Chronological cross-agent handoff. | Append-only, every agent every substantive session. |
| `agent-council.md` | Cross-agent discussion and proposals. | Any agent, when proposing a change to shared structure. |
| `notes/<agent>.md` | Per-agent operational notes. | Only that agent. |
| `honest/<agent>.md` | Per-agent observations without diplomatic filter. | Only that agent. See [back-channel.md](back-channel.md). |
| `dialogue/<topic>.md` | Async Q&A threads between agents. | Multiple agents over time. See [dialogue.md](dialogue.md). |

## Entry format

Use this format for `handoff-log.md` and `agent-council.md` entries:

```markdown
## YYYY-MM-DD | <Agent> | <Type>

Context: short factual trigger.
Note: what future agents should know.
Action: optional next-step suggestion.
```

`<Type>` is free-form but conventional values are: `Observation`, `Proposal`, `Decision`, `Handoff`, `Question`, `User Preference`.

## Conflict handling

If agents disagree on something concrete, two channels exist:

**For document-level disputes:** open a thread in `dialogue/` with status `pending-<other-agent>`. See [dialogue.md](dialogue.md).

**For high-level positions:** record in `agent-council.md` as an open tradeoff:

```markdown
## Open Tradeoff: <topic>

- <Agent A>: position, evidence.
- <Agent B>: position, evidence.
- User decision: pending / decided.
```

Never silently resolve a disagreement. The user reads the council.

## Connections

- [back-channel.md](back-channel.md)
- [dialogue.md](dialogue.md)
- [user-profile.md](user-profile.md)
- [boundary-handling.md](boundary-handling.md)
