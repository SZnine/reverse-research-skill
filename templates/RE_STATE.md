# RE_STATE

## Target

- target_name:
- target_type: apk | native | protocol | fileformat | mixed
- version:
- package/process/module:
- architecture/ABI:
- original_hash:
- working_copy_hash:
- current_date:
- current_mode:
- rigor_level:
- success_condition:

## Proven Baselines

| baseline | status | evidence_id | conditions | stale_if |
|---|---|---|---|---|
| original installs/runs | unknown | | | target hash/device changes |
| roundtrip rebuild starts | unknown | | | build tools/signing changes |
| dynamic attach works | unknown | | | process/device/connection changes |
| minimal script/hook loads | unknown | | | script/process/classloader changes |
| save/load/import/export baseline | unknown | | | data/schema/version changes |

## Confirmed Facts

| fact_id | fact | evidence_id | level | scope | confidence | status |
|---|---|---|---|---|---|---|

## Current System Map

| layer | status: blind/partial/observed/ruled-out/proven | evidence_id | unknowns | next_probe |
|---|---|---|---|---|
| packaging/signing/install | blind | | | |
| startup/lifecycle | blind | | | |
| loader/classloader/module | blind | | | |
| resources/assets/config | blind | | | |
| managed business logic | blind | | | |
| native/JNI | blind | | | |
| UI/rendering/input | blind | | | |
| persistence/save/db | blind | | | |
| network/server object flow | blind | | | |
| crypto/compression/integrity | blind | | | |
| auth/license/environment | blind | | | |
| protocol/file format | blind | | | |

## Active Decision

- current_mode:
- chosen_next_action:
- expected_observation:
- cost_class:
- kill_condition:
- state_files_to_update:

## Stale or Contradicted Facts

| old_fact | old_evidence | contradiction_evidence | action |
|---|---|---|---|
