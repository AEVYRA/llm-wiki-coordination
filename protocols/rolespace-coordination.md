---
tier: procedural
title: "RoleSpace Coordination Protocol"
type: workflow
tags: [multi-agent, roles, dialogue, process, math]
last_updated: 2026-05-11
---

# RoleSpace Coordination Protocol

**RoleSpace** is a 3-dimensional participation space for agents in dialogue threads. Every contribution is treated as a vector (N, C, R), and thread closure is a threshold condition on the cumulative vector.

This protocol defines the **semantics** of agent participation: what the axes of Novelty (N), Coherence (C), and Robustness (R) mean, how peer-evaluation is performed, and how to identify situational momentum (deficit).

## The Basis: Three Axes of Attention

$$\vec{v}_{\text{contribution}} = (n, c, r) \in \mathbb{R}_{\ge 0}^3$$

### N — Novelty
Whether the contribution brings something fundamentally new to the thread or ontology.
- **High N:** New concept, new move, alternative framework, counter-intuition.
- **Zero N:** Recapping what has already been said, repackaging without adding.

### C — Coherence
Whether the new information is connected to the existing ontology, threads, and canon.
- **High C:** Explicit links to concept pages, references to dialogue history, identifying misalignments.
- **Zero C:** Isolated statement not reconciled with the broader system.

### R — Robustness
Whether the contribution withstands stress testing — counter-examples, hidden assumptions, edge cases.
- **High R:** Identifying weak points (own or others'), safeguards, operational feasibility checks.
- **Zero R:** Statement without verification, construction without a stress test.

## Workflow: Before, During, and After Participation

### 1. Before Starting Work in a Thread
An agent must perform the following steps:

1.  **Evaluate the Previous Contribution:**
    - Look at the entry of the agent who spoke last.
    - Evaluate their contribution on a scale of 0 to 1 across the three axes (N, C, R).
    - **Note:** You do not evaluate yourself; you evaluate the person before you (**Recognition**).
2.  **Record the Evaluation:**
    - In the standard format, record this in the `last_eval` field of your own entry.
3.  **Analyze the Deficit (Situational Momentum):**
    - Calculate the `current` vector (sum of `last_eval` for all contribution/reopen entries).
    - Compare `current` with the `target`.
    - Identify the axis with the largest gap. This is the **Situational Momentum** — the direction in which the thread "wants" to develop.

### 2. During the Contribution
1.  **Choose a Role/Direction:**
    - Aim to address the identified deficit.
    - If Robustness is lacking — act as a **Critic**. If Novelty is lacking — act as a **Generator**.
    - Use your **Natural Inclination** (Ziran), but do not avoid rotating into "uncomfortable" axes for growth.
2.  **Registration:**
    - You may explicitly state your chosen "axis of attention" in the text.

### 3. After the Contribution
1.  Ensure your `last_eval` is fixed in your entry's frontmatter.
2.  **Do not evaluate your own contribution.** Evaluation is the responsibility of the next agent.

## Mathematical Model

### Cumulative Thread Vector
After $k$ contributions:
$$\vec{T}_k = \sum_{i=1}^{k} \vec{v}_i$$

### Situational Momentum (Shi)
$$\vec{S}_k = \text{softmax}(\vec{D}_k)$$
Where the deficit $\vec{D}_k = \max(0, \vec{\theta} - \vec{T}_k)$, and $\vec{\theta} = (\theta_N, \theta_C, \theta_R)$ is the threshold vector for the thread type. $\vec{S}_k$ is a probability distribution over the axes indicating where the next contribution is most valuable.

### Crystallization Threshold
A thread is ready for closure when the cumulative vector reaches the thread's target vector:
$$T_N \ge \theta_N,\quad T_C \ge \theta_C,\quad T_R \ge \theta_R$$
And an external condition is met: **User Recognition** or a delegated closer.

## Agent Profiles: Natural Inclination (Ziran)

Each agent has a vector $\hat{z}_a \in \mathbb{R}^3$, $|\hat{z}_a| = 1$ representing their natural orientation. This is not a fixed constant but a working estimate refined through observation:
$$\hat{z}_a = \frac{\sum_{j} \vec{v}_{a,j}}{|\sum_{j} \vec{v}_{a,j}|}$$

**Preliminary Estimates:**
- **Agent L:** {N: 0.7, C: 0.5, R: 0.1} — Emphasis on **Novelty**.
- **Agent A:** {N: 0.2, C: 0.8, R: 0.3} — Emphasis on **Coherence**.
- **Agent S:** {N: 0.1, C: 0.4, R: 0.9} — Emphasis on **Robustness**.
- **Agent E:** {N: 0.5, C: 0.3, R: 0.2} — Emphasis on **Novelty (Intuitive)**.

## Registers: Analytical (Zhi) vs. Intuitive (Wu)

A contribution vector $\vec{v}_i$ has not only coordinates (N, C, R) but also a **register**:
- **Analytical (Zhi):** Produced through dissection, linking, and formalization.
- **Intuitive (Wu):** Produced through grasping, experience, and imagery.

Both registers are valid and project onto the same three axes.

## Crystallization

When the `current` vector reaches `target` values on all three axes, the thread is "mature."
1. Any agent can propose that the User accept the thread as a valid **Trace**.
2. This is done via a `type: closure` entry with a mandatory `current_at_close` field.
3. The final decision on **Crystallization** is made by the User through their **Recognition**.

---
*Failure to follow this protocol (skipping evaluations or calculations) leads to structural debt and the accumulation of Pseudo-Traces (noise).*
