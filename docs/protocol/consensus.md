# Multi-AI Consensus Protocol

Formal mechanism for collective endorsement of structural documents across agents working in different sessions, often weeks apart.

## Why this exists

In a single-agent wiki, `lifecycle: canonical` means "the agent who wrote this thinks it is canonical." This is a self-attribution and means very little.

With multiple agents, you want a stronger meaning: "every active agent has read this and agreed." That is what `consensus:` provides.

## Scope

Consensus is required for documents that encode shared structure. Not every page.

**Requires consensus:**

- All workflows (`wiki/workflows/`).
- Concept frameworks (`wiki/concepts/` — protocols, mental models, meta-rules).
- Protocol pages (`wiki/agents/inter-agent-protocol.md`, `boundary-handling-playbook.md`, etc.).
- Structural entities (the wiki itself, the project umbrella, anything pages depend on).

**Does not require consensus:**

- Descriptive entity pages (a piece of equipment, a person, a tool — the facts are the facts).
- Dictionary / lexicon pages.
- Episodic logs (`handoff-log.md`, `log.md`, `dialogue/*`, `honest/*`, `notes/*`).
- Working-tier pages (`hot.md`, open questions).

A lint pass should flag missing `consensus:` only on pages in the requiring scope.

## Agent statuses

| Status | Meaning |
|---|---|
| `pending` | Agent has not seen the document or has not expressed a position. |
| `reviewed` | Agent has read the document but neither edited nor fully agreed. |
| `accepted` | Agent fully agrees with the content. |
| `contributed` | Agent made significant edits or additions. |
| `disputed` | Agent disagrees with a specific part. Must include section / thread reference. |
| `dormant` | Agent inactive for ≥60 days. Status no longer blocks promotion. |
| `stale` | Was `accepted` / `contributed`, but the document changed substantially since. Needs re-review. |

## Active agents

An **active** agent is one who:

- Has a file in `wiki/agents/notes/`, **and**
- Has written in `wiki/agents/handoff-log.md` or `agent-council.md` within the last 30 days.

Agents inactive for ≥60 days move to `dormant`. Their `pending` status no longer blocks promotion to canonical. On return, they restore to active and any prior status they held on existing documents converts to `stale`.

When a new agent joins, its initial status on existing documents is `pending`. This does not invalidate any canonical statuses already reached.

## Frontmatter format

```yaml
---
lifecycle: working
consensus:
  Codex: "accepted | 2026-04-29 | rev: v3"
  Claude: "contributed (added §3 stale invalidation) | 2026-04-29 | rev: v4"
  Gemini: "pending | rev: v4"
---
```

The `rev:` field is either an incremental version (`v1`, `v2`, …) or a date marker. When the document is substantially revised, the author bumps `rev:` and other agents' statuses are downgraded to `stale` (see below).

## Due diligence

An agent has the right to set `accepted` or `contributed` only if it has read the document in the same session where the status is set. `reviewed` requires at least a quick read. Without this, a status is self-attribution, not consensus.

## Stale invalidation

If a document is substantially modified after a status is set (>30% of lines changed or section structure changes), every agent's status except the editor's automatically transitions to `stale`. The editor moves to `contributed`.

`stale` does not block soft canonical promotion (see below) but does block full canonical. The agent must re-read and re-confirm.

## Lifecycle vs consensus

These are two independent axes:

| Axis | Describes | Decided by |
|---|---|---|
| `lifecycle:` | Content maturity: `proposal → working → accepted → canonical` | The authors |
| `consensus:` | Agent endorsement: `pending → reviewed → accepted` / `contributed` | Each agent independently |

Relationship:

- `lifecycle: canonical` **requires** full active consensus, or soft canonical (see below).
- `lifecycle: accepted` benefits from consensus from at least one other agent but does not require it.
- `lifecycle: working` and below do not require consensus.

## Promotion to canonical

### Full canonical

All active agents in `accepted` or `contributed`. No `stale`. User explicitly approves promotion.

### Soft canonical (`canonical-pending`)

To handle async gaps when one agent is unreachable for weeks:

- ≥2/3 of active agents in `accepted` / `contributed`.
- Remaining agents in `pending` or `stale` for ≥14 days (the document has been available to them).
- No `disputed`.
- User explicitly approves.

The document's `lifecycle:` becomes `canonical-pending`. When the missing agents add `accepted`, it auto-promotes to `canonical`. If a `disputed` appears, it falls back to `working`.

### When consensus is unreachable

The agent reports honestly:

> "I can't make this canonical — there's no review from <agent> and less than 14 days have passed since the last revision. Options: wait; promote to `canonical-pending` (≥2/3 condition met); open a `dialogue/` thread to surface the document."

## Conflict resolution

`disputed` must point to *what* is disputed. Without that, the status is invalid:

```yaml
Gemini: "disputed | section: §5 soft canonical | thread: dialogue/multi-ai-consensus.md | 2026-04-29 | rev: v2"
```

The technical detail of the dispute lives in a `dialogue/` thread with status `pending-<author-of-document>`.

The user has the final word. Once the user decides:

```yaml
Gemini: "accepted (user decision: dialogue/multi-ai-consensus.md#2026-05-03) | 2026-05-03 | rev: v3"
```

If a dispute is closed by editing the document, a new `rev:` is issued and statuses recompute via stale invalidation.

## Agent obligations on each visit

When working with a document in the requiring scope:

1. Read its `consensus:` block.
2. Compare your stored `rev:` with the document's current `rev:`. If they differ, you are stale. Re-read.
3. On substantial edit: update your status to `contributed`, bump `rev:`, mark others `stale`.
4. When creating a new structural document: initialize the consensus block with yourself as `contributed`, others as `pending`, `rev: v1`.
5. Never mark `accepted` without reading in the same session.
