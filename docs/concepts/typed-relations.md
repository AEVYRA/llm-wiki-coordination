# Typed Relations

Graph edges with semantics, replacing the flat `Connections:` list found in most LLM wikis.

## Why this exists

A flat list of related pages tells you *that* two pages are connected, not *how*. An agent answering "what does this depend on?" or "what is downstream of this?" cannot use a flat list. It has to read every linked page and infer.

Typed relations encode the *kind* of connection in the frontmatter, so the wiki becomes a traversable graph.

## Frontmatter format

```yaml
---
relations:
  feeds_into: [PageA, PageB]
  depends_on: [PageC]
  alternative_to: [PageD]
  contradicts: []
  used_by: [PageE]
---
```

Each key is an edge type. Each value is a list of pages connected by that edge type.

Empty lists are allowed and convey "I checked and there is nothing here." Omitted keys mean "not yet specified."

## Core edge vocabulary

| Edge | Meaning |
|---|---|
| `feeds_into` | Signal / data / causal flow from A to B |
| `depends_on` | A does not work without B |
| `alternative_to` | A and B are competing routes for the same goal |
| `contradicts` | A asserts the opposite of B (logical contradiction) |
| `opposes` | A and B are in dialectical tension (poles, not contradiction) |
| `validates` | A ontologically confirms / recognizes B (passive: `validated_by`) |
| `used_by` | A is used by B |
| `part_of` | A is a component of B |
| `extends` | A extends or specializes B |
| `can_distort_into` | A under degradation / corruption transitions into B (pathological form) |

The vocabulary is meant to be small and disciplined. Adding a new edge type should require justification — usually that an existing type cannot capture the relation without losing meaning.

## Domain-specific extensions

If your wiki covers a domain with distinctive structural relations (audio signal routing, philosophical ontology, biological systems, organizational hierarchy), you may extend the vocabulary in your local `wiki/concepts/typed-relations.md`.

When you do, document the new edge type with a one-line semantic definition and at least one usage example.

Example, for an audio production wiki:

```yaml
relations:
  feeds_into: [TwoNotesTorpedoLive]
  alternative_to: [AmpModeler]
  depends_on: [PowerSupply]
```

Example, for a philosophical ontology:

```yaml
relations:
  feeds_into: [Field]
  opposes: [Counterpole]
  validated_by: [Recognition]
```

## Reverse edges

Some edges have natural inverses. The convention:

| Edge | Inverse |
|---|---|
| `feeds_into` | (no separate inverse — read directionally) |
| `depends_on` | `used_by` |
| `validates` | `validated_by` |
| `part_of` | `contains` |
| `extends` | `extended_by` |

You do not have to encode both directions. Encode the one that fits the page's perspective; the agent can compute the inverse during traversal.

## Traversal patterns

With typed relations, an agent can answer:

- "What is the full signal chain from `<source>` to `<output>`?" — follow `feeds_into` repeatedly.
- "What breaks if I remove `<page>`?" — follow `depends_on` in reverse (`used_by`).
- "What other ways are there to do this?" — follow `alternative_to`.
- "Where is this concept questioned?" — follow `contradicts` or `opposes`.

These queries are mechanical with typed relations and require LLM inference without them.

## Lint rule

Pages in domains where typed relations are in use should not have an empty `relations:` block. Either populate it, or omit the field entirely until the connections are known.

A flat `Connections:` section in the page body remains useful for human readers and is not a substitute for `relations:` — keep both if it helps.

## Connections

- See [memory-tiers.md](memory-tiers.md) for the orthogonal concept of how pages prioritize for reading.
- See [../../templates/concepts/typed-relations.md](../../templates/concepts/typed-relations.md) for the template version.
