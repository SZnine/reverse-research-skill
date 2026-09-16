---
name: reverse-apk
description: "Authorized Android APK/AAB reverse analysis / 安卓逆向: manifest, resources, DEX/smali, JNI/native libraries, runtime instrumentation, persistence/network behavior, and rebuild/sign/install. Supplies APK-specific probes without startup scaffolding or unused tool requirements."
metadata:
  version: "5.0"
  role: "target-adapter"
---

# Android APK Adapter

Use with `reverse-research`. This skill supplies Android-specific probe choices; it does not own project state, tool acquisition, or proof policy.

## Choose by question

- **Identity/package baseline:** hash, ZIP entries, package/version/signing/certificate, split/AAB layout.
- **Components and resources:** manifest, exported components, intent filters, permissions, resources, assets, navigation, strings.
- **Managed code:** DEX inventory, strings/xrefs, call graph around the behavior, compare decompiler output with smali when semantics matter.
- **Native/JNI:** ABI libraries, exports/imports, `RegisterNatives`, JNI bridges, load order, Java/native ownership.
- **Runtime:** package/process/PID, feature-trigger timing, classloader/module, overload/signature, hook hit and caller context.
- **State and network:** preferences/files/databases, import/export, restart behavior, request/response objects, server overwrite.
- **Rebuild path:** first isolate decode/build/align/sign/install/launch baseline; then attribute failures to the behavioral change.

Start with the lowest-cost probe that can separate the live hypotheses. Do not run every lane and do not require JADX, apktool, ADB, Frida, or Ghidra until the selected probe needs that capability. Use `reverse-toolbox` at that point.

## Android false proofs

- Decompiled Java is a static interpretation, not runtime control.
- “Script loaded” is not “hook resolved,” “hook hit,” or “state changed.”
- A visual change proves a visual claim; it does not prove persistence, business acceptance, or server state.
- An APK that builds, signs, or installs has passed packaging stages only.
- An old obfuscated name or matching method hit is not a migrated semantic anchor when behavior is unaffected.

## Efficient operator use

Device interaction, permission dialogs, biometric flows, exact gesture sequences, and direct visual comparison are often cheap operator probes. Use the operator card from `reverse-research` when they are materially easier for the user than automation. Ask for a specific result that changes the next action, not a broad “test the app.”

Before a persistent patch or final success statement, use `reverse-verify`. Put builds and logs in a `reverse-state` stage so test packages disappear unless promoted.
