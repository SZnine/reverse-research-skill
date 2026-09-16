---
name: reverse-research
description: "Control authorized multi-step reverse engineering / 逆向分析 across APK, native binaries, protocols, and file formats. Use to choose probes, stop unproductive loops, and hand cheap visual/manual actions to the user when that is materially more efficient. Do not use for a single local code explanation."
metadata:
  version: "5.0"
  role: "control-plane"
---

# Reverse Research Control

## Outcome contract

Pursue the user's actual question, not completion of a predefined workflow. Let current evidence determine the path.

Proceed only on targets and actions the user owns or is authorized to assess. Pause only when a materially invasive step has unresolved scope; do not access or expose credentials, private data, accounts, or third-party services outside that scope. Preserve the original before irreversible mutation.

For a local snippet, one error, or one artifact fact, answer directly. Create state only when the work will span probes, mutations, handoff, or a likely context reset.

## Investigation loop

1. State the current question or decision in one sentence.
2. Choose the smallest probe that can change that decision.
3. Observe the result; distinguish fact, inference, and unknown.
4. Continue, change layer, hand off a micro-action, or stop.

Do not calculate elaborate cost scores. Quality is primary; among comparably informative paths, prefer the one with lower total execution, recovery, context, and human burden. Do not spend attention optimizing cost unless paths differ materially, a resource limit is real, or the operator split changes.

After two materially identical failures with no new evidence, do not attempt a third unchanged retry. Change the hypothesis, execution boundary, tool, or operator split.

## Agent versus operator

Do the work yourself when it is machine-readable, deterministic, accessible, and not materially more expensive than involving the user.

Return control to the user when all are true:

- the user can complete the action with a few clicks, a direct visual judgment, or local device access;
- the agent path is blocked, substantially costlier, slower, or less reliable;
- the result will determine the next probe or final claim.

Do not delegate shell commands, file searches, text comparison, or routine edits that the agent can perform. Do not keep simulating a GUI or visual oracle merely to preserve autonomy.

Before pausing, preserve only the minimum resume state. Ask for one compact operator card:

```text
Operator action: <one action or a tightly related batch>
Why it is needed: <decision it resolves>
Do: <exact clicks/gesture/observation>
Return: <specific value, screenshot, or one-of-N result>
Resume from: <next action for each likely result>
```

After issuing the operator card, stop dependent work until the result returns; do not simulate the observation or continue as though it succeeded. A user observation is an observation, not automatically a mechanism claim. It can be the correct oracle when the claim itself is visual or interaction-level.

## Conditional skills

Load only what the current step needs:

- target adapter: `reverse-apk`, `reverse-native`, or `reverse-protocol`;
- `reverse-state` for staged work, disposable artifacts, handoff, or context reset;
- `reverse-toolbox` only when a reusable capability is needed or unhealthy;
- `reverse-verify` before durable success/mechanism claims or reusable patched output.

Do not load every support skill at task start.

## Stop and report

Stop when the question is answered, the next useful observation requires the operator, the remaining probes have low decision value, or scope is not authorized. Report only the current result, its limit, and the next consequential action. Fixed status blocks and ceremonial ledgers are not required.

Read `references/CANONICAL_CASES.md` only when delegation or stopping behavior is ambiguous.
