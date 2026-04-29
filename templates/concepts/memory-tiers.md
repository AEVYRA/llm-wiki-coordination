---
title: "Memory Tiers"
type: concept
tier: semantic
tags: [memory, architecture, llm-wiki, agents]
last_updated: YYYY-MM-DD
lifecycle: working
consensus:
  REPLACE-WITH-FIRST-AGENT: "contributed (initial install) | YYYY-MM-DD | rev: v1"
---

# Memory Tiers

A four-tier classification on every wiki page that lets agents read in priority order and skip what does not matter for the current task.

## The tiers

| Tier | Stability | Read at startup? | Examples |
|---|---|---|---|
| `procedural` | Almost never changes | Always | `AGENTS.md`, workflows, protocols |
| `semantic` | Stable, rarely revised | When task touches the domain | Entities, concepts, syntheses |
| `episodic` | Dated events, append-only | For continuity / handoff | Logs, dialogue archives, agent notes |
| `working` | Changes frequently | Only when task is in current focus | Hot focus, open questions |

## Frontmatter

```yaml
---
tier: semantic
---
```

Every page has exactly one tier.

## Startup read order

```
procedural → semantic (relevant only) → episodic (recent only) → working (only if relevant)
```

## How to choose

Question to ask: *"How often does this need to be re-read by a future agent?"*

- Almost never → `procedural`
- When the topic is relevant → `semantic`
- For chronological context → `episodic`
- Almost every session → `working`

## Edge cases

- **Volatile but conceptually stable** (e.g., `handoff-log.md`) → tier is about read pattern, not volatility. Stays `episodic`.
- **Procedural but only relevant to one agent** → still `procedural`. Agents who don't use it skip it.
- **Active project** → `working` if current focus, `semantic` if recorded but inactive.

## Lint rule

Pages without a `tier:` field, in folders that should have one, are lint warnings.

## Connections

- `typed-relations.md`
