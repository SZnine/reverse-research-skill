# Universal Reverse Research Skill Pack v1.0

Date: 2026-06-20
Purpose: a modular, reusable reverse-engineering skill system that behaves like a senior reverse researcher instead of a single-threaded patch/rebuild loop.

This package is intentionally not tied to one APK, game, binary, or protocol. It provides an orchestrated workflow for Android APKs, native binaries, file formats, protocols, version migrations, patch/hook validation, and durable experience capture.

## Design goals

1. Optimize information gain per token, per build, and per runtime experiment.
2. Prevent premature local proof, premature patching, and repeated expensive rebuilds.
3. Preserve the useful parts of classic evidence-driven reverse engineering.
4. Add a fast path for simple targets so the agent does not overthink easy APKs.
5. Allow experience accumulation without turning hallucinated or overfitted lessons into permanent rules.
6. Treat project history as a prior, never as proof.
7. Make every expensive action produce durable state.

## Package structure

```text
reverse-research-skill-pack-v1/
  README.md
  PACKAGE_MANIFEST.md
  skills/
    00-reverse-research-orchestrator/SKILL.md
    01-reverse-quick-triage/SKILL.md
    02-reverse-state-evidence/SKILL.md
    03-reverse-blackbox-recon/SKILL.md
    04-reverse-hypothesis-frontier/SKILL.md
    05-reverse-static-cartography/SKILL.md
    06-reverse-dynamic-probing/SKILL.md
    07-reverse-anchor-validation/SKILL.md
    08-reverse-cost-control/SKILL.md
    09-reverse-local-proof-patch/SKILL.md
    10-reverse-migration-versioning/SKILL.md
    11-reverse-validation-release/SKILL.md
    12-reverse-knowledge-governance/SKILL.md
    platform-android-apk/SKILL.md
    platform-native-binary/SKILL.md
    platform-protocol-fileformat/SKILL.md
  templates/
    RE_STATE.md
    FRONTIER.md
    EVIDENCE_LEDGER.md
    PROBE_LOG.md
    BUILD_LEDGER.md
    ANCHORS.tsv
    KNOWLEDGE_CANDIDATES.md
    KNOWLEDGE_BASE.yaml
    NEGATIVE_LESSONS.yaml
    SHORTCUTS.yaml
    HANDOFF_REPORT.md
  sources/
    SOURCE_REGISTRY.md
  examples/
    MINIMAL_PROJECT_LAYOUT.md
    PROMPT_CONTRACTS.md
    LESSON_ENTRY_EXAMPLES.md
```

## How to use

Use `00-reverse-research-orchestrator` as the mandatory entry skill for all reverse-engineering work. The orchestrator decides whether to take the quick path, full black-box recon, static mapping, dynamic probing, local proof, patching, migration, validation, or knowledge curation.

Copy the directories under `skills/` into your skill system. Keep the templates under each reverse project root, not inside the global skill directory.

Recommended project layout:

```text
project/
  original/
  work/
  scripts/
  evidence/
  builds/
  notes/
    RE_STATE.md
    FRONTIER.md
    EVIDENCE_LEDGER.md
    PROBE_LOG.md
    BUILD_LEDGER.md
    ANCHORS.tsv
    KNOWLEDGE_CANDIDATES.md
    KNOWLEDGE_BASE.yaml
    NEGATIVE_LESSONS.yaml
    SHORTCUTS.yaml
```

## Core operating model

```text
Quick Triage -> Scope/Baseline -> Black-box Recon -> Hypothesis Frontier
      -> Static Cartography -> Dynamic Probing -> Anchor Validation
      -> Local Proof -> Patch/Hook -> Validation/Release -> Knowledge Governance
```

The agent should not always walk the whole pipeline. Simple cases use quick triage. Hard cases use the full orchestrated loop.

## Non-negotiable gates

- No behavior-changing patch before a source-of-truth path is proven.
- No rebuild for one low-confidence guess.
- No durable lesson without evidence IDs and applicability guards.
- No treating UI text, method names, generated decompiler output, or loaded hooks as proof by themselves.
- No repeating baselines already recorded in `RE_STATE.md` unless contradicted.
- If two local attempts fail without eliminating competing hypotheses, return to recon.

## Experience memory principle

Knowledge is stored in four layers:

1. `KNOWLEDGE_CANDIDATES.md`: untrusted candidate lessons.
2. `KNOWLEDGE_BASE.yaml`: promoted reusable patterns with evidence and contraindications.
3. `NEGATIVE_LESSONS.yaml`: measures that were proven wrong under specific conditions.
4. `SHORTCUTS.yaml`: validated shortest paths with preconditions and kill conditions.

Experience is a search prior, not a rule. Live evidence overrides memory.
