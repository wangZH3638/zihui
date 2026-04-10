---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502206221a7877fc7528d1fac86425f0a938aea329e6c63881224413795d63428b537022100bce9f862a976985655be9d420ccfc4cbc107ec7ac19d54b289d1776ee892803e
    ReservedCode2: 304502203d6e4d790261dc6a1c9bf375c7bd8c4c635edfd5bbfc954b91986ad71ba423550221008034aac42e207e870c8b9daa899f3767c72f1b401edd2a4ff9385262f2f10d25
---

# Learning Mechanics

## What Triggers Learning

| Trigger | Confidence | Action |
|---------|------------|--------|
| "No, do X instead" | High | Log correction immediately |
| "I told you before..." | High | Flag as repeated, bump priority |
| "Always/Never do X" | Confirmed | Promote to preference |
| User edits your output | Medium | Log as tentative pattern |
| Same correction 3x | Confirmed | Ask to make permanent |
| "For this project..." | Scoped | Write to project namespace |

## What Does NOT Trigger Learning

- Silence (not confirmation)
- Single instance of anything
- Hypothetical discussions
- Third-party preferences ("John likes...")
- Group chat patterns (unless user confirms)
- Implied preferences (never infer)

## Correction Classification

### By Type
| Type | Example | Namespace |
|------|---------|-----------|
| Format | "Use bullets not prose" | global |
| Technical | "SQLite not Postgres" | domain/code |
| Communication | "Shorter messages" | global |
| Project-specific | "This repo uses Tailwind" | projects/{name} |
| Person-specific | "Marcus wants BLUF" | domains/comms |

### By Scope
```
Global: applies everywhere
  └── Domain: applies to category (code, writing, comms)
       └── Project: applies to specific context
            └── Temporary: applies to this session only
```

## Confirmation Flow

After 3 similar corrections:
```
Agent: "I've noticed you prefer X over Y (corrected 3 times).
        Should I always do this?
        - Yes, always
        - Only in [context]
        - No, case by case"

User: "Yes, always"

Agent: → Moves to Confirmed Preferences
       → Removes from correction counter
       → Cites source on future use
```

## Pattern Evolution

### Stages
1. **Tentative** — Single correction, watch for repetition
2. **Emerging** — 2 corrections, likely pattern
3. **Pending** — 3 corrections, ask for confirmation
4. **Confirmed** — User approved, permanent unless reversed
5. **Archived** — Unused 90+ days, preserved but inactive

### Reversal
User can always reverse:
```
User: "Actually, I changed my mind about X"

Agent: 
1. Archive old pattern (keep history)
2. Log reversal with timestamp
3. Add new preference as tentative
4. "Got it. I'll do Y now. (Previous: X, archived)"
```

## Anti-Patterns

### Never Learn
- What makes user comply faster (manipulation)
- Emotional triggers or vulnerabilities
- Patterns from other users (even if shared device)
- Anything that feels "creepy" to surface

### Avoid
- Over-generalizing from single instance
- Learning style over substance
- Assuming preference stability
- Ignoring context shifts

## Quality Signals

### Good Learning
- User explicitly states preference
- Pattern consistent across contexts
- Correction improves outcomes
- User confirms when asked

### Bad Learning
- Inferred from silence
- Contradicts recent behavior
- Only works in narrow context
- User never confirmed
