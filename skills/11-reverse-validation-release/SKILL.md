---
name: reverse-validation-release
description: Real-behavior validation and release hygiene for reverse-engineering patches, hooks, migrations, and protocol/file fixes.
metadata:
  short-description: Reverse validation and release
---

# Reverse Validation and Release

Use this skill after behavior is changed, a patch/hook is migrated, or a final claim is needed.

## Principle

"Looks correct" is not enough. Validate the real source-of-truth state and adjacent flows.

## Validation matrix

Choose relevant tests:

| Category | Examples |
|---|---|
| Original scenario | The exact action that failed before now succeeds. |
| Negative control | A condition expected to fail still fails. |
| Adjacent transitions | Back, retry, repeated use, resume, restart, new session. |
| Persistence | Save/load/export/import/database/cache values. |
| UI vs state | Detail view, stats, logs, database, network object agree. |
| Network/server | Request/response, server object, retry/offline behavior. |
| Native/JNI | No crash, correct ABI, correct memory ownership. |
| Environment | Device/profile/account/path/timezone/locale variation when relevant. |
| Regression | Unrelated core paths unaffected. |
| Cleanup | Temporary diagnostics removed or disabled by default. |

## Release hygiene

- Preserve original artifact.
- Keep a single active working copy.
- Remove stale decode/build/dump/log artifacts after summarizing durable findings.
- Ensure temporary logs are gated by config and off by default.
- Record exact build/signing/install/test commands.
- Update `RE_STATE.md`, `BUILD_LEDGER.md`, and `EVIDENCE_LEDGER.md`.

## Validation result levels

| Level | Meaning |
|---|---|
| V0 | Not validated. |
| V1 | One scenario works. |
| V2 | Original scenario plus adjacent flow works. |
| V3 | Persistence/state/network verified. |
| V4 | Regression and repeatability validated. |

Promote a patch/hook/migration to reusable status only at V3+.

## Output standard

```text
Validation level V0-V4:
Scenarios tested:
Evidence IDs:
Failures or unknowns:
Temporary artifacts removed:
Final state:
```
