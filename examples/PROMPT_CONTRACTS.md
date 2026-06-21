# Prompt Contracts

## Full reverse research prompt

```text
Use reverse-research-orchestrator.
Target: <artifact/path/version>
Objective: <behavior to understand/change>
Constraints: minimize rebuilds; preserve original; use evidence-led state.
Before any rebuild, show hypotheses covered and expected observations.
Update RE_STATE.md, FRONTIER.md, EVIDENCE_LEDGER.md, PROBE_LOG.md, and BUILD_LEDGER.md when relevant.
```

## Quick triage prompt

```text
Use reverse-quick-triage unless evidence forces escalation.
Question: <specific APK/binary/protocol question>
Return direct evidence and the next cheapest check only.
```

## Migration prompt

```text
Use reverse-research-orchestrator and reverse-migration-versioning.
Old working artifact: <path/version>
New target: <path/version>
Goal: migrate behavior without local trial-and-error rebuild loops.
Treat old anchors as priors. After two failed anchors, return to black-box recon.
```

## Knowledge curation prompt

```text
Use reverse-knowledge-governance.
Review the latest probe/build logs and propose candidate lessons only.
Do not promote any lesson without evidence IDs, applicability, not-applicable cases, and kill conditions.
```
