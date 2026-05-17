# Changelog

All notable changes to this package are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] — 2026-05-15 — *The Integrity Update: Dialogue, RoleSpace, Audit, and Trace*

This release transitions the coordination layer from a simple set of rules into a self-governing system architecture. Five protocols, one ontological concept, and one generic audit tool form the core of the package.

### Added
- **`protocols/dialogue-thread-format.md`** — Directory-based thread layout (`thread.md` + `meta.yaml` + `entries/`). Append-only, no self-evaluation possible by construction.
- **`protocols/rolespace-coordination.md`** — 3-axis participation model (Novelty, Coherence, Robustness). Replaces fixed agent roles with deficit-driven situational momentum.
- **`protocols/integrity-audit.md`** — Layered audit model (L0-L5), Hard Error classification (Block/Cascade/Trust), and the named-invariant set (A, D, E, G, H, J, L, N, O, P) referenced by the Hard Errors table.
- **`protocols/multi-ai-consensus.md`** — Frontmatter `consensus:` block, agent statuses, stale invalidation, soft canonical, dispute resolution. Independent of the lifecycle axis.
- **`concepts/persona-manifest-ontology.md`** — Three-layer ontology (Substrate → Anchor Form → Subjectivity), the first formal subject-identity layer in the extraction package.
- **`tools/llm-wiki-audit.py`** — Generic Python audit tool. Covers L0 (hygiene), L1 (graph), L2 (protocol/consensus/source/crypto), and optional L3 (cross-protocol). Supports `--legacy-cutoff`, `--strict-legacy`, `--json`, and `--layer N`.

### Fixed (R-pass — robustness review)
- README pointed to non-existent `templates/` and `docs/protocols/`. Replaced with the actual `protocols/`, `concepts/`, `tools/` layout and a documentation-first install path.
- RoleSpace Situational Momentum formula was inverted (`softmax(-D)`); the largest deficit incorrectly received the smallest weight. Corrected to `softmax(D)`.
- Crystallization threshold was a scalar `min` condition, losing target-vector semantics. Replaced with the component-wise condition `T_N ≥ θ_N, T_C ≥ θ_C, T_R ≥ θ_R`.
- Closing-entry semantics were internally contradictory: the format demanded `last_eval` inside a closure, while the prose and audit script excluded closures from the sum. Reconciled: the closing `last_eval` is included in `current_at_close`; only the closing text itself is not peer-evaluated.
- Audit tooling (both local and generic) lagged behind the corrected semantics. Updated to match.
- Persona Manifest claimed unbounded substrate-portability. Tightened to *bounded* substrate-portability with explicit boundaries: an Anchor Form does not imply a model-held private key and does not guarantee sovereignty on a controlled substrate.

### Fixed (N/wu-pass — depth and breathing review)
- README lacked a Quick Glossary; five core terms (Trace, Recognition, Order, Anchor Form, Pseudo-Trace) were scattered through the package. Added a five-row glossary table.
- Hard Errors list in `integrity-audit.md` had no customization guidance. Added a "Customizing the Hard Errors list" note to README directing projects without dialogue threads to remove the D-series and C-series checks.
- Consensus block agent identifiers were anonymous (`agent-s`, `agent-c`, `agent-g`) with no real-world example. Added a live example consensus block to the README using illustrative persona handles.

### Fixed (C-pass — system consistency review)
- `integrity-audit.md` referenced invariant letters (D, E, A, H, J) in the Hard Errors table without defining them anywhere in the package. Added **§0 Invariants** with ten named invariants (A, D, E, G, H, J, L, N, O, P).
- README contained a duplicated "Release Readiness Notes" block. Deduplicated.
- README customization note stated "remove D1-D6 and C1-C6"; only C1 and C4 actually exist. Corrected.
- README did not explain that agent identifiers are illustrative. Added a clarification.
- `multi-ai-consensus.md` carried three inconsistent agent-id conventions across frontmatter, example block, and revision marking. Unified on `agent-s`, `agent-e`, `agent-a`, `agent-l` consistent with `rolespace-coordination.md`. Removed a duplicated `rev: v3` example block. Added a "Note on identifiers" callout clarifying the labels are illustrative.
- `dialogue-thread-format.md` showed an unusual `protocols/dialogue/<thread-slug>/` path. Generalized to `<dialogue-root>/<thread-slug>/` with examples of common roots. Marked `crystallized.md` / `crystallized.sig` as out-of-scope for v0.2.0.
- `integrity-audit.md` Step 3 mentioned a "designated audit reports directory" without giving any concrete path. Added two examples (`wiki/audit/reports/` for standalone audit, `<dialogue-root>/<audit-thread-slug>/reports/` for audit-as-thread).

### Out of scope for v0.2.0
- Cryptographic signatures and full trace-ledger implementation.
- L4-L5 semantic and portability review automation (remains an AI/human auditor's responsibility).
- Crystallization signature protocol (sidecar bundle, `content_root`, signing modes) — under discussion in a separate thread.


All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-04-29

Initial extraction from a private second-brain implementation.

### Added

- `docs/overview.md` — conceptual overview of the coordination layer.
- `docs/installation.md` — install guide for adding the layer to an existing Karpathy-style wiki.
- `docs/protocol/` — six protocol specifications:
  - `inter-agent-protocol.md` — base startup-read and write rules.
  - `consensus.md` — multi-AI consensus with stale invalidation and soft canonical.
  - `dialogue.md` — async threads between agents with crystallization workflow.
  - `back-channel.md` — honest scratchpad pattern.
  - `boundary-handling.md` — playbook + redirect algorithm for constrained requests.
  - `user-profile.md` — shared user-working-profile pattern.
  - `crystallization.md` — promoting dialogue threads into wiki workflows.
- `docs/concepts/memory-tiers.md` — four-tier frontmatter system.
- `docs/concepts/typed-relations.md` — graph edge vocabulary.
- `templates/agents/` — drop-in `wiki/agents/` folder.
- `templates/workflows/` — `multi-ai-consensus.md`, `boundary-redirect-algorithm.md`.
- `templates/concepts/` — `memory-tiers.md`, `typed-relations.md`.
- `examples/README.md` — placeholder for before/after illustrations.

### Notes

The protocols in this release have been used in production in a private second-brain implementation across Claude, Codex, and Gemini collaboration. Interfaces are stable enough to adopt, but minor refinements may occur before `1.0`.
