# Package Manifest

## Core skills

| Skill | Role |
|---|---|
| `00-reverse-research-orchestrator` | Mandatory entry point. Classifies task mode, complexity, budget, and next module. |
| `01-reverse-quick-triage` | Prevents overthinking on simple APKs/binaries/protocols. |
| `02-reverse-state-evidence` | Defines evidence levels, state files, claim discipline, and durable notes. |
| `03-reverse-blackbox-recon` | Builds system/layer map before local proof. |
| `04-reverse-hypothesis-frontier` | Maintains hypothesis search frontier and information-gain ranking. |
| `05-reverse-static-cartography` | Static map of package, code, resources, native libs, strings, xrefs, and candidate anchors. |
| `06-reverse-dynamic-probing` | Runtime observation with bounded probes, hooks, traces, logs, and differential behavior. |
| `07-reverse-anchor-validation` | Proves that an anchor executes, controls the relevant state, and is stable enough for proof/patch. |
| `08-reverse-cost-control` | Treats rebuild/repack/sign/install/test as expensive experiments. |
| `09-reverse-local-proof-patch` | Evidence chain, minimal patch/hook, rollback, and local validation. |
| `10-reverse-migration-versioning` | Version migration by responsibility and semantic anchors; anti-anchor-fixation. |
| `11-reverse-validation-release` | Final validation across real behavior, adjacent flows, persistence, and regressions. |
| `12-reverse-knowledge-governance` | Experience capture, promotion, demotion, expiry, anti-hallucination memory controls. |

## Platform skills

| Skill | Role |
|---|---|
| `platform-android-apk` | Android APK/DEX/smali/native/Gadget/signing/repackaging specialization. |
| `platform-native-binary` | ELF/PE/Mach-O/shared-library/native-code specialization. |
| `platform-protocol-fileformat` | File format, save, archive, protocol, paired resource, checksum, crypto/compression specialization. |

## Template files

The templates are operational state files. They are intentionally plain Markdown/YAML/TSV so agents can edit them cheaply and humans can audit them.
