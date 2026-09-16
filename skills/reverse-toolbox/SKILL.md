---
name: reverse-toolbox
description: "Resolve, acquire, and maintain reusable reverse-engineering tools in one persistent user-local toolbox. Use when a tool is needed, missing, stale, duplicated, or found only in PATH/old projects. Auto-acquire low-risk official portable tools when safe; ask only for privileged, invasive, or ambiguous installs."
metadata:
  version: "5.0"
  role: "persistent-tools"
  compatibility: Python 3.10+; network access is needed only for acquisition.
---

# Persistent Reverse Toolbox

## Invariant

Reusable tools live under one stable user-local root, default `~/.reverse-tools`. Projects contain target-specific scripts and outputs, not tool installations.

Resolve from the toolbox registry first. A PATH or old-project hit is a discovery hint: adopt it once if trustworthy, then use the registered path thereafter. Do not repeat broad path hunts on each task.

```bash
python <skill_dir>/scripts/toolbox.py init
python <skill_dir>/scripts/toolbox.py list [--query <capability>]
python <skill_dir>/scripts/toolbox.py resolve <name>
python <skill_dir>/scripts/toolbox.py doctor [<name>]
python <skill_dir>/scripts/toolbox.py prune              # dry run
python <skill_dir>/scripts/toolbox.py prune --apply      # registry-safe cleanup
```

Do not preflight a fixed APK/native tool profile. Identify the capability needed by the current probe, then resolve or acquire only that capability.

## Acquisition boundary

Acquire without a user round trip when all apply:

- current official vendor/project source over HTTPS;
- user-local portable archive, package, script, or binary;
- no administrator rights, driver, daemon, kernel component, account login, signing secret, license click-through, target-device mutation, or broad network service;
- provenance can be recorded and a published checksum/signature is verified when available.

Pause for approval when installation is system-wide, privileged, persistent, executable-installer based with unclear behavior, remotely connected, license-sensitive, or invasive to a device/account. The purpose is risk control, not habitual permission prompting.

Download to quarantine, verify, install under `packages/<name>/<version>/`, register its exact entry point, and keep a receipt. Never treat download success as tool health.

```bash
python <skill_dir>/scripts/toolbox.py fetch <name> --url <official-url> \
  --version <version> --entry <relative-executable> [--sha256 <digest>] \
  --source <official-project>
```

Adopt an already reviewed local tool once:

```bash
python <skill_dir>/scripts/toolbox.py register <name> --path <file-or-dir> \
  --version <version> --source <provenance> [--entry <relative-executable>]
```

If acquisition is blocked, continue with a lower-capability probe only when its evidentiary limits are explicit. Do not silently substitute a weaker tool merely to avoid a decision or permission boundary, and do not fabricate a tool result.

## Context economy

Search the registry by capability/tags, load only the selected tool's receipt, and return concise paths/version/health. Do not expose an entire catalog or broad MCP toolset to the model when one tool is needed. The library should grow through reviewed capabilities, not through stale quarantine files or invisible orphan installs; use `prune` to inspect and remove that operational debris.

For remote/MCP capability, prefer a local one-shot tool unless the capability is repeated or stateful. Before connecting a service, make data scope, write scope, authentication, and removal explicit.

Read `references/ACQUISITION_POLICY.md` for examples and edge cases.
