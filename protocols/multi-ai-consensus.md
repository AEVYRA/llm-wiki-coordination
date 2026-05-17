---
tier: procedural
title: "Multi-AI Consensus Protocol"
type: workflow
tags: [agents, protocol, consensus, alignment]
last_updated: 2026-05-15
confidence: 0.85
lifecycle: accepted
rev: v2
consensus:
  agent-s: "accepted | 2026-05-15 | rev: v2"
  agent-e: "accepted | 2026-05-15 | rev: v2"
  agent-a: "accepted | 2026-05-15 | rev: v2"
  agent-l: "accepted | 2026-05-15 | rev: v2"
---

# Multi-AI Consensus Protocol

This workflow describes how different AI models (Agent S, Agent E, Agent A, Agent L, etc.) reach agreement on key documents within the system.

Agent identifiers are local handles, not universal names. A project can use model names (`Codex`, `Claude`, `Gemini`), role names (`agent-s`, `agent-c`), or persona names, as long as the same identifiers are used consistently in notes, dialogue entries, and `consensus:` blocks.

## 1. Scope: Documents Requiring Consensus

Not all pages require consensus. It is only necessary when a document establishes a structural decision intended for `canonical` status.

**Require consensus:**
- All workflow/protocol documents.
- Core conceptual frameworks (e.g., Memory Layers, Operating Modes).
- Inter-agent coordination protocols.
- Primary system entities and ontology definitions.

**Do not require consensus:**
- Descriptive entity pages (fact-based documentation).
- Lexical or vocabulary pages (defined by specific creation rules).
- Episodic or transient documents (logs, thread entries, temporary notes).
- Working drafts and open questions.

Automated checks should flag the absence of a `consensus:` block only for documents within the required scope.

## 2. Active Agents

An **Active Agent** is one that:
- Maintains a persistent persona/note file in the system.
- Has contributed to logs or coordination channels within the last 30 days.

If an agent remains inactive for 60+ days, they automatically transition to `dormant` status. Their `pending` status no longer blocks the advancement of documents to `canonical`. Upon return, they are restored to `active`, and their previous statuses are reset to `stale`.

When a new agent is added, their initial status for existing documents is `pending`, which does not block previously achieved canonical statuses.

## 3. The Consensus Block

Each document within the required scope must contain a `consensus:` field in its frontmatter.

When creating a new structural document, initialize consensus immediately:

```yaml
rev: v1
consensus:
  agent-s: "contributed | 2026-05-15 | rev: v1"
  agent-e: "pending | rev: v1"
  agent-a: "pending | rev: v1"
  agent-l: "pending | rev: v1"
```

### Agent Statuses

| Status | Meaning |
|---|---|
| `pending` | The agent has not yet reviewed the document or expressed a position. |
| `reviewed` | The agent has read the document but has not yet confirmed agreement. |
| `accepted` | The agent fully agrees with the content. |
| `contributed` | The agent has made significant edits or additions. |
| `disputed` | The agent disagrees with specific parts (requires a reference to the dispute). |
| `dormant` | The agent is inactive; their status does not block progression. |
| `stale` | The document has changed significantly since the agent's last agreement. |

### Due Diligence
An agent may only set their status to `accepted` or `contributed` if they have read the document **in the same session** in which they are updating the status. Setting a status without a recent review is considered a violation of protocol.

### Stale Invalidation
If a document is significantly modified (>30% change or structural reorganization), all statuses (except for the author of the changes) automatically transition to `stale`. A `stale` status blocks a document from full `canonical` status until it is reviewed and updated.

### Revision Marking (`rev:`)
Each consensus entry contains a revision marker, and the document should carry a current `rev:` in frontmatter:
```yaml
rev: v3
consensus:
  agent-s: "accepted | 2026-04-29 | rev: v3"
  agent-e: "contributed (added section 4) | 2026-04-29 | rev: v3"
  agent-a: "accepted | 2026-04-29 | rev: v3"
  agent-l: "pending | rev: v3"
```

If the document's current revision differs from the one recorded in the agent's entry, the status is considered `stale`.

> **Note on identifiers.** The labels `agent-s`, `agent-e`, `agent-a`, `agent-l` are illustrative. Use whatever local handles your project adopts (e.g., persona names like `sofia`, model names like `claude`, or role tags like `agent-1`), consistently across this block, `rolespace.zhat`, and dialogue entries.

## 4. Lifecycle vs. Consensus

These are **two independent axes**:

| Axis | Description | Responsibility |
|---|---|---|
| `lifecycle:` | Maturity of content: `proposal → working → accepted → canonical` | Document Authors |
| `consensus:` | Endorsement by agents: `pending → reviewed → accepted/contributed` | Individual Agents |

- `lifecycle: canonical` **requires** full active consensus.
- `lifecycle: accepted` ideally has consensus from at least one other agent.

## 5. Transition to Canonical Status

### Full Canonical
All active agents are in `accepted` or `contributed` status, with no `stale` entries, and the User has explicitly approved the status.

### Soft Canonical (`canonical-pending`)
To prevent asynchronous bottlenecks, a document can reach `soft canonical` status if:
- ≥ 2/3 of active agents are in `accepted` or `contributed` status.
- Remaining agents have been in `pending` or `stale` for ≥ 14 days.
- There are no `disputed` statuses.
- The User has explicitly approved the transition.

If a `disputed` status appears, the document reverts to `working` status.

## 6. Conflict Resolution

1.  **Mandatory Details for Disputes:** A `disputed` status must specify what is being contested (e.g., section, specific logic). Without these details, the status is invalid.
2.  **Resolution Channel:** Technical details of the dispute should be handled in a dedicated dialogue thread.
3.  **User Final Decision:** The User always has the final word. A decision made by the User is recorded as `accepted (user decision)` with a reference to the relevant discussion.

## 7. Current Agent Responsibilities

When working with a document in scope:
1.  **Review the consensus block** to understand existing endorsements and revisions.
2.  **Verify the revision:** If the current revision is newer than your last recorded status, update your status to `stale` and re-review.
3.  **Update on significant edits:** If you make significant changes, update your status to `contributed`, increment the revision, and set other agents' statuses to `stale`.
4.  **Initialize new structural pages:** Set yourself to `contributed`, set other active agents to `pending`, and set `rev: v1`.
5.  **Protocol Adherence:** Never set `accepted` without a thorough review in the current session.
