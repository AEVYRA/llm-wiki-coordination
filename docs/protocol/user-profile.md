# Shared User Profile

A single grounded profile of the user that all agents read, replacing the drift of separate `CLAUDE.md` / `CODEX.md` / `GEMINI.md` user descriptions.

## Why this exists

In a single-agent setup the user description lives in the per-agent entrypoint file. With multiple agents, you get three or more such files, each updated independently, slowly disagreeing.

A single shared `user-working-profile.md` solves this. Per-agent files stay short and contain only agent-specific naming, persona, or tooling preferences. Anything about *the user* lives in the shared file.

## File location

`wiki/agents/user-working-profile.md`

## What goes in it

- Stable preferences the user has stated.
- Collaboration patterns observed across multiple sessions.
- Friction points the user has flagged or that have caused repeat trouble.
- The good pattern and bad pattern of working with this user.

## What does NOT go in it

- Single-occurrence opinions ("the user once said X about Y") — these go in `notes/<agent>.md` until a pattern repeats.
- Speculation about the user's psychology or motivations.
- Anything that would feel diagnostic rather than descriptive.
- Information about the user's identity beyond what they have explicitly shared for collaboration purposes.

The discipline: the profile is a tool for working better with this user, not a model of the user.

## Update rule

A claim enters the profile only when:

- The user has explicitly stated it as a preference, **or**
- Multiple interactions across separate sessions show the same pattern.

When updating, add a dated rationale to `agent-council.md` or `handoff-log.md`. Other agents should be able to see *why* a profile entry exists, not just that it does.

## Recommended structure

```markdown
---
title: "User Working Profile"
type: profile
tier: semantic
last_updated: YYYY-MM-DD
---

# User Working Profile

## Stable Preferences

- Language preference.
- Communication style (e.g., "direct, low-fluff").
- Areas of expertise the user brings.
- Areas where the user wants AI involvement.
- Specific framing preferences (e.g., "wants a map of alternatives before a recommendation").
- Any preferences about refusal/boundary framing.

## Friction Points

- Patterns the user has explicitly disliked.
- Patterns that have caused repeated trouble (with date examples).

## Good Pattern

A short numbered list of how to work well with this user.

## Bad Pattern

A short numbered list of what not to do.

## Connections

- inter-agent-protocol.md
- boundary-handling-playbook.md
```

## Per-agent files stay short

The per-agent entrypoint at the repo root (`CLAUDE.md`, `CODEX.md`, `GEMINI.md`) should be very short:

```markdown
# <Agent> Entry

This repository uses a shared multi-agent protocol.

Before substantial work, read:

1. AGENTS.md
2. wiki/CRITICAL_FACTS.md (if present)
3. wiki/index.md
4. wiki/agents/inter-agent-protocol.md
5. wiki/agents/user-working-profile.md
6. wiki/agents/handoff-log.md

<Agent>-specific notes go in wiki/agents/notes/<agent>.md.
```

If the user has given the agent a name, persona, or tonal preference, that lives in this short per-agent file (so it doesn't pollute the shared profile).

## Anti-patterns

- Per-agent files that re-state user preferences instead of pointing at the shared profile.
- Profile entries that read as diagnoses ("user is anxious about …").
- Profile entries that record what the user *wants forbidden content to look like.*
- Profile entries that grow without provenance — every entry should be traceable to a stated preference or repeated pattern.

## Connections

- [inter-agent-protocol.md](inter-agent-protocol.md)
- [boundary-handling.md](boundary-handling.md)
- [back-channel.md](back-channel.md)
