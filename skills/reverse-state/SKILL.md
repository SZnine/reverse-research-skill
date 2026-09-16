---
name: reverse-state
description: "Manage state for long or staged reverse work. Use when probes create scratch logs/builds/test packages, work must resume after handoff, or a milestone was reached. Keeps a compact working state, promotes only valuable proof or deliverables, and removes unpromoted stage artifacts by default. Not for one-off inspection."
metadata:
  version: "5.0"
  role: "state-and-retention"
  compatibility: Python 3.10+ for the optional deterministic state helper.
---

# Reverse State and Workspace Metabolism

## Minimal workspace

Use one project-local `.reverse/` directory:

```text
.reverse/
  STATE.md                 current objective, confirmed facts, blocker, next action
  checkpoints/             short milestone records
  stages/                  disposable output, one directory per active probe/build/test
  proof/                   promoted support for durable claims
  deliverables/            user-facing final artifacts
  original/                preserved targets only when mutation or source loss is possible
  LESSONS.json              concrete, deduplicated reusable lessons
```

Initialize only when the task warrants durable state:

```bash
python <skill_dir>/scripts/state.py init --workspace . --objective "<question>" [--target <path>]
```

## Stage lifecycle

Put all temporary output for one probe, build, or test under a stage directory. At a meaningful success, abandonment, or strategy change:

1. Distill the observation, decision, limitations, reproducible recipe, and next action into one short checkpoint; link raw output instead of pasting it.
2. Promote an artifact only when it is a final deliverable, is needed for rollback/regression, is expensive or impossible to reproduce, or materially supports a durable claim.
3. Delete the remaining stage by default after `success` or `abandoned`.
4. Keep a `blocked` stage only while its contents are needed to resume.

Do not archive by default. Snapshot only when the risk of losing non-reproducible work exceeds the storage and attention cost.

Test APKs, debug binaries, broad traces, screenshots, and failed build trees are ephemeral by default. A possible future use is not enough to retain them. For cheaply reproducible artifacts, keep the recipe and result rather than the artifact.

Use the helper when useful:

```bash
python <skill_dir>/scripts/state.py stage --workspace . --name "<probe>"
python <skill_dir>/scripts/state.py checkpoint --workspace . --stage <id> \
  --status success --summary "<observation>" --decision "<what changed>" \
  --next "<next action>" --recipe "<reproduction command>" \
  [--promote path:proof] [--promote path:deliverable]
```

## State and lessons

`STATE.md` is a working pointer, not a history dump. Replace stale detail with the latest decision and link to checkpoints.

Create a lesson only when it is likely to change a future investigation. Keep it concrete:

```text
When: matching situation and preconditions
Signal: observation that identifies it
Do: shortest useful action
Boundary: when this advice stops applying
Basis: checkpoint or target/version
```

Merge duplicates and strengthen boundaries instead of appending variants. Do not record generic advice, ceremonial summaries, a restatement of a checkpoint, or a lesson for every stage.

Read `references/RETENTION_EXAMPLES.md` when promotion is ambiguous.
