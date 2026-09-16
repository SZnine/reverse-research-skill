#!/usr/bin/env python3
"""Persistent user-local toolbox for reusable reverse-engineering tools.

This helper manages provenance and stable paths. It does not choose which
reverse-engineering tool or probe the agent should use.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tarfile
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-.")
    if not value:
        raise SystemExit("name/version cannot be empty")
    return value[:100]


def default_root() -> Path:
    raw = os.environ.get("REVERSE_TOOL_HOME") or os.environ.get("RE_TOOL_HOME")
    return Path(raw).expanduser() if raw else Path.home() / ".reverse-tools"


def toolbox_root(value: str) -> Path:
    return Path(value).expanduser().resolve() if value else default_root().expanduser().resolve()


def registry_path(root: Path) -> Path:
    return root / "registry.json"


def ensure_root(root: Path) -> None:
    for name in ["bin", "packages", "cache", "quarantine", "receipts"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    p = registry_path(root)
    if not p.exists():
        save_json(
            p,
            {
                "schema_version": SCHEMA_VERSION,
                "root": str(root),
                "created_utc": now(),
                "tools": {},
            },
        )


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON: {path}: {exc}") from exc


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def load_registry(root: Path) -> dict[str, Any]:
    ensure_root(root)
    data = load_json(registry_path(root), {})
    if data.get("schema_version") != SCHEMA_VERSION:
        raise SystemExit(f"unsupported registry schema: {data.get('schema_version')}")
    data.setdefault("tools", {})
    return data


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_digest(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    h = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(item.relative_to(path).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(sha256_file(item).encode("ascii"))
        h.update(b"\0")
    return h.hexdigest()


def relative_or_absolute(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def resolve_record_path(root: Path, raw: str) -> Path:
    p = Path(raw).expanduser()
    return p.resolve() if p.is_absolute() else (root / p).resolve()


def health(root: Path, entry: dict[str, Any]) -> tuple[str, str, Path]:
    p = resolve_record_path(root, entry.get("entry_path", ""))
    if not entry.get("entry_path"):
        return "invalid", "entry_path missing", p
    if not p.is_file():
        return "missing", f"entry path is not a file: {p}", p
    expected = entry.get("entry_sha256", "")
    if expected:
        actual = sha256_file(p)
        if actual != expected:
            return "hash-mismatch", f"expected {expected}, got {actual}", p
    if os.name != "nt" and p.suffix.lower() not in {".jar", ".py"} and not os.access(p, os.X_OK):
        return "not-executable", f"entry is not executable: {p}", p
    return "available", "ok", p


def create_shim(root: Path, name: str, entry: Path) -> str:
    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        shim = bin_dir / f"{name}.cmd"
        suffix = entry.suffix.lower()
        if suffix == ".jar":
            command = f'@java -jar "{entry}" %*\r\n'
        elif suffix == ".py":
            command = f'@"{sys.executable}" "{entry}" %*\r\n'
        else:
            command = f'@"{entry}" %*\r\n'
        temp = shim.with_suffix(shim.suffix + ".tmp")
        try:
            temp.write_text(command, encoding="utf-8")
            temp.replace(shim)
        finally:
            temp.unlink(missing_ok=True)
        return relative_or_absolute(shim, root)

    shim = bin_dir / name
    suffix = entry.suffix.lower()
    if suffix == ".jar":
        command = f'exec java -jar {shlex_quote(str(entry))} "$@"'
    elif suffix == ".py":
        command = f'exec {shlex_quote(sys.executable)} {shlex_quote(str(entry))} "$@"'
    else:
        command = f'exec {shlex_quote(str(entry))} "$@"'
    temp = shim.with_name(shim.name + ".tmp")
    try:
        temp.write_text(f"#!/bin/sh\n{command}\n", encoding="utf-8")
        temp.chmod(temp.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        temp.replace(shim)
    finally:
        temp.unlink(missing_ok=True)
    return relative_or_absolute(shim, root)


def shlex_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def choose_entry(installed: Path, entry_arg: str, source_was_file: bool) -> Path:
    if source_was_file:
        if entry_arg and entry_arg not in {installed.name, "."}:
            candidate = installed.parent / entry_arg
            if not candidate.exists():
                raise SystemExit(f"entry not found after install: {candidate}")
            return candidate
        return installed
    if not entry_arg:
        raise SystemExit("--entry is required when registering or fetching a directory/archive")
    candidate = (installed / entry_arg).resolve()
    try:
        candidate.relative_to(installed.resolve())
    except ValueError as exc:
        raise SystemExit("entry must stay inside installed package") from exc
    if not candidate.is_file():
        raise SystemExit(f"entry not found after install: {candidate}")
    return candidate


def install_source(
    *,
    root: Path,
    name: str,
    version: str,
    source_path: Path,
    entry_arg: str,
    source_label: str,
    source_url: str,
    capability: str,
    tags: list[str],
    reference: bool,
    replace: bool,
    receipt_extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate first, then atomically publish a package and registry record.

    A failed update must not destroy the currently registered tool. Copied
    sources are prepared under a sibling staging directory, validated there,
    and swapped into place only after the entry point and digests are known.
    """
    registry = load_registry(root)
    name = safe_name(name)
    version = safe_name(version)
    previous = registry["tools"].get(name)
    if previous and not replace:
        raise SystemExit(f"tool already registered: {name}; use --replace to update")

    source_path = source_path.expanduser().resolve()
    if not source_path.exists():
        raise SystemExit(f"source path not found: {source_path}")

    package_root: Path | None = None
    staging: Path | None = None
    backup: Path | None = None
    swapped = False
    receipt_path: Path | None = None
    committed = False
    shim_path = root / "bin" / (f"{name}.cmd" if os.name == "nt" else name)
    old_shim: bytes | None = None
    old_shim_mode: int | None = None
    if shim_path.exists() and shim_path.is_file():
        old_shim = shim_path.read_bytes()
        old_shim_mode = shim_path.stat().st_mode

    try:
        if reference:
            installed = source_path
            source_was_file = source_path.is_file()
            entry = choose_entry(installed, entry_arg, source_was_file)
        else:
            package_parent = root / "packages" / name
            package_parent.mkdir(parents=True, exist_ok=True)
            package_root = package_parent / version
            if package_root.exists() and not replace:
                raise SystemExit(f"package destination exists: {package_root}; use --replace or prune the orphan")

            staging = Path(tempfile.mkdtemp(prefix=f".{version}.stage-", dir=package_parent))
            if source_path.is_file():
                installed_stage = staging / source_path.name
                shutil.copy2(source_path, installed_stage)
                source_was_file = True
            else:
                installed_stage = staging / "content"
                shutil.copytree(source_path, installed_stage)
                source_was_file = False

            entry_stage = choose_entry(installed_stage, entry_arg, source_was_file)
            if os.name != "nt" and entry_stage.suffix.lower() not in {".jar", ".py"}:
                entry_stage.chmod(entry_stage.stat().st_mode | stat.S_IXUSR)

            installed_rel = installed_stage.relative_to(staging)
            entry_rel = entry_stage.relative_to(staging)

            if package_root.exists():
                index = 1
                backup = package_parent / f".{version}.backup-{stamp()}"
                while backup.exists():
                    index += 1
                    backup = package_parent / f".{version}.backup-{stamp()}-{index}"
                package_root.rename(backup)
            staging.rename(package_root)
            staging = None
            swapped = True
            installed = package_root / installed_rel
            entry = package_root / entry_rel

        if reference and os.name != "nt" and entry.suffix.lower() not in {".jar", ".py"}:
            if not os.access(entry, os.X_OK):
                raise SystemExit(
                    f"external entry is not executable: {entry}; fix its mode or register without --reference"
                )

        entry_sha = sha256_file(entry)
        package_sha = tree_digest(installed)
        receipt_id = f"{name}-{version}-{stamp()}"
        receipt_path = root / "receipts" / f"{receipt_id}.json"
        receipt_index = 1
        while receipt_path.exists():
            receipt_index += 1
            receipt_id = f"{name}-{version}-{stamp()}-{receipt_index}"
            receipt_path = root / "receipts" / f"{receipt_id}.json"
        receipt = {
            "schema_version": SCHEMA_VERSION,
            "receipt_id": receipt_id,
            "installed_utc": now(),
            "name": name,
            "version": version,
            "source": source_label,
            "source_url": source_url,
            "source_path": str(source_path),
            "reference_external": reference,
            "installed_path": str(installed),
            "entry_path": str(entry),
            "entry_sha256": entry_sha,
            "package_sha256": package_sha,
            "capability": capability,
            "tags": sorted(set(tags)),
        }
        if receipt_extra:
            receipt.update(receipt_extra)
        save_json(receipt_path, receipt)

        shim = create_shim(root, name, entry)
        record = {
            "state": "available",
            "name": name,
            "version": version,
            "source": source_label,
            "source_url": source_url,
            "capability": capability,
            "tags": sorted(set(tags)),
            "installed_path": relative_or_absolute(installed, root),
            "entry_path": relative_or_absolute(entry, root),
            "entry_sha256": entry_sha,
            "package_sha256": package_sha,
            "shim_path": shim,
            "receipt_path": relative_or_absolute(receipt_path, root),
            "reference_external": reference,
            "updated_utc": now(),
        }
        registry["tools"][name] = record
        registry["updated_utc"] = now()
        save_json(registry_path(root), registry)
        committed = True

        if backup is not None and backup.exists():
            try:
                shutil.rmtree(backup)
            except OSError as exc:
                print(f"Warning: old package backup retained at {backup}: {exc}", file=sys.stderr)
        return record
    except BaseException:
        if committed:
            raise
        if receipt_path is not None:
            receipt_path.unlink(missing_ok=True)
        if swapped and package_root is not None and package_root.exists():
            shutil.rmtree(package_root)
        if backup is not None and backup.exists() and package_root is not None:
            backup.rename(package_root)
        if staging is not None and staging.exists():
            shutil.rmtree(staging)
        if old_shim is None:
            shim_path.unlink(missing_ok=True)
        else:
            shim_path.parent.mkdir(parents=True, exist_ok=True)
            shim_path.write_bytes(old_shim)
            if old_shim_mode is not None:
                shim_path.chmod(old_shim_mode)
        raise


def safe_zip_extract(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            name = info.filename.replace("\\", "/")
            target = (destination / name).resolve()
            try:
                target.relative_to(destination.resolve())
            except ValueError as exc:
                raise SystemExit(f"unsafe ZIP path: {name}") from exc
            mode = (info.external_attr >> 16) & 0o170000
            if mode == stat.S_IFLNK:
                raise SystemExit(f"ZIP symlink rejected: {name}")
        zf.extractall(destination)


def safe_tar_extract(archive: Path, destination: Path) -> None:
    with tarfile.open(archive) as tf:
        for member in tf.getmembers():
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination.resolve())
            except ValueError as exc:
                raise SystemExit(f"unsafe TAR path: {member.name}") from exc
            if member.issym() or member.islnk():
                raise SystemExit(f"TAR link rejected: {member.name}")
            if not (member.isfile() or member.isdir()):
                raise SystemExit(f"TAR special file rejected: {member.name}")
        # Paths, links, and special files were checked above. Avoid the newer
        # ``filter=`` API so the helper remains compatible with Python 3.10+.
        tf.extractall(destination)


def archive_kind(path: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    if zipfile.is_zipfile(path):
        return "zip"
    if tarfile.is_tarfile(path):
        return "tar"
    return "file"


def download(url: str, destination: Path, allow_http: bool) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"https", "http"}:
        raise SystemExit("only HTTP(S) URLs are supported")
    if parsed.scheme != "https" and not allow_http:
        raise SystemExit("non-HTTPS download rejected; use --allow-http only for a reviewed local/test source")
    request = urllib.request.Request(url, headers={"User-Agent": "reverse-toolbox/1"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as out:
            shutil.copyfileobj(response, out)
    except Exception as exc:  # network errors vary by platform
        destination.unlink(missing_ok=True)
        raise SystemExit(f"download failed: {exc}") from exc


def age_days(path: Path) -> float:
    try:
        modified = path.lstat().st_mtime
    except OSError:
        return 0.0
    return max(0.0, (dt.datetime.now().timestamp() - modified) / 86400.0)


def path_size(path: Path) -> int:
    try:
        if path.is_symlink() or path.is_file():
            return path.lstat().st_size
        return sum(item.lstat().st_size for item in path.rglob("*") if item.is_file() or item.is_symlink())
    except OSError:
        return 0


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except (OSError, ValueError):
        return False


def prune_candidates(root: Path, registry: dict[str, Any], args: argparse.Namespace) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    referenced = [
        resolve_record_path(root, record.get("installed_path", ""))
        for record in registry.get("tools", {}).values()
        if record.get("installed_path") and not record.get("reference_external")
    ]

    packages = root / "packages"
    if packages.exists():
        for tool_dir in sorted(packages.iterdir()):
            if not tool_dir.is_dir() or tool_dir.is_symlink():
                continue
            for package_dir in sorted(tool_dir.iterdir()):
                if package_dir.name.startswith("."):
                    if age_days(package_dir) >= args.staging_days:
                        candidates.append(
                            {
                                "kind": "staging-or-backup",
                                "path": package_dir,
                                "reason": f"hidden install staging/backup older than {args.staging_days:g} days",
                            }
                        )
                    continue
                in_use = any(path_is_within(item, package_dir) for item in referenced)
                if not in_use:
                    candidates.append(
                        {
                            "kind": "orphan-package",
                            "path": package_dir,
                            "reason": "package version is not referenced by the registry",
                        }
                    )

    quarantine = root / "quarantine"
    if quarantine.exists():
        for item in sorted(quarantine.iterdir()):
            if age_days(item) >= args.quarantine_days:
                candidates.append(
                    {
                        "kind": "stale-quarantine",
                        "path": item,
                        "reason": f"quarantine item older than {args.quarantine_days:g} days",
                    }
                )

    cache = root / "cache"
    if cache.exists() and args.cache_days >= 0:
        for item in sorted(p for p in cache.rglob("*") if p.is_file() or p.is_symlink()):
            if age_days(item) >= args.cache_days:
                candidates.append(
                    {
                        "kind": "stale-cache",
                        "path": item,
                        "reason": f"cached download older than {args.cache_days:g} days",
                    }
                )

    for item in candidates:
        item["bytes"] = path_size(item["path"])
    return candidates


def remove_prune_candidate(root: Path, path: Path) -> None:
    allowed = [root / "packages", root / "quarantine", root / "cache"]
    # For a symlink, validate the lexical parent and unlink the link rather
    # than following its target. Real directories must resolve inside a root.
    if path.is_symlink():
        if not any(path.parent.resolve() == base.resolve() or path_is_within(path.parent, base) for base in allowed):
            raise SystemExit(f"refusing to unlink outside toolbox cleanup roots: {path}")
        path.unlink(missing_ok=True)
        return
    if not any(path_is_within(path, base) for base in allowed):
        raise SystemExit(f"refusing to remove outside toolbox cleanup roots: {path}")
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def cmd_prune(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    registry = load_registry(root)
    candidates = prune_candidates(root, registry, args)
    serializable = [
        {**item, "path": str(item["path"])}
        for item in candidates
    ]
    if args.json:
        print(json.dumps(serializable, ensure_ascii=False, indent=2))
    elif not candidates:
        print("No toolbox debris found.")
    else:
        for item in candidates:
            print(f"{item['kind']}\t{item['bytes']}\t{item['path']}\t{item['reason']}")
        print(f"Candidates: {len(candidates)}; bytes: {sum(item['bytes'] for item in candidates)}")

    if not args.apply:
        if candidates and not args.json:
            print("Dry run only; add --apply to remove these candidates.")
        return 0

    removed = 0
    for item in candidates:
        remove_prune_candidate(root, item["path"])
        removed += 1
    for base in [root / "cache", root / "packages"]:
        if base.exists():
            for directory in sorted((p for p in base.rglob("*") if p.is_dir()), reverse=True):
                try:
                    directory.rmdir()
                except OSError:
                    pass
    print(f"Removed: {removed}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    ensure_root(root)
    print(f"Toolbox: {root}")
    print(f"Registry: {registry_path(root)}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    registry = load_registry(root)
    query = args.query.lower().strip()
    rows = []
    for name, entry in sorted(registry["tools"].items()):
        hay = " ".join([name, entry.get("capability", ""), *entry.get("tags", [])]).lower()
        if query and query not in hay:
            continue
        status, note, path = health(root, entry)
        rows.append(
            {
                "name": name,
                "version": entry.get("version", ""),
                "status": status,
                "path": str(path),
                "capability": entry.get("capability", ""),
                "tags": entry.get("tags", []),
                "note": note,
            }
        )
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif not rows:
        print("No matching registered tools.")
    else:
        for row in rows:
            print(f"{row['name']}\t{row['version']}\t{row['status']}\t{row['path']}\t{row['capability']}")
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    registry = load_registry(root)
    entry = registry["tools"].get(args.name)
    if not entry:
        print(f"missing: {args.name}", file=sys.stderr)
        return 2
    status, note, path = health(root, entry)
    result = {
        "name": args.name,
        "version": entry.get("version", ""),
        "status": status,
        "path": str(path),
        "shim": str(resolve_record_path(root, entry.get("shim_path", ""))) if entry.get("shim_path") else "",
        "source": entry.get("source", ""),
        "receipt": str(resolve_record_path(root, entry.get("receipt_path", ""))) if entry.get("receipt_path") else "",
        "note": note,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif status == "available":
        print(path)
    else:
        print(f"{status}: {note}", file=sys.stderr)
    return 0 if status == "available" else 3


def cmd_doctor(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    registry = load_registry(root)
    names = [args.name] if args.name else sorted(registry["tools"])
    failures = 0
    if not names:
        print("No registered tools.")
        return 0
    for name in names:
        entry = registry["tools"].get(name)
        if not entry:
            print(f"{name}\tmissing-registration")
            failures += 1
            continue
        status, note, path = health(root, entry)
        if status != "available":
            failures += 1
        print(f"{name}\t{status}\t{path}\t{note}")
        if status == "available" and args.repair_shims:
            entry["shim_path"] = create_shim(root, name, path)
    if args.repair_shims:
        save_json(registry_path(root), registry)
    return 0 if failures == 0 else 3


def cmd_register(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    ensure_root(root)
    record = install_source(
        root=root,
        name=args.name,
        version=args.version,
        source_path=Path(args.path),
        entry_arg=args.entry,
        source_label=args.source,
        source_url=args.source_url,
        capability=args.capability,
        tags=args.tag,
        reference=args.reference,
        replace=args.replace,
    )
    print(f"Registered: {args.name} {args.version}")
    print(resolve_record_path(root, record["entry_path"]))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    ensure_root(root)
    name = safe_name(args.name)
    version = safe_name(args.version)
    parsed = urllib.parse.urlparse(args.url)
    filename = Path(parsed.path).name or f"{name}-{version}.download"
    quarantine = root / "quarantine" / f"{name}-{version}-{stamp()}-{filename}"
    download(args.url, quarantine, args.allow_http)
    actual_sha = sha256_file(quarantine)
    if args.sha256 and actual_sha.lower() != args.sha256.lower():
        quarantine.unlink(missing_ok=True)
        raise SystemExit(f"SHA-256 mismatch: expected {args.sha256.lower()}, got {actual_sha}")

    kind = archive_kind(quarantine, args.archive)
    with tempfile.TemporaryDirectory(prefix=f"{name}-", dir=root / "quarantine") as tmp:
        temp = Path(tmp)
        if kind == "zip":
            safe_zip_extract(quarantine, temp)
            source = temp
            entry_arg = args.entry
        elif kind == "tar":
            safe_tar_extract(quarantine, temp)
            source = temp
            entry_arg = args.entry
        elif kind == "file":
            source = quarantine
            entry_arg = args.entry
        else:
            raise SystemExit(f"unsupported archive type: {kind}")

        record = install_source(
            root=root,
            name=name,
            version=version,
            source_path=source,
            entry_arg=entry_arg,
            source_label=args.source,
            source_url=args.url,
            capability=args.capability,
            tags=args.tag,
            reference=False,
            replace=args.replace,
            receipt_extra={
                "download_sha256": actual_sha,
                "expected_download_sha256": args.sha256.lower() if args.sha256 else "",
                "archive_kind": kind,
            },
        )

    cache_dir = root / "cache" / name / version
    cache_dir.mkdir(parents=True, exist_ok=True)
    cached = cache_dir / filename
    if cached.exists():
        cached = cache_dir / f"{stamp()}-{filename}"
    shutil.move(str(quarantine), str(cached))
    receipt = resolve_record_path(root, record["receipt_path"])
    receipt_data = load_json(receipt, {})
    receipt_data["cached_download"] = str(cached)
    save_json(receipt, receipt_data)

    print(f"Installed: {name} {version}")
    print(resolve_record_path(root, record["entry_path"]))
    if not args.sha256:
        print(f"Warning: no published checksum supplied; recorded downloaded SHA-256 {actual_sha}", file=sys.stderr)
    return 0


def cmd_import_legacy(args: argparse.Namespace) -> int:
    root = toolbox_root(args.root)
    ensure_root(root)
    manifest_path = Path(args.manifest).expanduser().resolve()
    legacy = load_json(manifest_path, {})
    legacy_home = manifest_path.parent
    imported = 0
    skipped = 0
    for name, entry in sorted(legacy.get("tools", {}).items()):
        if entry.get("state") != "available":
            skipped += 1
            continue
        raw = Path(entry.get("path", "")).expanduser()
        source = raw if raw.is_absolute() else legacy_home / raw
        if not source.exists():
            skipped += 1
            continue
        try:
            install_source(
                root=root,
                name=name,
                version=entry.get("version") or "legacy",
                source_path=source,
                entry_arg=args.entry if source.is_dir() and len(legacy.get("tools", {})) == 1 else "",
                source_label=entry.get("source") or f"legacy manifest {manifest_path}",
                source_url="",
                capability=entry.get("capability", ""),
                tags=["legacy-import"],
                reference=not args.copy,
                replace=args.replace,
                receipt_extra={"legacy_manifest": str(manifest_path)},
            )
            imported += 1
        except SystemExit as exc:
            print(f"skip {name}: {exc}", file=sys.stderr)
            skipped += 1
    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")
    return 0 if imported else 2


def add_root_arg(parser: argparse.ArgumentParser) -> None:
    # Support both ``--root X command`` and the more discoverable
    # ``command --root X`` without the subparser default clobbering the first.
    parser.add_argument(
        "--root",
        default=argparse.SUPPRESS,
        help="toolbox root; defaults to REVERSE_TOOL_HOME/RE_TOOL_HOME/~/.reverse-tools",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Persistent reverse-engineering toolbox")
    parser.add_argument("--root", default="", help="toolbox root; defaults to REVERSE_TOOL_HOME/RE_TOOL_HOME/~/.reverse-tools")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    add_root_arg(p)
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("list")
    add_root_arg(p)
    p.add_argument("--query", default="")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("resolve")
    add_root_arg(p)
    p.add_argument("name")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser("doctor")
    add_root_arg(p)
    p.add_argument("name", nargs="?", default="")
    p.add_argument("--repair-shims", action="store_true")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("register")
    add_root_arg(p)
    p.add_argument("name")
    p.add_argument("--path", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--source-url", default="")
    p.add_argument("--entry", default="")
    p.add_argument("--capability", default="")
    p.add_argument("--tag", action="append", default=[])
    p.add_argument("--reference", action="store_true", help="record external path instead of copying into toolbox")
    p.add_argument("--replace", action="store_true")
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("fetch")
    add_root_arg(p)
    p.add_argument("name")
    p.add_argument("--url", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--sha256", default="")
    p.add_argument("--archive", choices=["auto", "zip", "tar", "file"], default="auto")
    p.add_argument("--entry", default="")
    p.add_argument("--capability", default="")
    p.add_argument("--tag", action="append", default=[])
    p.add_argument("--allow-http", action="store_true")
    p.add_argument("--replace", action="store_true")
    p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("prune")
    add_root_arg(p)
    p.add_argument("--apply", action="store_true", help="remove candidates; default is a dry run")
    p.add_argument("--quarantine-days", type=float, default=7.0)
    p.add_argument("--cache-days", type=float, default=180.0, help="negative disables cache cleanup")
    p.add_argument("--staging-days", type=float, default=1.0)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_prune)

    p = sub.add_parser("import-legacy")
    add_root_arg(p)
    p.add_argument("--manifest", required=True)
    p.add_argument("--copy", action="store_true", help="copy tools into the new toolbox instead of external references")
    p.add_argument("--entry", default="", help="entry for a single legacy directory tool")
    p.add_argument("--replace", action="store_true")
    p.set_defaults(func=cmd_import_legacy)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
