---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100aeffdf63c5ad6257da0154d661c25326fb4bbd93cdf9acb502fea602ff56dc790221009f21cbcc9aca3a8cadcac7e9a5d9d795df2f75ecb563942b36d08665b4d93ffa
    ReservedCode2: 304602210090f9354fe18263543fa37ff561e001e7a24edddd62770049aee36876a08dd187022100b9608d0c61609b594221dfaa2f31c01c94a57636d14f7340317c4ef16b68d53d
---

# Contributing / Development Conventions

## Version Management

- **SemVer**: `SKILL.md` frontmatter `version` field is the single source of truth
- **CHANGELOG.md**: reverse-chronological, update with every version bump
- Every change must update **both** `SKILL.md version` + `CHANGELOG.md` + git commit & push
- Changelog version format: `## v3.5.0` (prefixed with `v`)

## Code Conventions

- All prompts, templates, comments, and code in **English**
- Output language controlled at runtime via `LANGUAGE` variable
- Python: use `except Exception:` — never bare `except:`
- No hardcoded credentials — all secrets via environment variables
- When adding data sources, update `sources.json` schema **and** README source count

## Security

- ClawHub audit compliance: declare all `tools`/`bins`, file read/write paths, credential access in SKILL.md metadata
- No third-party untrusted RSS mirrors (supply chain risk)
- HTML email bodies written to temp files before CLI delivery
- Subjects restricted to static format strings (no injection)
- Discord embed suppression: wrap links in `<>` to prevent previews

## Debugging

- Full pipeline: `python3 scripts/run-pipeline.py --verbose --force`
- Each step generates `*.meta.json` with timing, counts, and status
- Individual scripts can be run standalone for targeted debugging

## File Structure

```
SKILL.md          — Skill metadata (version, env vars, tools, files)
CHANGELOG.md      — Version history
README.md         — English docs
README_CN.md      — Chinese docs
config/defaults/  — Default sources.json, topics.json
references/       — digest-prompt.md, output templates
scripts/          — Python pipeline scripts
```

## Environment vs Code

- **Never push environment-specific config to repo** — email sender names, API keys, file paths, channel IDs, timezone settings, etc. belong in local workspace config or env vars, not in skill code
- Repo code uses `<PLACEHOLDER>` patterns; actual values are substituted at runtime
- Local overrides go in `workspace/config/`, not in `config/defaults/`

## Git Workflow

- Commit messages: concise English, describe what changed
- Push to `main` branch on github.com/draco-agent/tech-news-digest
- No feature branches for solo development (direct to main)
