---
name: reverse-blackbox-recon
description: Build a system/layer map when the target mechanism is not localized. Maximizes information gain before local proof, patching, or expensive rebuilds.
metadata:
  short-description: Black-box reverse reconnaissance
---

# Reverse Black-box Recon

Use this skill when the mechanism is unknown or the agent is stuck in local trial-and-error.

## Goal

Maximize uncertainty reduction per token and per experiment. Do not patch in recon mode.

## Recon surfaces

Map the target across relevant layers:

1. Packaging/install/signing/startup.
2. Process model, entry points, lifecycle, threads.
3. Loaders, class loaders, dynamic code, plugins, scripts.
4. Resources/assets/configuration/localization.
5. Java/Kotlin/managed business logic.
6. Native/JNI/shared libraries/syscalls.
7. UI/rendering/input dispatch.
8. Persistence: files, databases, preferences, saves, caches.
9. Network/API/server object flow.
10. Crypto/compression/checksums/integrity.
11. Auth/license/anti-debug/root/emulator/tamper checks.
12. IPC/components/providers/services/broadcasts.
13. Environment/device/profile/account binding.
14. Protocol/file/archive companion resources.

## Required outputs

Create or update:

```text
RE_STATE.md: Current System Map
FRONTIER.md: Active hypotheses
PROBE_LOG.md: cheap probes and results
```

## Recon workflow

1. Define the exact behavior to explain.
2. Separate what is observed from what is inferred.
3. Identify which layers could plausibly control the behavior.
4. Mark each layer as `blind`, `partial`, `observed`, or `ruled-out`.
5. Pick probes that split the search space, not probes that merely deepen one favorite branch.
6. Prefer buildless probes first.
7. Stop recon only when a candidate source-of-truth path reaches sufficient confidence for anchor validation or local proof.

## Probe classes

### Buildless probes

- Static strings, xrefs, manifest/resources, imports/exports, certificate/signature metadata.
- Existing logs and crash/tombstone/call stack.
- Runtime attach without modifying the binary.
- Frida/LLDB/GDB/JDB scripts loaded externally.
- Network/file/process inspection.
- Differential sample comparison.

### Low-cost runtime probes

- Narrow method hooks.
- Class-loader enumeration.
- Branch input/output logging.
- Return-value observation without behavior change.
- File/database read/write observation.
- Packet/request/response observation.

### Expensive probes

- Rebuild/repack/sign/install.
- Embedded instrumentation or Gadget injection.
- Broad tracing.
- Full native trace or instruction-level trace.
- Persistent data mutation.

Expensive probes must pass `reverse-cost-control`.

## Anti-local-trap rules

- Do not spend more than two local attempts on one path unless each attempt eliminates a competing hypothesis.
- If a path explains UI but not state, return to layer isolation.
- If a path executes but does not affect behavior, it is not the source of truth.
- If an old anchor fails twice, switch from migration to recon.

## Output standard

```text
Behavior to explain:
Layer coverage matrix:
Top hypotheses:
Best next probes ranked by information gain/cost:
Dead ends and why:
Escalation condition:
```
