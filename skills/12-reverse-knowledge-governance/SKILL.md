---
name: reverse-knowledge-governance
description: Governs reverse-engineering experience memory. Captures useful lessons, wrong measures, shortest paths, applicability guards, promotion/demotion, expiry, and anti-hallucination controls.
metadata:
  short-description: Evidence-governed reverse knowledge memory
---

# Reverse Knowledge Governance

Use this skill when a finding might become reusable experience.

## Core principle

Experience is a prior, not proof. Memory must accelerate future search without binding the agent to false patterns.

## Knowledge stores

- `KNOWLEDGE_CANDIDATES.md`: untrusted candidate lessons.
- `KNOWLEDGE_BASE.yaml`: promoted reusable patterns.
- `NEGATIVE_LESSONS.yaml`: measures proven wrong under specific conditions.
- `SHORTCUTS.yaml`: shortest paths with strict preconditions.

## Evidence-based promotion ladder

| Tier | Meaning | May influence |
|---|---|---|
| K0 | Candidate lesson from one run or analyst intuition | Hypothesis only. Never auto-apply. |
| K1 | Single target/version proven with evidence | Project prior. Must check applicability. |
| K2 | Repeated across 2+ versions or closely related targets | Strong project-family prior. |
| K3 | Repeated across different target families or supported by authoritative source | General prior. |
| K4 | Tool/platform invariant from official docs or formal specification | General rule, still bounded by version/tool applicability. |

No lesson can exceed K1 without multiple evidence IDs or an authoritative source.

## Required fields for any lesson

```yaml
id:
title:
tier: K0|K1|K2|K3|K4
status: candidate|active|deprecated|contradicted
situation:
preconditions:
shortest_path:
incorrect_measures:
why_incorrect:
evidence_ids:
validated_on:
not_applicable_when:
kill_conditions:
contradictions:
last_reviewed:
expiry:
owner_notes:
```

## Candidate lesson rules

Write a candidate when:

- A repeated failure pattern was explained.
- A shorter path was discovered.
- A tempting action was proven wrong.
- A stable anchor was validated.
- A platform/tool behavior caused misleading evidence.

Do not write a candidate when:

- It is only a model guess.
- It lacks evidence IDs.
- It is target-specific but no target scope is recorded.
- It merely restates a standard workflow without new applicability detail.

## Promotion rules

Promote only after:

1. Evidence IDs exist and are auditable.
2. Preconditions are explicit.
3. At least one counterexample or `not_applicable_when` is written.
4. A kill condition exists.
5. A human or later run confirms it did not overfit one case.

## Demotion and expiry

Demote or deprecate when:

- A contradiction appears.
- It causes a wrong early conclusion.
- Tool/platform versions changed.
- It has not been validated for the expiry window.
- It lacks evidence after cleanup.

Expired lessons return to hypothesis status, not deletion. Delete only obvious duplicates or unsafe hallucinations.

## Anti-self-binding rules

- Load only lessons whose preconditions match the current target.
- Never use a lesson to skip live evidence when the cost of checking is low.
- Never let a shortcut bypass baseline preservation, source-of-truth proof, or validation.
- Every shortcut must say when not to use it.
- Negative lessons are scoped; do not universalize them.

## Maintenance rule

Prefer refactoring over appending. Merge duplicates, replace weak lessons with stronger ones, and delete obsolete wording after preserving evidence references.

## Output standard

```text
Candidate/promoted/deprecated lesson:
Tier:
Evidence IDs:
Applicability:
Not applicable when:
Future shortcut or warning:
State file updated:
```
