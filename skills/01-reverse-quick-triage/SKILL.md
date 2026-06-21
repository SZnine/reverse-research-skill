---
name: reverse-quick-triage
description: Fast path for simple reverse-engineering questions and simple APK/binary checks. Prevents over-engineering by using cheap inspections and small hypothesis sets before escalating.
metadata:
  short-description: Fast reverse triage without overthinking
---

# Reverse Quick Triage

Use this skill when the target appears simple, the user asks a direct question, or the objective can likely be answered by cheap inspection.

## Use cases

- Identify package name, version, manifest components, permissions, min/target SDK.
- Explain a known build/sign/install error.
- Locate a string, resource, API usage, or obvious code path.
- Confirm whether a hook likely missed process/class-loader/timing/overload.
- Inspect one crash/log snippet.
- Compare two small snippets or two versions at a single anchor.
- Determine whether escalation to full reverse research is required.

## Minimal workflow

1. Restate the objective and expected output.
2. Inspect the smallest useful artifact first.
3. Keep at most two hypotheses unless contradictory evidence appears.
4. Prefer buildless actions: grep, strings, manifest read, existing logs, static xrefs, decompiler check, certificate/signature verification, current state files.
5. Produce either a direct answer or an escalation reason.

## Anti-overthinking rules

- Do not create full `FRONTIER.md` for a one-layer direct question.
- Do not propose a rebuild before checking existing evidence and cheap artifacts.
- Do not enumerate every possible protection if the error is specific and local.
- Do not run broad tracing for a simple static lookup.
- Do not promote a one-off finding into long-term knowledge; at most create a candidate lesson.

## Escalate to full orchestration when

- Two cheap inspections do not explain the issue.
- The target involves version migration, obfuscation, packing, integrity checks, JNI/native code, dynamic loading, persistence mismatch, or network/server state.
- The user is paying a high cost per test, such as APK repack/sign/install loops.
- A patch, hook, or rebuild becomes necessary.
- UI success differs from persisted/business-layer state.

## Output standard

```text
Triage result:
Evidence:
Likely explanation:
Confidence:
Next cheapest check:
Escalate? yes/no, reason:
```
