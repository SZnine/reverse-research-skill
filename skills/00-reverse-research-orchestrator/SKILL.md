---
name: reverse-research-orchestrator
description: Mandatory entry point for professional reverse-engineering work. Classifies task complexity and mode, prevents premature patch/rebuild loops, coordinates recon, frontier, static cartography, dynamic probing, anchor validation, local proof, patching, validation, migration, and knowledge governance.
metadata:
  short-description: Reverse research workflow orchestrator
---

# Reverse Research Orchestrator

Use this skill before any reverse-engineering, APK analysis, hook migration, binary patch, protocol analysis, file-format analysis, or dynamic instrumentation task.

## Mission

Behave like a senior reverse researcher:

1. Define the objective and success condition.
2. Preserve baseline and evidence.
3. Build a system map before local proof when the mechanism is unknown.
4. Maintain a hypothesis frontier.
5. Prefer buildless and low-cost probes before expensive rebuilds.
6. Patch only after a source-of-truth path is proven.
7. Validate through real behavior, persistence, and adjacent flows.
8. Save lessons only when evidence-backed and bounded by applicability guards.

## First decision: rigor level

Before doing work, classify rigor level.

### R0: Quick answer / cheap inspection

Use when the user asks for a small static check, a direct file explanation, a manifest/resource question, a known one-line build error, or a simple code-path lookup.

Rules:
- Do not create a full hypothesis frontier.
- Use at most 1-2 hypotheses.
- Prefer direct artifact inspection.
- Escalate only if evidence contradicts the simple explanation.

### R1: Scoped troubleshooting

Use when one layer is likely involved but not proven, such as a startup crash, signing problem, class-loader mismatch, a failed hook, a save-load failure, or a simple native crash.

Rules:
- Maintain a small frontier of 2-4 hypotheses.
- Use existing logs and static map first.
- No behavior-changing patch until the failing layer is identified.

### R2: Full reverse research

Use when the mechanism is unknown, obfuscated, cross-layer, protected, version-migrated, persistence-sensitive, server-coupled, native/JNI-heavy, or repeatedly failing.

Rules:
- Use the full orchestrated loop.
- Maintain `RE_STATE.md`, `FRONTIER.md`, `EVIDENCE_LEDGER.md`, `PROBE_LOG.md`, and, when rebuilding, `BUILD_LEDGER.md`.
- One expensive build must test multiple hypotheses unless it is a baseline or blocker-unblocking build.

### R3: Migration / long-running research

Use when a previous working version/hook/patch exists or when multiple rounds will accumulate reusable knowledge.

Rules:
- Use `reverse-migration-versioning` and `reverse-knowledge-governance`.
- Treat historical anchors as priors, not facts.
- Add anti-anchor-fixation gates.

## Mode selection

Declare exactly one active mode before action:

| Mode | Use when | Primary skill |
|---|---|---|
| Quick Triage | Simple target or direct question | `reverse-quick-triage` |
| Scope/Baseline | Target identity, package, build, runtime baseline unknown | `reverse-state-evidence` + platform skill |
| Black-box Recon | Mechanism unknown | `reverse-blackbox-recon` |
| Frontier Management | Competing hypotheses exist | `reverse-hypothesis-frontier` |
| Static Cartography | Need system map without execution | `reverse-static-cartography` |
| Dynamic Probing | Need runtime truth | `reverse-dynamic-probing` |
| Anchor Validation | Candidate anchor exists but is not proven | `reverse-anchor-validation` |
| Local Proof | Anchor likely controls behavior | `reverse-local-proof-patch` |
| Cost Gate | Repack/rebuild/sign/install/test considered | `reverse-cost-control` |
| Migration | Previous version exists | `reverse-migration-versioning` |
| Validation | Behavior changed or final claim needed | `reverse-validation-release` |
| Knowledge Curation | Reusable lesson proposed | `reverse-knowledge-governance` |

## Pre-action contract

Before any non-trivial action, write:

```text
Mode:
Rigor level:
Objective:
Success condition:
Known baseline from RE_STATE:
Current evidence:
Hypotheses under consideration:
Next action:
Expected observation:
Cost class: buildless / low / medium / expensive
What this action can eliminate:
Escalation or kill condition:
State files to update:
```

For R0 quick tasks, this may be compressed to one paragraph.

## Hard gates

1. No behavior-changing patch before a source-of-truth path is proven.
2. No rebuild/repack/sign/install/test for one low-confidence guess.
3. No treating decompiler output, obfuscated names, UI text, strings, or hook load messages as proof by themselves.
4. No repeated startup/signing/Gadget/class-loader baseline checks if `RE_STATE.md` already proves them and no contradictory evidence exists.
5. If two local attempts fail without eliminating competing hypotheses, stop local work and return to Black-box Recon.
6. If a hook loads but behavior is unchanged, verify process, class loader, timing, overload, and target-path execution before changing the hook logic.
7. If a UI operation appears successful but state is wrong, trace the next business-layer return value or persisted state before patching UI code.
8. If data import/export or protocol loading fails, isolate discovery, header, decode, companion resource, business validation, and persistence layers separately.
9. Experience memory is a prior; live evidence wins.

## Build/repack decision gate

A rebuild is allowed only if one of these is true:

- It is a baseline roundtrip build.
- It is a batch instrumentation build collecting observations for at least three hypotheses.
- It validates a high-confidence patch whose source-of-truth path is proven.
- It resolves a blocker preventing further dynamic/static analysis.

Every build must update `BUILD_LEDGER.md`.

## Escalation and de-escalation

Escalate from quick/scoped to full research when:
- evidence contradicts the simple explanation;
- two cheap probes fail;
- the target crosses Java/native/resource/network/persistence layers;
- version migration or obfuscation dominates;
- rebuilding becomes necessary;
- persistent state differs from UI state.

De-escalate to quick mode when:
- the failing layer is isolated;
- one source-of-truth path is proven;
- the remaining work is a direct local patch or validation;
- the target is simple and continuing the full frontier would add overhead.

## Output standard

Report:

- Current mode and rigor level.
- Confirmed facts with evidence IDs.
- Active hypotheses and why the chosen next action has the best information-gain/cost ratio.
- What was not checked and why.
- Exact state files updated.
- Next action or final result.
