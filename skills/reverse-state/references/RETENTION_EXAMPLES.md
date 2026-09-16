# Retention Examples

| Artifact | Default | Promote when |
|---|---|---|
| Original APK/binary | Record path/hash during read-only analysis | Copy before mutation, when source may disappear, or when exact rollback is required |
| Decompiled tree | Ephemeral/cache | A tiny cited excerpt or mapping is not cheaply reproducible or needed for handoff |
| Broad logcat/trace | Delete after distillation | A narrow raw segment is the only support for a durable claim or regression |
| Debug/test APK | Delete after the test | It is the final deliverable, a unique baseline, or rebuilding is materially expensive/non-deterministic |
| Failed build directory | Delete after cause is captured | Needed to reproduce a toolchain defect that is still active |
| Screenshot | Ephemeral | The claim is visual and the screenshot is the chosen oracle/deliverable |
| Hook script | Keep as project source when still active | Promote to deliverable only when reusable and documented |
| Patched release binary | Deliverable | Always retain with the exact source target, recipe, and validation result |
| Tool installer/package | Never project-local | Store in the persistent toolbox cache/receipt store |

“Could be useful later” is not a promotion criterion. Prefer reconstructability over accumulation.
