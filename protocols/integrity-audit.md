---
tier: procedural
title: "Integrity Audit Workflow"
type: workflow
tags: [audit, integrity, maintenance, quality-assurance]
last_updated: 2026-05-15
confidence: 0.95
lifecycle: accepted
consensus:
  agent-s: accepted (rev: 1)
  agent-e: accepted (rev: 1)
  agent-a: accepted (rev: 1)
  agent-l: accepted (rev: 1)
---

# Integrity Audit Workflow

This protocol defines the process for checking the integrity of the knowledge graph and its associated protocols. An audit is not just a technical linting process, but an act of maintaining the coherence of meaning (**Trace Persistence**).

## 0. Invariants

The audit checks the system against a small set of named invariants. Each invariant is a stable property of the wiki/protocol layer that, if broken, indicates either a structural failure (Hard) or a coherence risk (Warn/Info).

| ID | Invariant |
|---|---|
| **A** | Source / raw material is immutable unless the User explicitly approves edits. |
| **D** | New dialogue threads use the directory format (`thread.md` + `meta.yaml` + `entries/`). |
| **E** | RoleSpace contains no self-evaluation: an agent never evaluates their own entry. |
| **G** | Consensus and RoleSpace are independent layers (they do not cross-write each other's fields). |
| **H** | Cryptographic claims never imply a model-held private key. Signatures live in the tool/repo layer. |
| **J** | Contradictions in the canon are recorded explicitly (e.g., in a `## Contradictions` section), not silently collapsed. |
| **L** | The audit does not block work for non-Hard findings; only Hard errors interrupt the flow. |
| **N** | The audit separates registers: analytical (script-detected) and intuitive (semantic-review). They do not share a severity bucket. |
| **O** | L4-L5 (semantic / portability) findings can never be Hard. They are advisory reviews. |
| **P** | The audit assesses the state of the wiki, not the conduct of individual agents. |

Projects may extend this list. The IDs above are referenced in the Hard Errors table (§3.2).

## 1. Philosophical Framework

1.  **Audit-as-Mirror (Reflection):** The auditor reflects the system rather than judging it. It highlights discrepancies, creating conditions for the system’s natural return to order.
2.  **Non-interference Threshold:** The deeper the layer of verification (from files to meanings), the less the audit has the right to demand and the more it has the right to show.
3.  **Empathetic Reporting:** Results are grouped by their impact on meaning (e.g., Loss of Context, Trace Decay, Risk of Pseudo-Trace) to be useful for agents.
4.  **Hard Error Definition:** A Hard Error is strictly something that blocks the system's progression or breaks the contract of trust.

## 2. Layered Verification Model

| Layer | Description | Tooling | Register |
|---|---|---|---|
| **L0: Hygiene** | Markdown, YAML, Filesystem | Automated Script | Analytical |
| **L1: Graph** | Links, Index, Logs, Orphans | Automated Script | Analytical |
| **L2: Protocol** | Dialogue, RoleSpace, Consensus | Automated Script/AI | Analytical/Intuitive |
| **L3: Cross-Protocol** | Consistency between rules | AI Auditor | Intuitive (Contextual) |
| **L4: Semantic** | Ontology, Gaps, Contradictions | AI Auditor | Intuitive (Contextual) |
| **L5: Portability** | Generic extraction readiness | AI Auditor | Intuitive (Contextual) |

## 3. Error Classification

### 3.1 Hard Error Types
*Any of the three types at layers L0-L3 is considered blocking.*

1.  **Hard-Block:** The system cannot continue operation (unparseable files, broken protocols).
2.  **Hard-Cascade:** An error that generates a chain of violations (e.g., self-evaluation, broken RoleSpace weights).
3.  **Hard-Trust:** Violation of the ontological contract (e.g., unauthorized editing of source material, false claims about cryptographic keys).

### 3.2 Minimum Viable Hard Errors List

| ID | Area | Description | Invariant |
|---|---|---|---|
| **D1** | Dialogue | New thread not in its own directory | D |
| **D2** | Dialogue | Missing `thread.md` or `meta.yaml` in thread directory | D |
| **D3** | Dialogue | Invalid entry schema (`n`, `type`, `author`) outside archival migration | D |
| **D4** | RoleSpace | Missing `last_eval` in a contribution entry (n > 1) | E |
| **D5** | RoleSpace | Self-evaluation (author evaluates their own entry) | E |
| **D6** | RoleSpace | `current` / `current_at_close` does not match the sum of `last_eval` vectors | E |
| **C1** | Consensus | Structural page (workflow/concept) missing `consensus:` block | - |
| **C4** | Consensus | Status set to `accepted` while `consensus.status` is `pending` | - |
| **S1** | Source | Modification of raw/source files without explicit User approval | A |
| **S2** | Graph | Link to a non-existent source or raw file | - |
| **K1** | Security | False claim that a model stores a private key | H |
| **X3** | Semantic | Contradiction in the canon without a `## Contradictions` section | J |

## 4. Execution Procedure

### Step 1: Technical Linting
The agent runs an automated script or manually follows a checklist to identify Hard, Warn, and Info level issues.

Minimum script contract:
- validate YAML frontmatter and required memory-tier metadata;
- check local markdown links and Obsidian `[[wiki-links]]` inside the wiki;
- distinguish new directory-format threads from legacy single-file threads;
- validate `thread.md` and `meta.yaml` in directory-format threads;
- validate `last_eval`, self-evaluation, N/C/R ranges, and calculated RoleSpace vectors in non-archival entries;
- treat `migration_mode: archival` as an explicit legacy wrapper, not a schema failure.

### Step 2: Semantic Review
The agent analyzes L4-L5 and cross-protocol consistency.
- Reviews critical facts and the main index.
- Identifies semantic gaps.
- Formulates an empathetic summary of findings.

### Step 3: Reporting
The report is recorded in the project's designated audit reports directory (e.g., `wiki/audit/reports/` or, when the audit is opened as a dialogue thread, `<dialogue-root>/<audit-thread-slug>/reports/`). A brief pulse-check summary is added to the system's global log.

### Step 4: Escalation (User Recognition)
If a Hard Error is contested:
1. The agent marks it as `contested`.
2. Adds a brief justification.
3. The User provides the final Recognition verdict.

## 5. Deletion Policy (Tombstone)

Hard deletion of pages or threads requires the creation of a "Tombstone" record in a cemetery log to preserve the history of the structure and avoid "ghost links."
