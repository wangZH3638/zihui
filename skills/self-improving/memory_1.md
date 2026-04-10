---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100c26913fbc3a3eb722718b299d40e6c795703294b685a997b123150670f25d548022100e65b32bc2cac9846ed08763726ca1f4cf434c3928c60c82927862db0efa3f2ea
    ReservedCode2: 3045022100805b751d9f47edf6ac7b7fea3a4f699bfd489bfbb3a748704ef5fe7245a7e54b02203c5aeed0d5c9673d1a659f349a179e977196fa65e7df1b2804b9e3b1871d64ec
---

# HOT Memory — Template

> This file is created in `~/self-improving/memory.md` when you first use the skill.
> Keep it ≤100 lines. Most-used patterns live here.

## Example Entries

```markdown
## Preferences
- Code style: Prefer explicit over implicit
- Communication: Direct, no fluff
- Time zone: Europe/Madrid

## Patterns (promoted from corrections)
- Always use TypeScript strict mode
- Prefer pnpm over npm
- Format: ISO 8601 for dates

## Project defaults
- Tests: Jest with coverage >80%
- Commits: Conventional commits format
```

## Usage

The agent will:
1. Load this file on every session
2. Add entries when patterns are used 3x in 7 days
3. Demote unused entries to WARM after 30 days
4. Never exceed 100 lines (compacts automatically)
