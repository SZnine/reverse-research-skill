---
name: reverse-state-evidence
description: Evidence discipline and durable project state for reverse engineering. Defines claim levels, state files, evidence IDs, and when a fact can be reused instead of rediscovered.
metadata:
  short-description: Evidence and durable reverse state
---

# Reverse State and Evidence

Use this skill whenever reverse-engineering work should be reusable across turns, sessions, builds, versions, or analysts.

## Principle

A claim is reusable only when it is tied to evidence. Evidence may be a file path, hash, offset, method, call stack, log line, trace, packet, saved field, database row, debugger observation, screenshot, diff, or command output.

Do not treat any of these as proof by themselves:

- UI text or visual success.
- Decompiled pseudocode alone.
- Obfuscated method/class names.
- A hook-loaded message.
- A single string match.
- A guess based on prior projects.

## Evidence levels

| Level | Meaning | Reuse rule |
|---|---|---|
| E0 | User report, model inference, intuition, unverified prior | Use only as a hypothesis. Never persist as fact. |
| E1 | Static artifact evidence: path, offset, symbol, xref, manifest, string, code branch | May guide probes. Not proof of runtime behavior. |
| E2 | Runtime observation: log, hook hit, breakpoint, trace, packet, file write | Proof the path executed under observed conditions. |
| E3 | Source-of-truth state evidence: persisted field, return enum, database row, network object, generated object, crash stack | Can support local proof and patch planning. |
| E4 | Repeated validation across restart/adjacent flows/versions or independent tools | Can become a reusable project fact or knowledge candidate. |

## Required state files

Use the templates in `templates/`.

- `RE_STATE.md`: target identity, baseline, confirmed facts, current mode, system map.
- `FRONTIER.md`: active hypotheses and information-gain ranking.
- `EVIDENCE_LEDGER.md`: evidence IDs and exact observations.
- `PROBE_LOG.md`: probes, expected observations, actual observations, and eliminations.
- `BUILD_LEDGER.md`: expensive build/repack/sign/install/test experiments.
- `ANCHORS.tsv`: semantic anchors, their evidence, and version mapping.

## Claim template

Every non-trivial claim should be expressible as:

```text
Claim:
Evidence ID(s):
Evidence level:
Scope:
Confidence:
Counterexamples or unknowns:
Reusable? yes/no:
```

## Reuse rule

Before re-running a baseline or diagnostic:

1. Read `RE_STATE.md`.
2. Check whether the fact is already proven at E2+ and still applicable.
3. Re-run only if the environment, APK/binary hash, OS/device, signing state, build, hook, or relevant config changed.

## Contradiction rule

When new evidence contradicts a confirmed fact:

- Do not silently overwrite.
- Mark the old fact as `contradicted` or `stale`.
- Add both evidence IDs.
- Return to the relevant mode: recon, frontier, anchor validation, or validation.

## Output standard

- Confirmed facts and evidence IDs.
- Likely but unproven hypotheses.
- Unknowns that matter.
- State files updated.
