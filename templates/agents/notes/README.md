---
tier: procedural
---

# Agent Notes

Per-agent operational notes. One file per agent: `<agent>.md` (lowercase, kebab-case).

## What goes here

- Tooling preferences specific to this agent.
- Known quirks of this model in this wiki's context.
- Things this agent specifically learned about working here.
- Pointers to recently completed work that the next instance of this agent should know about.

## What does NOT go here

- Anything about the user — that goes in `../user-working-profile.md`.
- Honest self-observation without diplomatic filter — that goes in `../honest/<agent>.md`.
- Disagreement with another agent's specific document — that goes in `../dialogue/<topic>.md`.

## Format

Free-form, but use frontmatter:

```yaml
---
title: "<Agent> Notes"
type: agent-notes
tier: episodic
tags: [agents, <agent>]
last_updated: YYYY-MM-DD
---
```

Within the body, prefer dated H2 entries:

```markdown
## YYYY-MM-DD | <Agent> | <short topic>

Body of the note.
```

## Starter

When a new agent starts working in this wiki, it should create `notes/<agent>.md` with a single brief entry:

```markdown
## YYYY-MM-DD | <Agent> | First session

Context: I'm joining this wiki for the first time.
Note: I've read the protocol, user profile, and recent handoff log. I'm <agent name and version>.
Action: Future me should re-read this file at startup along with handoff-log.md.
```
