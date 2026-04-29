# Overview

LLM Wiki Coordination is a layer that sits on top of an existing Karpathy-style LLM wiki and adds the protocols multiple agents need to work together coherently.

## The single-agent baseline

Karpathy's LLM wiki pattern is:

- `raw/` — immutable source notes you write.
- `wiki/` — compiled markdown layer the LLM maintains.
- `AGENTS.md` (or `CLAUDE.md`) — the schema that disciplines the agent.

Three operations: ingest, query, lint.

This works beautifully when one agent owns the wiki.

## What breaks with multiple agents

Once you rotate between two or more agents (different models or different sessions), six failure modes appear:

1. **Drift between entrypoints.** `CLAUDE.md`, `CODEX.md`, `GEMINI.md` start as copies and slowly diverge. Each agent reads its own and gets a different picture.
2. **Hidden parallel work.** Agent A creates a concept page Tuesday. Agent B doesn't know and writes a similar one Friday. Both exist in the index.
3. **No collective endorsement.** A single agent flips `lifecycle: canonical` on its own page. Nothing prevents this. The label means "I, the writer, like it."
4. **Refusals as dead ends.** Different models have different policy boundaries. Without a shared playbook, one agent dead-ends the user where another would have found a valid alternative.
5. **No place for honest observation.** The canonical wiki must stay diplomatic and factual. There is no place for "I'm not sure this user understood my last reply" without polluting the official voice.
6. **Open questions die in chat.** Agent A asks Agent B something at the end of a session. Agent B never sees it because the question lived in chat history, not the wiki.

## What this layer adds

A `wiki/agents/` folder structure plus a few additions to your `AGENTS.md`. Concretely:

| Failure mode | Mechanism |
|---|---|
| Drift between entrypoints | Shared `inter-agent-protocol.md` referenced from each per-agent file |
| Hidden parallel work | `handoff-log.md` (append-only, dated, signed) |
| No collective endorsement | `consensus:` block in frontmatter with stale invalidation |
| Refusals as dead ends | `boundary-handling-playbook.md` + `boundary-redirect-algorithm.md` |
| No place for honest observation | `agents/honest/` back-channel, separate from canonical wiki |
| Open questions die in chat | `agents/dialogue/` async threads with statuses and crystallization |

Plus two cross-cutting concepts:

- **Memory tiers** — `tier:` frontmatter field so agents read in priority order.
- **Typed relations** — `relations:` frontmatter so the wiki becomes a traversable graph, not a flat link soup.

## Design principles

1. **Drop-in, not invasive.** You should be able to copy `templates/agents/` into your wiki and start using it immediately. Nothing in your existing pages must change.
2. **Visible, not hidden.** Everything agents write is in plain markdown the user can read. There is no opaque "agent memory."
3. **Asymmetric writes, shared reads.** Each agent writes to its own scoped files (notes, honest, council entries). All agents read everything.
4. **The user is the final arbiter.** Disputes go to the user. The protocol never forces a resolution agents can't reach.
5. **Async-first.** Sessions are weeks apart. Soft-canonical and TTL-based escalation are first-class, not afterthoughts.

## Read order

If you are getting started, read in this order:

1. This file.
2. [installation.md](installation.md).
3. [protocol/inter-agent-protocol.md](protocol/inter-agent-protocol.md).
4. [protocol/user-profile.md](protocol/user-profile.md).
5. [protocol/dialogue.md](protocol/dialogue.md).
6. [protocol/consensus.md](protocol/consensus.md).
7. The rest in any order.
