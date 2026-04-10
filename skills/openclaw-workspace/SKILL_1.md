---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: ebf3b130395906b74f13c82205a773d4
    PropagateID: ebf3b130395906b74f13c82205a773d4
    ReservedCode1: 3045022100992b03446a7c22604a3150b4904d5e831de1a6cc0ecdad890401fcc68120c65e0220099bb50599f4de7c64df52b8c7bc18df0ecd287ea277c380f3155f6818a4eae7
    ReservedCode2: 30450220605bfc1c800e217e6794413edcc479a8591cb04bcdf16cde1c43092b534c527b02210089057ff1b2375839b9d92c0e2963a97c11aebf9fa67fb0bff7781e168edf239c
description: Use when maintaining or optimizing OpenClaw workspace files — AGENTS.md, TOOLS.md, SOUL.md, USER.md, IDENTITY.md, HEARTBEAT.md, BOOT.md, MEMORY.md, and related checklists and memory files. Covers workspace auditing, token budget analysis, new agent workspace setup from scratch, memory distillation, and cross-file consistency reviews.
name: openclaw-workspace
---

# OpenClaw Workspace Skill

## Overview

OpenClaw workspace files form the agent's "soul and memory" — they are injected into the system prompt on every turn (or on relevant turns), giving the agent its identity, behavioral rules, environmental knowledge, and long-term memory. Managing these files well is critical: bloat wastes tokens, redundancy creates confusion, and stale content leads to bad decisions.

**Token budget:** 20,000 chars per file, ~150,000 chars total across all bootstrap files.

## File Inventory

| File | Purpose | Loaded When | Sub-agents? |
|------|---------|-------------|-------------|
| `AGENTS.md` | Boot sequence, checklists, behavioral rules | Every turn (all agents) | Yes |
| `SOUL.md` | Persona, tone, values, continuity philosophy | Every turn (all agents) | Yes |
| `TOOLS.md` | Env-specific notes (SSH, TTS, cameras, devices) | On-demand reference (part of bootstrap set) | Yes |
| `USER.md` | Human profile, preferences, relationship context | Every turn (all agents) | Yes |
| `IDENTITY.md` | Name, emoji, avatar, self-description | Every turn | Yes |
| `HEARTBEAT.md` | Periodic check tasks and health routines | Every heartbeat turn | Depends |
| `BOOT.md` | Startup actions (requires `hooks.internal.enabled`) | On gateway startup | No |
| `BOOTSTRAP.md` | First-time onboarding script — delete after use | New workspaces only | No |
| `MEMORY.md` | Long-term curated facts and iron-law rules | Main sessions only | No |
| `memory/YYYY-MM-DD.md` | Daily session logs | Loaded per AGENTS.md boot sequence | No |
| `checklists/*.md` | Step-by-step ops guides | Referenced in AGENTS.md, loaded on demand | No |

**Security rule:** MEMORY.md must NEVER be loaded in group chats or sub-agent sessions — it contains private context that should not leak.

## Workspace Paths

| Path | Purpose |
|------|---------|
| `~/.openclaw/workspace/` | Default workspace for main agent |
| `~/.openclaw/workspace-<profile>/` | Per-profile workspace (multiple agents) |
| `~/.openclaw/workspace/vendor/OpenClaw-Memory/` | Vendor-managed base files |
| `~/.openclaw/workspace/checklists/` | Checklist files referenced from AGENTS.md |
| `~/.openclaw/workspace/memory/` | Daily session logs |
| `~/.openclaw/workspace/docs/` | On-demand documentation (NOT auto-loaded) |

## Workflow: Audit Existing Workspace

Use when workspace files may be bloated, stale, or redundant.

1. **Read all active files** — AGENTS.md, SOUL.md, TOOLS.md, USER.md, IDENTITY.md, HEARTBEAT.md, BOOT.md, MEMORY.md
2. **Check character counts:**
   ```bash
   wc -c ~/.openclaw/workspace/*.md
   ```
3. **Flag files over 10,000 chars** — prime candidates for trimming or offloading to `docs/`
4. **Check for redundancy** — same fact in SOUL.md and AGENTS.md? Same tool note in TOOLS.md and MEMORY.md?
5. **Check for staleness** — outdated SSH hosts, old tool names, deprecated rules
6. **Check MEMORY.md discipline** — should contain curated facts, lessons learned, decisions — not raw session summaries

## Workflow: Set Up New Workspace

**File creation order:**

1. `SOUL.md` — persona and values first
2. `AGENTS.md` — boot sequence, safety rules, checklist table
3. `IDENTITY.md` — name, emoji, avatar
4. `USER.md` — human profile and preferences (main agent only)
5. `TOOLS.md` — environment-specific notes
6. `MEMORY.md` — start minimal; only truly universal iron laws
7. `HEARTBEAT.md` — periodic health checks (optional)
8. `BOOT.md` — startup hooks (optional)
9. `BOOTSTRAP.md` — first-run onboarding (delete after use)

**Minimal viable workspace:** AGENTS.md + SOUL.md + TOOLS.md

## Workflow: Memory Distillation

1. Read recent `memory/YYYY-MM-DD.md` files
2. Identify candidates for promotion to MEMORY.md
3. Promote recurring mistakes and hard-won rules to iron-law format
4. Archive or delete old logs
5. Consider moving mature rules to skill `SKILL.md` files

## Common Issues

### File exceeds token limit (> 20,000 chars)
Move content to `docs/` (loaded on demand). Keep only what needs to be in context every turn.

### MEMORY.md leaking to group chats
Add explicit gating in AGENTS.md: "Main session only: Read MEMORY.md"

### BOOTSTRAP.md still exists
Delete it after first successful startup.

### Workspace changes not taking effect
Start a new session or restart the gateway for changes to apply.
