---
name: reverse-native
description: "Authorized native binary/library/firmware reverse analysis: architecture, imports/exports, disassembly/decompilation, ABI/calling convention, debugger/instrumentation, memory/state writes, crashes, and binary patches. Supplies native-specific probes without a fixed pipeline."
metadata:
  version: "5.0"
  role: "target-adapter"
---

# Native Binary Adapter

Use with `reverse-research`. Select only the probe family that can answer the current question.

## Probe families

- **Identity and loading:** format, architecture/endianness, hashes, segments/sections, dependencies, symbols, relocations, loader context.
- **Static responsibility map:** strings/xrefs, imports/exports, callers/callees, data references, control-flow around the decision.
- **ABI boundary:** calling convention, parameter/return representation, stack/register effects, structure layout, JNI/FFI boundary.
- **Runtime path:** correct process/module/base address, breakpoint/hook/watchpoint hit, caller context, register/memory values.
- **State ownership:** locate the write or accepted result that controls the observed behavior; distinguish cached/displayed state from durable/native truth.
- **Crash triage:** faulting instruction, exception/signal, stack integrity, lifetime/race, architecture mismatch, instrumentation side effects.
- **Patch path:** preserve original before mutation; prefer a causal runtime probe before persistent bytes; record exact offset/bytes/relocations and rollback.

Pseudocode is a navigation aid, not proof. Before patching, reconcile important semantics with disassembly, xrefs/callers, ABI, and a runtime or causal observation when feasible.

Do not install a full native suite at startup. Resolve the needed disassembler, debugger, emulator, or instrumentation capability through `reverse-toolbox` when the chosen probe requires it.

Use operator assistance for physical-device reproduction, visual/audio output, hardware state, or debugger actions inaccessible to the agent. Use `reverse-verify` for durable mechanism, crash-fix, or release claims; keep transient dumps/builds in a `reverse-state` stage.
