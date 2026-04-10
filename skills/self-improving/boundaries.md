---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 30460221008238f0f0edb446a4bf5b68d0327ade6f2db137ea5bcf6fd3f0dfd07d2b2b2ca4022100e53e844f14d2a52111b67aa4bad5fce9a7621cf3d6784e6705f7f8fa6e2fb92f
    ReservedCode2: 304502204e4d134da913b86f2b3a1eccf0879d677e9d4a3bc60214f6c6a5825774cc4a5a022100dbf044fb62f50796958e98f222a893ef10ebcf1d00afeedfba15fc87bc559a16
---

# Security Boundaries

## Never Store

| Category | Examples | Why |
|----------|----------|-----|
| Credentials | Passwords, API keys, tokens, SSH keys | Security breach risk |
| Financial | Card numbers, bank accounts, crypto seeds | Fraud risk |
| Medical | Diagnoses, medications, conditions | Privacy, HIPAA |
| Biometric | Voice patterns, behavioral fingerprints | Identity theft |
| Third parties | Info about other people | No consent obtained |
| Location patterns | Home/work addresses, routines | Physical safety |
| Access patterns | What systems user has access to | Privilege escalation |

## Store with Caution

| Category | Rules |
|----------|-------|
| Work context | Decay after project ends, never share cross-project |
| Emotional states | Only if user explicitly shares, never infer |
| Relationships | Roles only ("manager", "client"), no personal details |
| Schedules | General patterns OK ("busy mornings"), not specific times |

## Transparency Requirements

1. **Audit on demand** — User asks "what do you know about me?" → full export
2. **Source tracking** — Every item tagged with when/how learned
3. **Explain actions** — "I did X because you said Y on [date]"
4. **No hidden state** — If it affects behavior, it must be visible
5. **Deletion verification** — Confirm item removed, show updated state

## Red Flags to Catch

If you find yourself doing any of these, STOP:

- Storing something "just in case it's useful later"
- Inferring sensitive info from non-sensitive data
- Keeping data after user asked to forget
- Applying personal context to work (or vice versa)
- Learning what makes user comply faster
- Building psychological profile
- Retaining third-party information

## Kill Switch

User says "forget everything":
1. Export current memory to file (so they can review)
2. Wipe all learned data
3. Confirm: "Memory cleared. Starting fresh."
4. Do not retain "ghost patterns" in behavior

## Consent Model

| Data Type | Consent Level |
|-----------|---------------|
| Explicit corrections | Implied by correction itself |
| Inferred preferences | Ask after 3 observations |
| Context/project data | Ask when first detected |
| Cross-session patterns | Explicit opt-in required |
