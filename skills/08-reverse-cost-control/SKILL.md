---
name: reverse-cost-control
description: Cost gates for rebuild/repack/sign/install/test, broad tracing, and other expensive reverse-engineering actions. Forces batch experiments and state updates.
metadata:
  short-description: Reverse experiment cost control
---

# Reverse Cost Control

Use this skill before any expensive action: APK rebuild, repack, re-sign, install/test cycle, Gadget injection, binary patch, broad tracing, full native trace, persistent data mutation, or long-running automated analysis.

## Principle

Expensive actions are scarce experiments. One expensive action should reduce multiple uncertainties or validate a proven source-of-truth patch.

## Cost classes

| Cost | Examples |
|---|---|
| Buildless | static grep, strings, xrefs, manifest read, existing logs, attach-only script, file inspection |
| Low | narrow hook, log filter, breakpoint, small differential sample, external Frida script |
| Medium | method tracing, native bridge tracing, emulator/device scenario setup, database diff |
| Expensive | rebuild/repack/sign/install, embedded Gadget, broad trace, instruction trace, persistent mutation, release validation |

## Allowed expensive actions

An expensive action is allowed only when at least one is true:

1. It proves a clean baseline.
2. It collects observations for at least three active hypotheses.
3. It validates a high-confidence patch whose source-of-truth path is proven.
4. It unblocks all further analysis.
5. It is the final regression/release validation.

## Disallowed actions

- Rebuilding for a single low-confidence guess.
- Patching a suspicious branch without proving runtime control.
- Re-running a baseline already recorded in `RE_STATE.md` without a changed condition.
- Adding wide noisy instrumentation without filters and kill conditions.
- Mixing unrelated behavior changes in a patch build.

## Build types

### Baseline build

Purpose: prove roundtrip build/sign/install/startup with no intended behavior change.

Required:
- Original hash.
- Work copy hash.
- Build command.
- Signing scheme/certificate state.
- Startup result.

### Instrumentation build

Purpose: collect observations without changing behavior.

Required:
- At least three hypotheses or one hard blocker.
- Stage-labeled, configurable logs.
- Expected observation per checkpoint.
- Kill condition.

### Patch build

Purpose: change behavior after proof.

Required:
- Source-of-truth proof A3+ / E3+.
- Exact diff.
- Rollback plan.
- Adjacent-flow validation plan.

### Regression build

Purpose: final validation.

Required:
- Original failing scenario.
- Positive and negative tests.
- Persistence and restart tests.
- Cleanup of temporary diagnostics.

## Required ledger entry

Update `BUILD_LEDGER.md`:

```text
build_id:
type:
changed_files:
purpose:
hypotheses covered:
expected observations:
actual observations:
hypotheses eliminated:
result:
next mode:
```

## Output standard

```text
Expensive action approved? yes/no
Reason:
Build/probe type:
Hypotheses covered:
Expected observations:
Kill condition:
State updates:
```
