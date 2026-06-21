---
name: reverse-hypothesis-frontier
description: Maintain a ranked hypothesis frontier for reverse-engineering work. Prevents local tunnel vision by scoring information gain, cost, confidence, and kill conditions.
metadata:
  short-description: Hypothesis frontier management
---

# Reverse Hypothesis Frontier

Use this skill whenever there are competing explanations or repeated local failures.

## Objective

Choose probes that eliminate the most uncertainty for the lowest cost.

## Frontier table

Maintain `FRONTIER.md` with this schema:

```text
| id | hypothesis | layer | evidence | confidence | cost | info_gain | next_probe | expected_obs | eliminates | kill_condition | status |
```

## Scoring

Use qualitative values unless numeric scoring is useful.

- Confidence: low / medium / high.
- Cost: buildless / low / medium / expensive.
- Information gain: low / medium / high.
- Priority = information gain divided by cost, adjusted by objective relevance.

Do not let confidence exceed `medium` unless the hypothesis has E2+ evidence. Do not let it exceed `high` unless it has E3+ evidence and no active contradictions.

## Rules

1. Keep 3-7 active hypotheses for R2/R3 work. R0/R1 may use fewer.
2. Each hypothesis must have a kill condition.
3. Prefer probes that distinguish multiple hypotheses.
4. Do not patch a hypothesis; patch a proven source-of-truth path.
5. If a probe only confirms that a suspicious path exists, but not that it controls behavior, keep the hypothesis active or move to anchor validation.
6. Dead-end a hypothesis only with evidence, not boredom.
7. Reopen a dead hypothesis if new evidence contradicts the reason it was closed.

## Common hypothesis classes

- Wrong process, class loader, timing, or overload.
- Hook path executes but is downstream of source of truth.
- UI path succeeds but business/persistence path fails.
- Java path delegates to native/JNI.
- Resource/config path controls behavior instead of code.
- Signature/integrity/path check causes startup or load failure.
- Server object state overrides local state.
- Save/protocol header parses but body/companion resource fails.
- Decompiler produced misleading pseudocode.
- Version migration anchor changed responsibility.

## Update protocol

After every probe:

1. Add evidence to `EVIDENCE_LEDGER.md`.
2. Update the relevant hypothesis confidence/status.
3. Record which hypotheses were eliminated.
4. Choose the next highest information-gain/cost action.
5. If no hypothesis has a good next probe, return to black-box recon.

## Output standard

```text
Selected next probe:
Why this probe beats alternatives:
Hypotheses it can eliminate:
Expected observations:
Kill condition:
Fallback mode:
```
