---
name: platform-native-binary
description: Native binary reverse-engineering specialization for ELF, PE, Mach-O, shared libraries, firmware blobs, JNI libraries, and low-level protocol/parser/crypto code. Use with the reverse-research orchestrator.
metadata:
  short-description: Native binary reverse platform module
---

# Platform: Native Binary Reverse Engineering

Use this skill for ELF, PE, Mach-O, shared libraries, JNI libraries, firmware blobs, native protections, parsers, crypto/compression, and low-level control flow.

## Native layer map

1. Format: ELF/PE/Mach-O/raw/firmware/container.
2. Architecture/ABI/endian/compiler/runtime.
3. Sections/segments/permissions/entropy/packing.
4. Imports/exports/symbols/relocations.
5. Strings, constants, error messages, paths, URLs, protocol markers.
6. Call graph, function graph, xrefs, data references.
7. Entry points, constructors, init arrays, TLS callbacks, JNI exports.
8. Syscalls, file/network/process/thread APIs.
9. Crypto/compression/checksum/parser loops.
10. Anti-debug/anti-tamper/integrity checks.
11. Memory ownership, allocator boundaries, object lifetimes.
12. Dynamic runtime behavior under debugger/instrumentation.

## Static workflow

- Identify format, arch, and dependencies.
- Generate strings/imports/exports/xrefs.
- Use decompiler output as a guide, not proof.
- Build call tree around target strings/APIs/guards/parsers.
- Recover structs/types incrementally.
- Mark unknown calling conventions and suspicious decompiler artifacts.
- Record candidate anchors in `ANCHORS.tsv`.

## Dynamic workflow

- Verify exact loaded module and base address.
- Use debugger or instrumentation to confirm path execution.
- Log inputs/outputs/caller and memory state at function boundaries.
- Use watchpoints for source-of-truth writes.
- Use tracing only with filters and kill conditions.
- Consider emulation/symbolic execution only when it can target a specific branch or parser condition.

## Patch rules

- Do not patch a conditional branch without understanding caller context and side effects.
- Prefer input shaping or wrapper-level hooks over raw instruction patch when possible.
- Preserve calling conventions, stack alignment, register clobbers, and memory ownership.
- Validate across repeated runs and negative controls.

## JNI-specific notes

- Java-side success does not prove native-side success.
- JNI method registration may be static or dynamic.
- Anchor both Java bridge and native implementation when behavior crosses the boundary.
- Validate ABI-specific libraries separately.

## Output standard

```text
Binary identity:
Native map:
Candidate anchors:
Runtime proof:
Patch risk:
Next probe:
```
