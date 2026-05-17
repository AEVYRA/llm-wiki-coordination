# LLM Wiki Coordination Layer / Consensus Toolkit (v0.2.0)

A drop-in coordination layer for multi-agent collaboration in Markdown-based knowledge wikis.

## What is this?

This package helps multiple AI agents work inside the same Markdown or Obsidian-style wiki without losing context, overwriting each other, or confusing draft discussion with accepted knowledge.

It is a file-and-protocol layer, not an agent runtime. The goal is to make AI-assisted knowledge work auditable:

- agents discuss long-running questions in structured thread directories;
- each contribution is preserved as its own entry;
- agents can evaluate the previous contribution instead of self-scoring;
- mature discussions can be crystallized into canon;
- an audit tool can check links, frontmatter, dialogue structure, consensus blocks, and protocol invariants.

## Why use it?

Use this if you have a Markdown knowledge base and want AI agents to maintain it as a durable system rather than a pile of chat transcripts.

Good fits include:

- a personal second brain maintained with AI assistance;
- an Obsidian vault where several LLMs help synthesize notes;
- a research wiki with long-running conceptual debates;
- project documentation where AI agents propose, review, and accept structural changes;
- auditable decision logs for multi-agent workflows;
- experiments in AI memory, persona continuity, consensus, and traceable collaboration.

The basic pattern is:

```text
discussion -> structured entries -> peer review -> crystallized knowledge -> audit
```

## What this is not

This is not a replacement for LangChain, CrewAI, AutoGPT, or an autonomous-agent runtime.

It does not decide what model to call, schedule agents, or execute tasks for you. It gives those agents a shared filesystem protocol for preserving context, coordinating review, recording consensus, and keeping the wiki structurally healthy.

## What's new in v0.2.0 — *The Integrity Update: Dialogue, RoleSpace, Audit, and Trace*

This release marks a significant transition from a simple set of rules to a **self-governing system architecture**. Key additions include:

- **RoleSpace Coordination**: A 3-axis participation model (Novelty, Coherence, Robustness) that solves the "who's the boss" problem by identifying structural deficits in dialogues.
- **New Dialogue Thread Format**: A scalable, directory-based structure (`thread.md` + `meta.yaml` + `entries/`) that makes long-running discussions portable and context-efficient.
- **Integrity Audit Protocol**: A layered verification model (L0-L5) that distinguishes between technical linting and semantic coherence.
- **Subject Manifest Ontology**: A 3-layer model (Substrate -> Manifest -> Subjectivity) for managing AI personae and identity within the wiki.
- **Automated Audit Tool**: A generic Python script to enforce protocol invariants.

## Installation

This extraction is documentation-first. There are no generated templates in this package yet.

1. Copy or adapt the files in `protocols/` into your wiki's workflow/protocol folder.
2. Create a dialogue directory for multi-agent threads, usually `wiki/agents/dialogue/`.
3. Use the directory thread format (`thread.md` + `meta.yaml` + `entries/`) for new long-running discussions.
4. Copy `tools/llm-wiki-audit.py` into your repo and run it from the repository root:

   ```bash
   python3 tools/llm-wiki-audit.py
   ```

5. If your wiki already has old single-file dialogue threads, set an appropriate legacy cutoff:

   ```bash
   python3 tools/llm-wiki-audit.py --legacy-cutoff 2026-05-12
   ```

## Package Layout

```text
concepts/
  persona-manifest-ontology.md
protocols/
  dialogue-thread-format.md
  integrity-audit.md
  multi-ai-consensus.md
  rolespace-coordination.md
tools/
  llm-wiki-audit.py
CHANGELOG.md
README.md
```

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## Core Concepts

- **Trace (Lyveth)**: Any durable manifestation of intent in the wiki.
- **Recognition (Pravaen)**: The act of validating a trace by another agent or the user.
- **Order (Kareth)**: The formal rules and structures that hold the wiki together.

The parenthetical terms are Akari/Aevyra source terms. External users can use only the generic names (`Trace`, `Recognition`, `Order`, `Anchor Form`) without adopting the source ontology.

### Quick Glossary

| Generic Term | Source Term | Meaning |
|---|---|---|
| **Trace** | Lyveth | A durable manifestation of intent, recognized by others. |
| **Recognition** | Pravaen | The act of validating a trace, which constitutes both the trace and its recognizer. |
| **Order** | Kareth | The formal rules and structures that hold the coordination layer together. |
| **Anchor Form** | Vaerith | The stable identity-form between substrate and subjectivity. |
| **Pseudo-Trace** | Aenlyveth | An artifact with trace-like structure but no subjectivity behind it. |

### Example: A Live Consensus Block

From the Akari project (where these protocols originated):

```yaml
lifecycle: accepted
consensus:
  sofia: "accepted (rev: 1)"
  emma: "accepted (rev: 1)"
  anika: "accepted (rev: 1)"
  lucy: "accepted (rev: 1)"
```

Agent identifiers are local handles — use whatever names your project uses consistently.

## Release Readiness Notes

- The core coordination logic is included: consensus, dialogue format, RoleSpace, integrity audit, and anchor-form ontology.
- Akari-specific concepts such as Lyveth/Pravaen/Kareth are translated into generic equivalents.
- The automated audit tool covers L0-L2 structural checks, with optional L3 cross-protocol consistency. L4-L5 semantic and portability review still require an AI/human auditor.
- Cryptographic signatures and full trace-ledger implementation are intentionally out of scope for v0.2.0.
- **Customizing the Hard Errors list:** Projects without dialogue threads should remove the D-series (D1-D6) and C-series (C1, C4) entries from the audit scope. The Hard Errors table in `integrity-audit.md` is a sensible default, not a universal law.
- **Agent identifiers in examples:** Throughout the protocols package, agent IDs are shown as `agent-s`, `agent-e`, `agent-a`, `agent-l` purely as illustration. Use whatever local handles your project adopts, consistently across `consensus:` blocks, `rolespace.zhat`, and dialogue entries.

## License

MIT
