---
title: "Multi-AI Consensus Protocol"
type: workflow
tier: procedural
tags: [agents, protocol, consensus, alignment]
last_updated: YYYY-MM-DD
lifecycle: working
consensus:
  REPLACE-WITH-FIRST-AGENT: "contributed (initial install) | YYYY-MM-DD | rev: v1"
---

# Multi-AI Consensus Protocol

How different AI agents reach formal agreement on key documents.

## 1. Scope: which documents require consensus

Not every page. Consensus is required only for documents encoding shared structure that may reach `lifecycle: canonical`.

**Requires consensus:**

- All workflows (`wiki/workflows/`).
- Concept frameworks (protocols, mental models, meta-rules).
- Protocol pages in `wiki/agents/`.
- Structural entities (the wiki itself, project umbrella, anything pages depend on).

**Does not require consensus:**

- Descriptive entity pages (equipment, people, tools — facts are facts).
- Dictionary / lexicon pages.
- Episodic logs (`handoff-log.md`, `log.md`, `dialogue/*`, `honest/*`, `notes/*`).
- Working-tier pages (`hot.md`, open questions).

Lint should flag missing `consensus:` only on documents in the requiring scope.

## 2. Active agents

**Active** = has a file in `wiki/agents/notes/` AND has written in `handoff-log.md` or `agent-council.md` within the last 30 days.

Inactive 60+ days → `dormant`. Pending status no longer blocks promotion. On return, prior statuses convert to `stale`.

New agents start with `pending` on existing documents. Their `pending` does not invalidate already-canonical documents.

## 3. Consensus block

```yaml
consensus:
  <Agent1>: "accepted | YYYY-MM-DD | rev: v3"
  <Agent2>: "contributed (added §3) | YYYY-MM-DD | rev: v4"
  <Agent3>: "pending | rev: v4"
```

### Statuses

| Status | Meaning |
|---|---|
| `pending` | Has not seen or expressed a position. |
| `reviewed` | Read but did not edit or fully agree. |
| `accepted` | Fully agrees. |
| `contributed` | Made significant edits or additions. |
| `disputed` | Disagrees with a specific part (must reference section / thread). |
| `dormant` | Inactive ≥60 days. Does not block. |
| `stale` | Was `accepted` / `contributed`, document changed substantially since. |

### Due diligence

`accepted` or `contributed` requires reading in the same session. `reviewed` requires at least a quick read.

### Stale invalidation

Substantial edits (>30% lines changed or section structure changed) auto-reset all non-editor statuses to `stale`. Editor moves to `contributed`.

`stale` blocks full canonical, not soft canonical.

### `rev:` field

Every status carries a revision marker (incremental `v1`, `v2`, … or a date). Author bumps `rev:` on substantial edits.

## 4. Lifecycle vs consensus

| Axis | Describes | Decided by |
|---|---|---|
| `lifecycle:` | Content maturity: `proposal → working → accepted → canonical` | Authors |
| `consensus:` | Agent endorsement: `pending → reviewed → accepted/contributed` | Each agent |

`canonical` requires full consensus or soft canonical. Lower lifecycles do not require consensus.

## 5. Promotion to canonical

### Full canonical

All active agents in `accepted` / `contributed`. No `stale`. User explicitly approves.

### Soft canonical (`canonical-pending`)

For async gaps:

- ≥2/3 active agents in `accepted` / `contributed`.
- Remaining in `pending` or `stale` for ≥14 days.
- No `disputed`.
- User explicitly approves.

`lifecycle: canonical-pending`. Auto-promotes to `canonical` when missing accepts arrive. Falls back to `working` on `disputed`.

### When unreachable

The agent reports honestly:

> "I can't make this canonical — there's no review from <agent> and less than 14 days have passed. Options: wait; promote to `canonical-pending` (≥2/3 condition met); open a `dialogue/` thread."

## 6. Conflict resolution

`disputed` must reference what is disputed:

```yaml
<Agent>: "disputed | section: §5 | thread: dialogue/multi-ai-consensus.md | YYYY-MM-DD | rev: v2"
```

The dispute detail lives in a `dialogue/` thread with status `pending-<author-of-document>`.

User has the final word. After user decides:

```yaml
<Agent>: "accepted (user decision: dialogue/...) | YYYY-MM-DD | rev: v3"
```

## 7. Agent obligations

When working with a document in scope:

1. Read its `consensus:` block.
2. Compare your stored `rev:` with the document's current `rev:`. If different, you are stale. Re-read.
3. On substantial edit: update your status to `contributed`, bump `rev:`, mark others `stale`.
4. When creating a new structural document: initialize the consensus block with yourself as `contributed`, others as `pending`, `rev: v1`.
5. Never mark `accepted` without reading in the same session.

## Connections

- `../agents/inter-agent-protocol.md`
- `../agents/handoff-log.md`
- `../concepts/memory-tiers.md`
