---
name: platform-android-apk
description: Android APK reverse-engineering specialization covering APK/DEX/smali/resources/native libs/signing/repackaging/Frida/Gadget/ADB/logcat/JNI/persistence/network. Use with the reverse-research orchestrator.
metadata:
  short-description: Android APK reverse platform module
---

# Platform: Android APK Reverse Engineering

Use this skill for Android APKs, DEX, smali, resources, native libraries, Frida/Gadget, signing, repackaging, app data, and Android runtime analysis.

## Always coordinate with

- `reverse-research-orchestrator`
- `reverse-state-evidence`
- `reverse-cost-control` before rebuild/repack/sign/install
- `reverse-dynamic-probing` before behavior-changing hooks

## APK layer map

1. APK identity: package, versionCode/versionName, hash, size, split/XAPK state.
2. Signing/install: signature schemes, certificate, zipalign, debuggable state, min/target SDK.
3. Manifest/components: activities, services, receivers, providers, permissions, intent filters.
4. Resources/assets: configs, strings, layouts, raw assets, network security config.
5. DEX/managed code: classes, obfuscation, reflection, dynamic loading, Kotlin/coroutines/generated dispatch.
6. Native/JNI: ABIs, `.so` libraries, JNI exports, `System.loadLibrary`, mapped modules.
7. Runtime: process, class loaders, threads, lifecycle, logs, exceptions.
8. Persistence: SharedPreferences, SQLite, files, saves, cache, external storage, backups.
9. Network: endpoints, cert pinning, request builders, response parsers, server object flow.
10. Protections: root/emulator/debugger/hook/tamper/integrity/license checks.

## Baseline checklist

Before modifying behavior:

- Preserve original APK hash.
- Confirm original install/startup behavior if feasible.
- Decode/analyze without rebuilding when possible.
- Record signing state and installed package state.
- Confirm whether existing state files already prove a baseline.

## Static APK cartography

Recommended inventory:

```text
apktool/analyze resources and manifest
jadx/java view for DEX-level map
smali for exact bytecode when decompiler output is suspect
unzip/aapt/apksigner output for package, resources, signature, and manifest facts
Ghidra/radare2 for native libraries
strings/xrefs/endpoints/log tags/file paths
```

Treat JADX/decompiler output as a hypothesis when exact control flow matters.

## Dynamic APK probing

Prefer buildless probes:

- `adb logcat` with narrow tag/message filters.
- Crash stack/tombstone inspection.
- `frida -U` / `frida -H` attach where possible.
- Process, module, and class-loader enumeration.
- `Java.perform` after the VM is ready.
- Method overload and caller verification.
- Runtime file/database/network observation.

Use Gadget only when inject/attach mode is unavailable or insufficient. If Gadget is embedded, prove:

1. Plain repack/sign/startup baseline.
2. Gadget library is loaded in the target process.
3. Connection mode and endpoint are correct.
4. Minimal script runs.
5. Target hooks execute under the target scenario.

## Repackaging/signing gates

Before rebuilding:

- Use `reverse-cost-control`.
- Decide whether this is baseline, instrumentation, patch, or regression build.
- Use a build ledger entry.
- Do not rebuild for a single low-confidence Java/smali guess.
- Validate signing scheme compatibility and install result.

## Common Android false conclusions

- Hook-loaded does not mean target path executed.
- UI success does not mean business/persistence success.
- `complete` callback does not imply saved state or server acceptance.
- Decompiled Java may hide native/JNI, reflection, dynamic code, or bad decompilation.
- A class name match across versions may be meaningless after obfuscation.
- A startup crash after repack may be signing/resource/native extraction/integrity, not the new hook.
- A value changed in a getter may be overwritten by persistence, native code, or server sync later.

## Output standard

```text
APK identity:
Baseline state:
Layer map:
Static evidence:
Runtime evidence:
Build/repack required? yes/no, reason:
Next platform-specific probe:
```
