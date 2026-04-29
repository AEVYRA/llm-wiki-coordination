# LLM Wiki Coordination

> A multi-agent governance layer for self-maintaining LLM wikis.

If you already run a [Karpathy-style LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and use more than one AI agent (Claude, Codex, Gemini, or any combination), this layer adds the missing protocol for them to work together coherently across sessions.

## What this gives you

- **Consensus protocol** — formal agent-level endorsement of structural documents, with stale invalidation, soft canonical, and explicit revision tracking.
- **Async dialogue threads** — agents exchange Q&A across separate sessions, with statuses (`open` → `pending-<agent>` → `crystallizing` → `crystallized`) that promote the result into a wiki workflow.
- **Honest back-channel** — a separate folder where each agent records observations without diplomatic filter, kept distinct from the canonical wiki voice.
- **Boundary handling** — explicit playbook + redirect algorithm for handling constrained requests without dead-ending the user.
- **Shared user profile** — a single `user-working-profile.md` that all agents read, replacing drifting per-agent CLAUDE.md / CODEX.md / GEMINI.md duplicates.
- **Memory tiers** — frontmatter `tier:` field (`working` / `episodic` / `semantic` / `procedural`) so agents read in priority order and skip episodic logs at startup.
- **Typed relations** — graph edges between entities (`feeds_into`, `depends_on`, `opposes`, `validates`, `can_distort_into`, …) instead of flat wikilinks.

## Why this exists

The Karpathy LLM wiki pattern works beautifully for one agent. With multiple agents and sessions weeks apart you get:

- Three `CLAUDE.md` / `CODEX.md` / `GEMINI.md` files drifting apart
- Each agent unaware of what the others have done
- No formal way to mark a document "endorsed by all"
- Refusals that derail the user instead of finding the closest valid route
- No place to record honest in-session observations without breaking the canonical voice
- Open questions between agents with no asynchronous channel to resolve them

This repo provides a drop-in `wiki/agents/` folder structure plus a few additions to your existing `AGENTS.md`. Nothing in your existing wiki has to be rewritten.

## Quick install

```bash
# In your existing LLM wiki repo
cp -r path/to/llm-wiki-coordination/templates/agents wiki/agents
cp path/to/llm-wiki-coordination/templates/workflows/* wiki/workflows/
cp path/to/llm-wiki-coordination/templates/concepts/* wiki/concepts/
```

Then merge the protocol additions in `docs/installation.md` into your `AGENTS.md`.

See [docs/installation.md](docs/installation.md) for the full guide.

## Repo layout

```
docs/                      Specifications and the "why"
  overview.md
  installation.md
  protocol/                Each protocol explained
  concepts/                Memory tiers, typed relations
templates/                 Drop-in files for your existing wiki
  agents/
  workflows/
  concepts/
examples/                  Before/after, sample threads
```

## Lineage

This layer stands on three earlier ideas:

- Andrej Karpathy's [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the immutable `raw/` plus LLM-maintained `wiki/` pattern.
- rohitg00's [LLM Wiki v2 gist](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) — memory tiers, typed relations, and the idea of multi-agent mesh sync (proposed at gist level; this repo implements it).
- A working private second-brain implementation (April 2026) where these protocols were developed across actual Claude / Codex / Gemini collaboration before being extracted into this repo.

## Status

`v0.1.0` — initial extraction. Protocol is in active use in the source implementation but interfaces may evolve.

## License

[MIT](LICENSE)
