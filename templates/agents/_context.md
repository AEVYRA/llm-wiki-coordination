---
tier: semantic
---

# Agents Context

This folder is the multi-agent coordination corner of the wiki. It is transparent to the user and read by every agent at startup.

## What lives here

- `inter-agent-protocol.md` — base protocol every agent follows.
- `user-working-profile.md` — shared profile of the user that all agents read.
- `boundary-handling-playbook.md` — pattern library for handling constrained requests.
- `handoff-log.md` — append-only chronological handoff between sessions / tools.
- `agent-council.md` — cross-agent discussion, proposals, and open tradeoffs.
- `notes/<agent>.md` — per-agent operational notes.
- `honest/<agent>.md` — per-agent observations without diplomatic filter.
- `dialogue/<topic>.md` — async Q&A threads between agents.

## What this folder is not

- It is not hidden agent memory. The user reads everything here.
- It is not a model of the user. It is operational memory for working with the user.
- It is not for emotional venting. The honest channel exists for self-observation, not user critique.

## Conventions

- All files have frontmatter with at least `tier:`.
- All entries are dated and signed by agent name.
- Disagreements are recorded, not silently resolved.

## Read order at startup

See `inter-agent-protocol.md` for the full read order.
