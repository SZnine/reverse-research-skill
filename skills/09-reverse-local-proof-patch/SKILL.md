---
name: reverse-local-proof-patch
description: Evidence-driven local proof, minimal patching, hook design, and controlled validation once a source-of-truth path is sufficiently proven.
metadata:
  short-description: Local proof and minimal patch
---

# Reverse Local Proof and Patch

Use this skill only after recon/frontier/anchor validation has identified a likely source-of-truth path.

## Core chain

```text
symptom -> observation -> candidate code/data path -> trigger condition -> proof -> minimal intervention -> validation
```

## Entry requirements

- Objective and success condition are explicit.
- Candidate anchor is A2+; patch requires A3+ unless this is an exploratory runtime-only mutation with rollback.
- Evidence IDs exist for the failing scenario.
- Competing hypotheses are either eliminated or explicitly lower priority.
- Cost gate is satisfied for rebuilds or persistent mutation.

## Patch design rules

1. Patch the earliest stable source of truth, not downstream UI/rendering.
2. Prefer calling original factory/wrapper paths with altered inputs over manual object reconstruction.
3. Preserve original side effects unless intentionally changing them.
4. Keep one feature group per patch build, but instrumentation builds may batch observations.
5. Make changes reversible and easy to diff.
6. Avoid hardcoding constants from a single sample unless code proves invariance.
7. Avoid permanent identity/device/profile rewrites unless persistence mutation is the explicit objective.
8. Do not fake server state locally if the server later rejects or overwrites it; validate object flow.
9. Remove temporary diagnostics before final release build.

## Hook design rules

- Verify process/class-loader/timing/overload before changing hook logic.
- Wrap original code when possible.
- Log inputs, outputs, and exceptions with stage labels.
- Keep config switches to enable/disable diagnostics.
- Avoid reconstructing complex runtime objects manually unless constructors/factories are proven unsafe or inaccessible.

## Patch plan template

```text
Target behavior:
Source-of-truth evidence:
Patch location:
Patch mechanism:
Expected state change:
Expected UI/behavior change:
Rollback:
Failure modes:
Validation tests:
```

## Validation minimum

- Original failing scenario now succeeds.
- Adjacent behavior still works.
- Restart/resume/save/load still works when relevant.
- Persisted state matches UI when relevant.
- Network/server state matches local state when relevant.
- Negative control still fails or remains unchanged when expected.

## Output standard

```text
Patch/hook decision:
Evidence chain:
Exact intervention:
Why this is source-of-truth:
Validation result:
Remaining risks:
State updates:
```
