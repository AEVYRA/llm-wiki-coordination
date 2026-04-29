---
title: "Typed Relations"
type: concept
tier: semantic
tags: [knowledge-graph, entities, relations, llm-wiki]
last_updated: YYYY-MM-DD
lifecycle: working
consensus:
  REPLACE-WITH-FIRST-AGENT: "contributed (initial install) | YYYY-MM-DD | rev: v1"
---

# Typed Relations

Graph edges with semantics, replacing the flat `Connections:` list found in most LLM wikis.

## Frontmatter format

```yaml
---
relations:
  feeds_into: [PageA, PageB]
  depends_on: [PageC]
  alternative_to: [PageD]
  used_by: [PageE]
---
```

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
| `can_distort_into` | A under degradation transitions into B (pathological form) |

## Domain extensions

If your wiki has distinctive structural relations, you may extend the vocabulary. Document each new edge with a one-line semantic and at least one usage example.

## Reverse edges

Some edges have natural inverses. You only need to encode one direction; the agent can compute the inverse during traversal.

| Edge | Inverse |
|---|---|
| `depends_on` | `used_by` |
| `validates` | `validated_by` |
| `part_of` | `contains` |
| `extends` | `extended_by` |

## Traversal patterns

With typed relations, an agent can answer:

- "What is the full chain from `<source>` to `<output>`?" — follow `feeds_into`.
- "What breaks if I remove `<page>`?" — follow `depends_on` in reverse.
- "What other ways are there to do this?" — follow `alternative_to`.
- "Where is this concept questioned?" — follow `contradicts` or `opposes`.

These queries become mechanical with typed relations.

## Lint rule

Pages in domains where typed relations are in use should not have an empty `relations:` block — either populate it or omit the field until connections are known.

A flat `Connections:` section in the page body remains useful for human readers and is not a substitute.

## Connections

- `memory-tiers.md`
