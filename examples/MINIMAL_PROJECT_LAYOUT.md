# Minimal Project Layout

```text
project/
  original/
    target.apk | target.bin | samples/
  work/
    active/
  scripts/
    frida/
    ghidra/
    analysis/
  evidence/
    logs/
    screenshots/
    traces/
    diffs/
  builds/
    baseline/
    instrumentation/
    patch/
    regression/
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

For simple R0/R1 tasks, not every directory is required. Start with `original/`, `work/`, and `notes/RE_STATE.md` only.
