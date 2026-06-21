---
name: reverse-static-cartography
description: Static mapping for binaries, APKs, native libraries, resources, protocols, and version comparisons. Builds a cartography before runtime probing or patching.
metadata:
  short-description: Static reverse cartography
---

# Reverse Static Cartography

Use this skill to build a map without executing the target.

## Goal

Produce a structured map of code, data, resources, entry points, references, dependencies, and candidate anchors. Static cartography is not proof of runtime behavior; it produces hypotheses and probe targets.

## Generic workflow

1. Identify artifact format, architecture, build type, hash, size, timestamp, packing/obfuscation hints.
2. Inventory entry points, exports, imports, symbols, sections, resources, manifests, permissions, endpoints, schemas, and native libraries.
3. Extract strings and classify by purpose: UI, logs, URLs, file paths, crypto, errors, feature names, protocol constants.
4. Build xrefs/call graph around relevant strings, imports, validators, constructors, factories, parsers, persistence, and network submitters.
5. Locate candidate source-of-truth paths.
6. Record decompiler uncertainty and places requiring dynamic proof.
7. Write candidate anchors to `ANCHORS.tsv` with status `candidate`.

## Map outputs

- Entry-point map.
- Component/resource map.
- Data-flow map around target behavior.
- Candidate anchor list.
- Static dead ends.
- Dynamic probe plan.

## Evidence discipline

Static facts are usually E1. They become E2+ only when runtime execution or state effects are observed.

## Pitfalls

- Decompilers can be wrong or incomplete.
- Obfuscated names are not semantic anchors.
- Dead code and anti-analysis decoys can be convincing.
- Resource names and UI strings may be misleading.
- Decompiled Java/Kotlin may omit native behavior, reflection, dynamic loading, or generated dispatch.
- Constants from one sample may be variable across locale, version, identity, or metadata.

## Android APK notes

Use the Android platform skill for APK-specific details. Static APK cartography should include:

- Manifest components and permissions.
- APK signature/certificate metadata.
- DEX/class inventory.
- Resources/assets/configs.
- Native libraries and ABI list.
- Dynamic loading and reflection indicators.
- Network security config, endpoints, WebView usage.
- Persistence schemas and save/archive formats.

## Native binary notes

Use the native platform skill for ELF/PE/Mach-O details. Static native cartography should include:

- Imports/exports/symbols/relocations.
- Cross references to APIs and strings.
- Function graph and call tree around the target.
- Type recovery opportunities.
- Crypto/compression/parser loops.
- Syscall and JNI boundaries.

## Output standard

```text
Artifact identity:
Static map summary:
Candidate anchors:
Static evidence IDs:
Untrusted decompiler assumptions:
Recommended dynamic probes:
```
