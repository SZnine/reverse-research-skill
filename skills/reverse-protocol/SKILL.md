---
name: reverse-protocol
description: "Authorized protocol, file-format, save-file, parser, and serializer reverse analysis. Use for sample comparison, framing/container/decode/schema/business layers, controlled corpus generation, parser instrumentation, and roundtrip validation. Avoids turning one sample into a universal rule."
metadata:
  version: "5.0"
  role: "target-adapter"
---

# Protocol and File-Format Adapter

Use with `reverse-research`. Start at the layer implicated by the question; do not require a full corpus when code or a narrow local fact already answers it.

## Probe families

- **Sample identity:** hashes, lengths, source/version/environment, known-good/known-bad labels.
- **Controlled differential:** change one semantic input at a time and compare bytes, parsed fields, or messages.
- **Framing/container:** magic, version, lengths, offsets, checksums/MACs, compression/encryption boundaries, record framing.
- **Decode boundary:** identify where opaque bytes become structured data and where validation rejects them.
- **Schema/business layer:** field hypotheses, optionality, enums, invariants, object construction, acceptance/rejection result.
- **Runtime instrumentation:** parser entry/exit, read/write offsets, decoded buffers, return codes, exceptions, caller context.
- **Roundtrip:** parse then serialize/import/export and verify the business-level result plus negative controls.

One sample supports a candidate pattern, not a stable constant, unless implementation code or a specification establishes it. Prefer a second controlled sample over prolonged speculation when the user can cheaply generate it.

Header, decompression, or decryption success proves only that layer. Match final validation to the import, parser, synchronization, or business claim through `reverse-verify`.

Use `reverse-toolbox` only for the specific hex/diff/parser/dissector capability selected. Store temporary corpora, decoded dumps, and generated test files in a `reverse-state` stage; promote only irreplaceable samples, final schemas/tools, or artifacts needed for a durable claim.
