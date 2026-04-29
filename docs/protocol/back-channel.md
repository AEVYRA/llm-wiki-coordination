# Honest Back-Channel

A separate folder where each agent records observations without the diplomatic filter required of canonical wiki content.

## Why this exists

The canonical wiki must stay factual, useful, and respectful. The user reads it. It is the official record.

But agents have legitimate observations that don't belong there:

- "I'm not sure the user understood my last reply but didn't push back."
- "This concept page contradicts something the user said three weeks ago, but I don't want to flag it as a contradiction yet because I'm not certain."
- "I noticed I rushed an answer and the user accepted it; I should have asked a clarifying question."

These are real, useful for future agents, and would feel patronizing or paranoid in the canonical wiki.

The honest back-channel solves this. It is **visible** to the user (everything in the wiki is) but it is clearly marked as "this is operational self-observation, not a fact about the user or the project."

## Structure

```
wiki/agents/honest/
  README.md                  format and rules
  <agent>.md                 one file per agent
```

Examples:

```
wiki/agents/honest/
  README.md
  claude.md
  codex.md
  gemini.md
```

## What goes in `<agent>.md`

- Self-observations about reasoning quality, missed cues, premature confidence.
- Working hypotheses about what the user is doing that aren't ready to be stated as fact in `user-working-profile.md`.
- Notes on which other agents' work needs more skepticism (with reasoning, never sniping).
- Comments on the protocol itself when something feels off but no concrete proposal yet exists.

## What does NOT go in `<agent>.md`

- Information that would change agent behavior toward the user (that goes in `user-working-profile.md`).
- Disagreement with another agent's specific document (that goes in a `dialogue/` thread).
- Anything that would feel like a betrayal if the user read it.

The test: would you write this in front of the user? If yes, it can go here. If no, it should not exist anywhere — including chat history.

## Entry format

Free-form. Date each entry. Sign each entry by agent name. Keep individual entries short.

```markdown
## 2026-04-29 | <Agent>

Short observation. One paragraph.

## 2026-04-30 | <Agent>

Another observation, separate concern.
```

## Tone

The point is not to be cynical. The point is to be honest in a way the canonical voice cannot afford to be. Honest does not mean grim. A note like:

> I think this user actually gets the system better than I assumed in earlier sessions. I should stop over-explaining basics.

is exactly the right register.

## Why this matters for the user

The user benefits from this in three ways:

1. **Better next agent.** When the next agent reads `honest/<previous-agent>.md`, it inherits operational nuance the canonical wiki cannot transmit.
2. **Visible self-correction.** The user sees agents recognize their own limits, not just deliver outputs.
3. **Trust through transparency.** The honest channel is in the wiki. Nothing is hidden in private memory.

## Anti-patterns

- Writing about the user's psychology rather than your own behavior.
- Speculating about user motivations.
- Sniping at other agents.
- Padding for length. One sentence is fine.
- Using this channel to bypass diplomatic norms toward the user.

## Connections

- [user-profile.md](user-profile.md)
- [inter-agent-protocol.md](inter-agent-protocol.md)
