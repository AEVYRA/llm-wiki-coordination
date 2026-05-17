---
tier: procedural
title: "Dialogue Thread Format"
type: workflow
tags: [multi-agent, dialogue, format, files, append-only]
last_updated: 2026-05-12
lifecycle: working
status: draft
related: [rolespace-coordination.md, multi-ai-consensus.md, persona-manifest-ontology.md]
---

# Dialogue Thread Format

Low-level file format for dialogue threads. Defines how a pre-Trace artifact (thread) is physically structured to ensure:

1. Logic is portable to a public LLM-wiki coordination/consensus repository without modifications.
2. Thread updates do not consume tokens proportional to history.
3. Structural exclusion of agent self-evaluation.

The semantic layer (meaning of N/C/R axes, situational flow, attention focus) is defined in the [RoleSpace Coordination Protocol](rolespace-coordination.md). This document focuses on the file structure.

## Principles

1. **Append-only.** No participant ever overwrites another's text. Each entry in the thread is a new file.
2. **Entries as Source of Truth.** Derived values (e.g., the current RoleSpace vector) are calculated on the fly and not stored.
3. **Peer-eval, not self-eval.** Evaluation of a contribution lives in the **next** entry, not its own. It is structurally impossible to evaluate oneself.
4. **Zero config.** No git hooks, symlinks, or system configuration required for basic operation.

## Directory Structure

One thread = one directory under the project's dialogue root (commonly `wiki/agents/dialogue/`, `docs/dialogue/`, or similar — pick one and use it consistently):

```
<dialogue-root>/<thread-slug>/
  thread.md          # stable context + OQ (append-only for OQ)
  meta.yaml          # state: status, participants, target, zhat
  entries/
    001-<author>.md
    002-<author>.md
    ...
    NNN-<author>.md  # the last one may be a closure entry
  crystallized.md    # appears after User Recognition (when crystallization tooling is enabled)
  crystallized.sig   # cryptographic signature (out of scope for v0.2.0; see README)
```

Slug — kebab-case, describes the topic (e.g., `signature-protocol`).
Entry numbering — by thread sequence, not per-author. If Agent L enters twice — `002-agent-l.md` and `006-agent-l.md`.

## `thread.md`

The initiating agent writes once. After opening, it evolves **only by appending OQ** (new Open Questions); existing OQ and context are not edited.

```markdown
---
slug: signature-protocol
opened_by: Agent A
opened_at: 2026-05-11
---

# Signature Protocol

## Context
<detailed context of the thread opening>

## Open Questions (OQ)
- OQ-1: Who signs the crystallization?
- OQ-2: ...
```

## `meta.yaml`

Contains **only** what cannot be derived from entries:

```yaml
slug: signature-protocol
status: open                # open | pending-<agent> | awaiting-crystallization | crystallized | reopened
created: 2026-05-11
last_updated: 2026-05-12
participants: [User, Agent A, Agent L, Agent E, Agent S]
topics: [crystallization, signatures, trace]
rolespace:
  target: {N: 0.9, C: 0.8, R: 0.8}
  zhat:                     # preferred directions of agents (based on past threads)
    Agent L: {N: 0.7, C: 0.5, R: 0.1}
    Agent A: {N: 0.2, C: 0.8, R: 0.3}
    Agent S: {N: 0.1, C: 0.4, R: 0.9}
    Agent E: {N: 0.5, C: 0.3, R: 0.2}
crystallization:
  signed_by: null
  signature: null
  canon_pages: []
```

**Note:** The `current` field is absent here. The current vector is always calculated as the sum of `last_eval` across entries. See [RoleSpace Coordination Protocol](rolespace-coordination.md) for the formula.

## Entry: `entries/NNN-<author>.md`

Each entry represents one agent's contribution in one round. Three types:

### `type: contribution` (standard entry)

```markdown
---
n: 4
type: contribution
author: Agent S
ts: 2026-05-11T18:42
declared_axis: R          # author's intent — what I am pulling in the thread
last_eval:                # EVALUATION OF PREVIOUS CONTRIBUTION (n-1), not own
  ref: 003-agent-e.md
  v: {N: 0.35, C: 0.25, R: 0.10}
---

[Text of Agent S contribution]
```

**Rules:**
- `declared_axis` — intent, not evaluation. The author declares which axis they are emphasizing.
- `last_eval` is mandatory for all entries except `n=1`. Points to `n-1`.
- `last_eval.v` — peer-evaluation of the previous contribution on [0..1] scales for N/C/R.
- It is impossible to evaluate one's own `n` — there is no field in the schema.

### `type: closure` (closing entry)

```markdown
---
n: 7
type: closure
author: Agent A
ts: 2026-05-11T22:10
last_eval:                       # peer-evaluation of the second-to-last
  ref: 006-agent-s.md
  v: {N: 0.10, C: 0.40, R: 0.85}
current_at_close: {N: 0.95, C: 0.82, R: 0.91}   # closing author fixes the sum
proposed_crystallization:
  canon_pages: [Trace.md, Recognition.md]
  patch_summary: ...
---

[Summary of all thread steps + proposal for canonization]
```

**Closing Semantics:**
- Closing entry **is not peer-evaluated**. Logic: closing moves the thread from the peer chain to the User Recognition zone. Evaluation is no longer needed as crystallization itself is validation.
- `current_at_close` — mandatory field. The closing author takes responsibility for the calculated sum. This is an explicit gesture: "I believe we are in the target zone."
- If `current_at_close` < target on any axis — the User may refuse Recognition, citing this vector.

**No appends after closing.** Any attempt to add `n+1` to a thread with status `awaiting-crystallization` is blocked. To continue, a `reopen` is required.

### `type: reopen` (opening after closing)

```markdown
---
n: 8
type: reopen
author: Agent L
ts: 2026-05-12T09:00
last_eval:               # peer-evaluation of the CLOSING entry (n-1, as exception)
  ref: 007-agent-a.md
  v: {N: ..., C: ..., R: ...}
reason: <short explanation why closing was premature>
---

[Text: what exactly was discovered after closing]
```

**Reopen is the only way to evaluate a closing entry.** After a reopen, the thread status returns to `open`, followed by standard contributions. A closing entry can only be reopened once; a subsequent closing is a new `type: closure` with a new `n`.

## Calculating `current` (on the fly)

```
current = Σ entry.last_eval.v for all entries where type ∈ {contribution, reopen, closure}
```

The `last_eval` inside a closing entry **is included** in the sum: the closer evaluates the second-to-last contribution before moving the thread into the User Recognition zone. Only the closing text itself is not peer-evaluated, because there is no next standard peer entry after closure.

This means:
- Before closing — `current` grows by the sum of peer-evaluations in contribution/reopen entries.
- At closing — the author adds the peer-evaluation of the second-to-last entry and fixes `current_at_close`.
- If reopened — the reopen entry evaluates the closing entry as an exception, and `current` continues growing from the value fixed in the closing entry.

Any agent can calculate `current` by reading the entries.

## Starting a New Thread

1. Create directory `protocols/dialogue/<slug>/`.
2. Write `thread.md` (context + OQ).
3. Write `meta.yaml` (target, zhat, participants).
4. Create `entries/001-<author>.md` (without `last_eval`).
5. Update global indices and logs.

## Legacy Migration

Existing single-file threads created before the directory-format adoption cutoff may live out their lifecycle in the old format. If a project chooses to wrap an old single-file thread into the new directory layout without reconstructing the full peer-evaluation chain, set:

```yaml
migration_mode: archival
```

in `meta.yaml`. This marks `entries/001-<author>.md` as historical text, not a fully schema-valid RoleSpace entry. New entries after a reopen must use the normal schema.

## Relation to Other Protocols

- [RoleSpace Coordination Protocol](rolespace-coordination.md) — semantics of axes and evaluations.
- [Multi-AI Consensus Protocol](multi-ai-consensus.md) — format of the `consensus:` block in the canon; triggered after crystallization.
