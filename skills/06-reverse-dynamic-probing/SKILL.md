---
name: reverse-dynamic-probing
description: Runtime observation and bounded instrumentation for reverse engineering. Uses logs, hooks, traces, breakpoints, file/network observation, and differential behavior before patching.
metadata:
  short-description: Runtime probes before patching
---

# Reverse Dynamic Probing

Use this skill when runtime truth is required.

## Goal

Observe actual execution and state transitions without changing behavior unless the probe explicitly requires controlled mutation.

## Probe hierarchy

Prefer lower-cost probes first:

1. Existing logs, crash stacks, tombstones, event logs.
2. Process/module/class-loader/thread inspection.
3. Narrow method/function hooks that log inputs, outputs, exceptions, and callers.
4. Breakpoints and watchpoints.
5. File/database/network observation.
6. Method tracing or execution tracing with filters.
7. Native/JNI tracing.
8. Instruction-level tracing only when justified.
9. Behavior-changing runtime patch only after observation proves the path.

## Runtime context verification

Before trusting a hook or breakpoint, verify:

- Correct process and PID.
- Correct architecture/ABI.
- Correct class loader/module instance.
- Correct method overload/signature/calling convention.
- Correct timing: class/module loaded and path executed.
- Correct thread/context when state is thread-local.
- Correct environment/account/profile/device state.

## Bounded probing rules

- Every probe must have an expected observation and kill condition.
- Logs must be stage-labeled and filterable.
- Broad tracing must be time-bounded, path-bounded, or trigger-bounded.
- Stop broad tracing once it identifies a smaller branch, field, or function to validate.
- Do not turn a probe into a permanent patch.

## High-signal probe targets

- Constructors/factories/public wrappers.
- Validators/guards/return enums.
- Save/load/database open/write paths.
- Network request construction and response parsing.
- Native bridge boundaries.
- Crypto/checksum/compression boundaries.
- Error/exception paths and forced exits.
- UI boundary callbacks followed by business-layer returns.

## Dynamic proof levels

- Hook hit: proves path executed only under observed context.
- Input/output log: proves data shape and branch conditions.
- Caller stack: proves call chain.
- State mutation: proves source-of-truth effect.
- Repeat after restart/adjacent flow: supports durable validation.

## Output standard

```text
Probe ID:
Hypothesis:
Runtime context verified:
Expected observation:
Actual observation:
Evidence level:
Hypotheses eliminated:
Next narrower probe or handoff:
```
