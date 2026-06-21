---
name: reverse-anchor-validation
description: Validates semantic anchors before proof, hook migration, or patching. Prevents false anchors caused by obfuscated names, hook-loaded messages, UI paths, or downstream display logic.
metadata:
  short-description: Prove stable reverse anchors
---

# Reverse Anchor Validation

Use this skill when a candidate function, method, field, branch, packet, file offset, database field, resource, or object flow might control the target behavior.

## Anchor definition

A stable anchor is a semantic control point that remains meaningful across obfuscation, versions, or execution contexts. Prefer:

- Constructors and factory methods.
- Public wrappers that invoke original business logic.
- Validators and guard branches.
- Parser/load/save boundaries.
- Network submitters and response processors.
- Native/JNI bridge boundaries.
- Source-of-truth state writes.
- Error or forced-exit wrappers plus their callers.

## Anti-false-anchor rules

Not enough by themselves:

- Name resemblance.
- One string near a function.
- Decompiled pseudocode shape.
- UI value changed.
- Hook loaded.
- A function executed once without observed state effect.
- Old-version anchor mapping by obfuscated name.

## Anchor proof ladder

| Level | Requirement | Status |
|---|---|---|
| A0 | Static candidate only | candidate |
| A1 | Runtime hit under target scenario | observed |
| A2 | Inputs/outputs/branch condition match target behavior | likely |
| A3 | Caller/context and source-of-truth state effect proven | proven |
| A4 | Stable across restart/adjacent flow/version or independent tool | stable |

Patch/hook behavior only at A3+. Use A4 for reusable migration anchors.

## Validation workflow

1. Write the candidate anchor and why it matters.
2. Identify the expected side effect.
3. Prove runtime execution in the target scenario.
4. Log inputs, outputs, branch outcome, caller, and resulting state.
5. Check whether the anchor is upstream of UI/rendering.
6. Check whether native/server/persistence later overrides the state.
7. Record in `ANCHORS.tsv`.

## Migration-specific anchor rule

When migrating across versions, match by responsibility, call shape, constants, field access patterns, caller/callee relationships, and side effects. Do not rely on exact obfuscated names.

## Output standard

```text
Anchor ID:
Semantic role:
Static evidence:
Runtime evidence:
Side effect:
Proof level A0-A4:
Version stability:
Patch/hook eligible? yes/no:
```
