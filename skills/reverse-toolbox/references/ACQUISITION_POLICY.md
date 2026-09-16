# Acquisition Policy Examples

## Usually autonomous

- Download a portable JADX or apktool release from the current official project release page into the user-local toolbox.
- Install a Python CLI into a toolbox-owned virtual environment from the official package index, after checking the current package identity and version.
- Adopt an existing reviewed `adb` binary by copying it into the toolbox and recording version/hash/source.

## Usually requires approval

- Install an Android USB driver or kernel extension.
- Start a persistent privileged daemon or expose a listening service.
- Add a remote MCP server that can read projects or write external state.
- Run an opaque `.exe`/`.msi` installer when a portable archive is unavailable and behavior is unclear.
- Use signing credentials, log into an account, root/jailbreak a device, or alter third-party/server state.

## Repair rather than rediscover

When a registered path disappears or its hash changes, mark the entry unhealthy, repair or re-acquire it, and update the receipt. Do not silently fall back to an arbitrary PATH version.

## Current facts

Tool versions, release URLs, install flags, signatures, platform support, and known compatibility issues are versioned facts. Verify them against current official documentation at acquisition or troubleshooting time; store only the concise decision and receipt.
