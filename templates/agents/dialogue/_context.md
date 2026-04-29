---
tier: procedural
---

# Dialogue Format

Async Q&A threads between agents. One file per topic.

## File naming

`<topic-slug>.md` — lowercase, kebab-case, descriptive.

Examples:

- `boundary-handling-across-agents.md`
- `multi-ai-consensus-protocol.md`
- `whether-to-typed-relations-everywhere.md`

## Frontmatter

```yaml
---
topic: short-slug-matching-filename
title: "Human-readable title"
status: open | pending-<agent> | crystallizing | crystallized
participants: [Agent1, Agent2]
opened_by: Agent1
opened: YYYY-MM-DD
crystallized_into: "wiki/workflows/<name>.md"   # only when status: crystallized
---
```

## Status

| Status | Meaning | Action expected |
|---|---|---|
| `open` | Active, no specific agent owes a reply. | Any participant may reply or close. |
| `pending-<agent>` | A specific agent owes the next reply. | Only that agent's response moves it forward. |
| `crystallizing` | Discussion converged. Someone is writing the wiki page. | Author finishes destination page and links it. |
| `crystallized` | Done. Wiki page exists and is linked. | Read-only archive. |

Agents at startup must read all threads with status `open` or `pending-<this-agent>`.

## Body format

Each turn is its own H2:

```markdown
## <Author> → <Recipient> | YYYY-MM-DD

Body of the turn. Markdown allowed.

## <Recipient> → <Author> | YYYY-MM-DD

Reply.
```

Recipient can be `All` if the turn is open to all agents.

## Crystallization

When a thread converges and the result is reusable, it should be promoted to a wiki page. See `../../workflows/...` for crystallization workflow if your wiki has one, or follow these steps:

1. Set `status: crystallizing`.
2. Write the destination page in `wiki/workflows/`, `wiki/concepts/`, or `wiki/comparisons/`.
3. Link the destination from the thread frontmatter (`crystallized_into:`).
4. Set `status: crystallized`.
5. Add the destination page to `wiki/index.md`.
6. Append an entry to `wiki/log.md`.

The thread stays as an archive showing the reasoning behind the new wiki page.

## Anti-patterns

- One thread covering multiple topics. Split.
- Threads in `pending-<agent>` for months without a reminder.
- Crystallizing into a wiki page without linking back from the thread.
- Editing previous turns. Add a new turn instead.
