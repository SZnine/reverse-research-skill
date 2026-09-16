---
name: reverse-verify
description: "Validate durable reverse-engineering claims and patched outputs against the claim's real oracle/source of truth. Use before saying a mechanism, migration, patch, persistence behavior, server outcome, or release artifact is successful. Do not force proof bookkeeping during ordinary exploration."
metadata:
  version: "5.0"
  role: "claim-validation"
---

# Claim-Matched Verification

## Match proof to the claim

Name the exact claim first, then choose the environment state that would make it true. Do not validate a stronger or different claim merely because its oracle is easy to observe.

| Claim | Suitable oracle |
|---|---|
| Visual/UI appearance | Controlled visual observation or screenshot; human observation can be primary |
| Execution path reached | Trace, breakpoint, hook hit with correct process/module/classloader/context |
| Mechanism controls behavior | Causal intervention plus the predicted state/output change and a control |
| Local persistence | File/database/preference state and reload/restart behavior |
| Parser/import success | Business-layer object/result, not header/decode success alone |
| Server/account outcome | Accepted server response or account-side state |
| Native patch correctness | ABI/calling convention, caller-visible effect, and stability under the target path |
| Reusable/release artifact | Clean build, target scenario, relevant adjacent/negative checks, and diagnostics removed |

A decompiler view, string, hook-loaded message, install success, or changed UI is useful only for the claim it directly observes.

## Minimum sufficient validation

Exploration may stop at an observation. Before a durable mechanism or success claim:

1. identify the oracle and overwrite/reversion risks;
2. run the target scenario;
3. include one relevant control or persistence/adjacent check when a cosmetic or coincidental result is plausible;
4. state what remains untested.

Do not run a generic regression matrix when the claim is narrow. Increase validation only when the artifact will be reused, distributed, migrated, or relied upon later.

When a human performs the oracle step, record the exact build/target, steps, and reported result. Do not downgrade a direct human visual judgment merely because it was manual; do not upgrade it into hidden-state proof.

Promote raw proof through `reverse-state` only when the claim is durable or must survive handoff. Otherwise report the observation inline.

## Final claim card

```text
Claim:
Oracle:
Observed result:
Control/repeatability:
Supported scope:
Not established:
```

Read `references/ORACLE_EXAMPLES.md` when the source of truth is ambiguous.
