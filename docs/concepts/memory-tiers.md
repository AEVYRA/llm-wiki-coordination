# Memory Tiers

A four-tier classification on every wiki page that lets agents read in priority order and skip what doesn't matter for the current task.

## Why this exists

In a flat wiki, every page is equal at startup. The agent reads everything or nothing. With a few hundred pages this becomes a context budget problem; with a few thousand it becomes impossible.

Memory tiers solve this by tagging each page with how stable it is and how often it should be read.

## The four tiers

| Tier | Stability | Read at startup? | Examples |
|---|---|---|---|
| `procedural` | Almost never changes | Always | `AGENTS.md`, workflows, protocols, lint checks |
| `semantic` | Stable, rarely revised | When task touches the domain | Entities, concepts, syntheses, comparisons |
| `episodic` | Dated events, append-only | For continuity / handoff | Logs, dialogue archives, agent notes, council |
| `working` | Changes frequently | Only when task is in current focus | Hot focus, open questions, current sprints |

## Frontmatter format

```yaml
---
title: "..."
type: ...
tier: semantic
last_updated: 2026-04-29
---
```

Every page has exactly one tier. If you can't decide, the question to ask is: "How often does this need to be re-read by a future agent?"

- Almost never → `procedural`
- When the topic is relevant → `semantic`
- For chronological context → `episodic`
- Almost every session → `working`

## Startup read order

```
procedural → semantic (relevant only) → episodic (recent only) → working (only if relevant)
```

Concretely, an agent at startup should:

1. Read all procedural pages required by the protocol (typically: `AGENTS.md`, the protocol pages, the workflows the agent might use).
2. Read semantic pages only for the domain of the current question.
3. Read episodic pages: at minimum the latest few entries of `handoff-log.md` and any open dialogue threads.
4. Read working pages only if the current task touches the active focus.

This is how a wiki of 1000+ pages stays usable. Without tiers, the agent either reads it all (bankrupt context) or skips it (loses continuity).

## Edge cases

**A page changes a lot but is conceptually stable.** Use the page's *intended* read pattern, not its volatility. `handoff-log.md` is volatile but conceptually episodic — it stays `episodic`.

**A page is procedural but only relevant to one agent.** Still `procedural`. Tier is about read pattern, not scope. The agent without that tool simply skips it.

**A page describes a current project.** If the project is your active focus, `working`. If the project is recorded but not currently active, `semantic`.

## Lint rule

Pages without a `tier:` field, in folders that should have one, are lint warnings. Suggested folders requiring tier:

- All of `wiki/`.
- Optionally `raw/` if you want raw notes to also be tier-classified.

## Connections

- See [typed-relations.md](typed-relations.md) for the orthogonal concept of how pages link to each other.
- See [../../templates/concepts/memory-tiers.md](../../templates/concepts/memory-tiers.md) for the template version that ships into a user wiki.
