---
name: platform-protocol-fileformat
description: Reverse-engineering specialization for file formats, save games, archives, serialized blobs, protocols, paired resources, checksums, compression, crypto, and import/export compatibility.
metadata:
  short-description: Protocol and file-format reverse module
---

# Platform: Protocol and File-format Reverse Engineering

Use this skill for save files, custom archives, network protocols, serialized blobs, import/export compatibility, paired resource files, checksums, compression, encryption, and schema inference.

## Layer model

Separate evidence by layer:

1. Discovery: file exists, path, slot/item selected, size, visible metadata.
2. Container/header: magic, version, lengths, flags, identity fields, locale/name fields.
3. Decode: compression, encryption, checksum, MAC/hash, derived key/password.
4. Companion resources: paired database/blob/resource exists and opens with derived credentials.
5. Body/schema: records, fields, offsets, variable-length structures, repeated sections.
6. Business validation: loader/parser return enum, exception, state transition, identity/device/profile rules.
7. Persistence/export: re-save/re-export can be consumed by downstream environment.
8. Cross-host compatibility: original host/app/version can still read the output when required.

## Workflow

1. Collect multiple samples with controlled differences.
2. Diff samples before assuming fixed offsets.
3. Identify variable fields: names, locale strings, timestamps, IDs, version labels, counters.
4. Isolate header parse from body load.
5. Verify companion files and derived keys separately.
6. Trace parser return values and exceptions.
7. Validate output by round-trip import/export.

## Anti-mistake rules

- Do not hardcode a length, offset, or constant from one sample unless code proves invariance.
- Header parse success is not full load success.
- UI listing success is not business-layer import success.
- Decryption success is not schema/model construction success.
- Rewriting provenance fields can corrupt cross-device compatibility; prefer runtime compatibility or read-time proxying unless permanent mutation is the objective.
- Paired resources often fail after the primary header succeeds.

## Probe targets

- Magic/version/length/hash checks.
- Key derivation and password construction.
- Compression/encryption boundaries.
- Database/blob open result.
- Parser enums and exception branches.
- Model construction and persistence writes.
- Export/re-import paths.

## Output standard

```text
Artifact/protocol identity:
Layer status:
Variable vs invariant fields:
Decode/body/business/persistence evidence:
Round-trip result:
Next probe:
```
