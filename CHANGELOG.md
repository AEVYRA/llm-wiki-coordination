# Changelog

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
