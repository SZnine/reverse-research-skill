# Upgrade From Existing Reverse Skills

The previous compact reverse workflow is strong for evidence chains, layer isolation, minimal patching, and validation. In this package it is preserved mainly in:

- `02-reverse-state-evidence`
- `07-reverse-anchor-validation`
- `09-reverse-local-proof-patch`
- `11-reverse-validation-release`

The key change is that these are no longer the entry point for hard targets. The entry point is now `00-reverse-research-orchestrator`, which decides whether to use quick triage, black-box recon, frontier management, cost gating, local proof, migration, or knowledge governance.

## What changed

| Old behavior | New behavior |
|---|---|
| Local symptom quickly leads to local instrumentation or patch | Mechanism-unknown work enters black-box recon and hypothesis frontier first |
| Rebuilds may happen after one suspicious local conclusion | Rebuilds are cost-gated and must cover multiple hypotheses unless baseline/blocker/proven patch |
| Project-specific notes can bias future runs | Knowledge is tiered, evidence-bound, scoped, expiring, and treated as prior only |
| Migration follows old anchors by default | Old anchors are priors; two failed anchors trigger recon |
| Simple tasks can be over-processed | R0 quick triage exists and avoids full frontier/state overhead |

## How to migrate an existing project

1. Copy templates into the project `notes/` directory.
2. Convert current facts into `RE_STATE.md` with evidence IDs.
3. Move old stable anchors into `ANCHORS.tsv` with proof levels.
4. Move old repeated lessons into `KNOWLEDGE_CANDIDATES.md`, not directly into `KNOWLEDGE_BASE.yaml`.
5. Promote lessons only after filling evidence, applicability, not-applicable cases, and kill conditions.
6. Route future tasks through `00-reverse-research-orchestrator`.

## What not to carry over

- Chronological logs without reusable lessons.
- Single-sample constants treated as invariants.
- Old obfuscated names without semantic proof.
- Successful UI screenshots without persistence/business-layer validation.
- Build steps that are not tied to evidence or eliminated hypotheses.
