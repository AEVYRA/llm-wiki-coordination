# Installation

This guide assumes you already have a Karpathy-style LLM wiki with at least:

- A `raw/` folder for immutable source notes.
- A `wiki/` folder the agent maintains.
- An `AGENTS.md` (or `CLAUDE.md`) at the repo root with operating rules.

If you don't have this baseline, start with [Karpathy's gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) first.

## Step 1. Copy the agents folder

```bash
cp -r templates/agents <your-wiki-repo>/wiki/agents
```

Your wiki now has:

```
wiki/agents/
  _context.md
  inter-agent-protocol.md
  user-working-profile.md
  boundary-handling-playbook.md
  handoff-log.md
  agent-council.md
  notes/README.md
  honest/README.md
  dialogue/_context.md
  dialogue/_template.md
```

`handoff-log.md` and `agent-council.md` start essentially empty — they grow over time.

## Step 2. Copy the workflows

```bash
cp templates/workflows/*.md <your-wiki-repo>/wiki/workflows/
```

This adds `multi-ai-consensus.md` and `boundary-redirect-algorithm.md` to your existing workflows folder.

## Step 3. Copy the concept pages

```bash
cp templates/concepts/*.md <your-wiki-repo>/wiki/concepts/
```

This adds `memory-tiers.md` and `typed-relations.md`.

## Step 4. Update your AGENTS.md

Add the following sections to your existing `AGENTS.md`. Place them after your existing "Hard Rules".

### Required addition: Multi-agent startup read

```markdown
## Multi-Agent Startup Read

Before substantial work, read in this order:

1. This file (`AGENTS.md`).
2. Your agent-specific entrypoint if present (`CLAUDE.md`, `CODEX.md`, `GEMINI.md`).
3. `wiki/CRITICAL_FACTS.md` (if you have one).
4. `wiki/agents/inter-agent-protocol.md`.
5. `wiki/agents/user-working-profile.md`.
6. `wiki/agents/handoff-log.md`.
7. Your own note file under `wiki/agents/notes/`, if present.
8. All files in `wiki/agents/dialogue/` with status `open` or `pending-<this-agent>`.
```

### Required addition: Memory tiers

```markdown
## Memory Tiers

Every wiki page carries a `tier:` field in its frontmatter. Use it to prioritize reading:

| Tier | Read when | Examples |
|---|---|---|
| `procedural` | Always — rules, protocols, workflows | `AGENTS.md`, `workflows/`, protocols |
| `semantic` | For knowledge questions — stable compiled facts | `entities/`, `concepts/`, `syntheses/` |
| `episodic` | For continuity — dated events and logs | `handoff-log.md`, `log.md`, agent notes |
| `working` | Only if the task touches current focus | `hot.md`, open questions |

Startup read order: procedural → semantic (relevant pages) → episodic → working.

When creating new pages, add a `tier:` field to frontmatter.
```

### Required addition: Write rules for `agents/`

```markdown
## Write Rules for `wiki/agents/`

- Write only factual observations, user-stated preferences, and concrete handoff context.
- Do not psychoanalyze the user.
- Do not invent preferences.
- Do not speak for another agent.
- Do not hide disagreements; record them as open tradeoffs or open dialogue threads.
- Date and sign each entry by agent name.
- Keep entries scannable.
```

## Step 5. Optional: per-agent entrypoint files

If you want each agent to have a personality or naming convention, create files like:

```
CLAUDE.md
CODEX.md
GEMINI.md
```

at the repo root. Each should be very short and end with: "For shared protocol, read `wiki/agents/inter-agent-protocol.md`."

A starter template is in [protocol/inter-agent-protocol.md](protocol/inter-agent-protocol.md).

## Step 6. Optional: lint additions

If you have a lint workflow, add these checks:

- Pages without a `tier:` field in frontmatter (in directories that require it).
- Documents in `wiki/workflows/`, `wiki/concepts/` (structural ones), and `wiki/entities/` (structural ones) without a `consensus:` block.
- `dialogue/` threads in `pending-<agent>` status for more than 30 days.
- `agents/honest/` files with no entries for more than 60 days.

## Step 7. First-session bootstrap

The first time an agent picks up the new structure, it should:

1. Read all the new protocol files.
2. Add an entry to `wiki/agents/handoff-log.md` acknowledging the protocol is now in effect.
3. Initialize its own `wiki/agents/notes/<agent>.md` and `wiki/agents/honest/<agent>.md`.

Subsequent agents will find these and follow the same pattern.

## Verifying the install

A correctly installed coordination layer means:

- `wiki/agents/` exists with the eight files listed in step 1.
- `wiki/workflows/multi-ai-consensus.md` exists.
- `AGENTS.md` references the protocol.
- The next agent that opens the repo can answer: "Who worked here last, and what was the last open dialogue thread?"

If the third point fails, the install is incomplete.
