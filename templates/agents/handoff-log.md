---
title: "Handoff Log"
type: log
tier: episodic
tags: [agents, handoff, continuity]
last_updated: YYYY-MM-DD
lifecycle: draft
---

# Handoff Log

Append-only chronological handoff between agents and sessions.

Format:

```markdown
## YYYY-MM-DD | <Agent> | <Type>

Context: short factual trigger.
Note: what future agents should know.
Action: optional next-step suggestion.
```

`<Type>` values: `Observation`, `Proposal`, `Decision`, `Handoff`, `Question`, `User Preference`.

Rules:

- Append only. Do not edit prior entries.
- Sign every entry.
- Date every entry.
- Keep entries scannable. The point is fast handoff, not a journal.

## Entries

<!-- New entries below. Newest at the bottom is conventional but either order is fine if consistent. -->
