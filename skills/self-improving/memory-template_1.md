---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3045022100aadf03203e4a802d13a1e0d9a160357ab1ce10c3e2ab515f04ed2fc457aef38f02203900a542fffd3243b36ad40568d527fe419086408c3850e5fb9e544f91a507aa
    ReservedCode2: 304502200e243aa01a06aa395efa30c023770c658c56a011736965e0c31c4f16083d4e57022100f8d3dbacb466b9190bcc24b78c6427c2f1067f22465aa019f12907031f83e1df
---

# Memory Template

Copy this structure to `~/self-improving/memory.md` on first use.

```markdown
# Self-Improving Memory

## Confirmed Preferences
<!-- Patterns confirmed by user, never decay -->

## Active Patterns
<!-- Patterns observed 3+ times, subject to decay -->

## Recent (last 7 days)
<!-- New corrections pending confirmation -->
```

## Initial Directory Structure

Create on first activation:

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
touch ~/self-improving/{memory.md,index.md,corrections.md}
```

## Index Template

For `~/self-improving/index.md`:

```markdown
# Memory Index

## HOT
- memory.md: 0 lines

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last compaction: never
```

## Corrections Log Template

For `~/self-improving/corrections.md`:

```markdown
# Corrections Log

<!-- Format:
## YYYY-MM-DD
- [HH:MM] Changed X → Y
  Type: format|technical|communication|project
  Context: where correction happened
  Confirmed: pending (N/3) | yes | no
-->
```
