---
name: reverse-migration-versioning
description: Version migration for reverse-engineered hooks, patches, anchors, and behavioral rules. Uses semantic anchor mapping and anti-anchor-fixation gates.
metadata:
  short-description: Version migration and anti-anchor-fixation
---

# Reverse Migration and Versioning

Use this skill when a previous working version, hook, patch, script, bypass, file format, or protocol parser exists.

## Principle

Previous work is a prior, not a constraint. Migrate by semantic responsibility, not by names.

## Migration workflow

1. Identify old version, new version, old working artifact, and success condition.
2. Confirm whether the baseline still holds in `RE_STATE.md`.
3. Build a version delta map: package layout, entry points, resources, DEX/classes, native libs, protocol/schema, signing/build, server/API.
4. Map old anchors to new candidates by:
   - caller/callee role;
   - call shape and arguments;
   - constants and strings;
   - field access pattern;
   - side effects;
   - runtime state transition;
   - nearby public wrappers/factories/validators.
5. Validate anchors using `reverse-anchor-validation`.
6. Migrate in dependency order: baseline -> loaders/startup -> state/persistence -> core behavior -> UI/reporting -> cleanup/regression.
7. Record mapping in `ANCHORS.tsv` and lessons in candidate knowledge only after validation.

## Anti-anchor-fixation rules

- If two old anchors fail to map or fail to affect behavior, stop migration and return to black-box recon.
- If a hook loads but behavior does not change, do not keep expanding hook code until runtime context and path execution are proven.
- If old responsibilities moved to native, resources, server, dynamic code, or persistence, abandon name-based mapping.
- If startup or loader baseline is already proven and unchanged, do not spend cycles re-proving it.

## Migration modes

### Shallow migration

Use when minor version change preserves structure. Validate existing anchors quickly, then patch/hook.

### Deep migration

Use when obfuscation, architecture, persistence, native code, or server flow changed. Return to static cartography + recon.

### Rebuild migration

Use when repack/sign/Gadget/injection changed. Must use cost-control and baseline build.

## Output standard

```text
Old artifact:
New target:
Delta summary:
Anchor mapping table:
Validated anchors:
Failed anchors and kill reasons:
Current migration mode:
Next action:
```
