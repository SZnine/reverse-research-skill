# Lesson Entry Examples

## Candidate negative lesson

```yaml
id: NL-android-hook-loaded-no-effect-001
title: Hook loaded but behavior unchanged does not prove hook logic is wrong
status: candidate
tier: K0
situation: Android method hook logs startup but target behavior is unchanged
preconditions:
  - Hook framework reports script loaded
  - No evidence that target method executed in the target scenario
incorrect_measures:
  - Rebuilding or rewriting the hook logic immediately
why_incorrect:
  - The failure may be process, class loader, timing, overload, or path execution
shortest_path:
  - Verify process/PID, class loader, overload, timing, and runtime hit with caller stack before editing hook logic
evidence_ids:
  - EVID-PLACEHOLDER
not_applicable_when:
  - Runtime hit, inputs/outputs, and source-of-truth state effect are already proven
kill_conditions:
  - Target method hit with expected caller and correct state effect still fails
```

## Shortcut template

```yaml
id: SC-apk-rebuild-gate-001
title: Batch instrumentation before patch build
status: active
tier: K1
situation: Large APK where rebuild/install/test is expensive and mechanism is not localized
preconditions:
  - At least three active hypotheses exist
  - Buildless probes cannot answer them
shortest_path:
  - Create one instrumentation build with stage-labeled checkpoints for all top hypotheses
not_applicable_when:
  - A source-of-truth patch is already proven
  - The build is only a baseline roundtrip
kill_conditions:
  - Instrumentation causes startup failure or hides target behavior
```
