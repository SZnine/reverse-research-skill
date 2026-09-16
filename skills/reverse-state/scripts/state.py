#!/usr/bin/env python3
"""Deterministic state/checkpoint helper for reverse-state.

The script deliberately does not choose investigation strategy. It creates a
small working state, isolates disposable stage output, promotes selected
artifacts, and removes the rest at milestone boundaries.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

SCHEMA_VERSION = 1


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-.")
    return value[:64] or "stage"


def stage_label(value: str) -> str:
    return re.sub(r"^\d{8}-\d{6}-", "", value) or value


def unique_file(folder: Path, stem: str, suffix: str) -> Path:
    path = folder / f"{stem}{suffix}"
    if not path.exists():
        return path
    for index in range(2, 10000):
        candidate = folder / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
    raise SystemExit(f"cannot allocate unique file in {folder}: {stem}{suffix}")


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


def state_root(workspace: str, state_dir: str) -> Path:
    ws = Path(workspace).expanduser().resolve()
    raw = Path(state_dir).expanduser()
    return raw.resolve() if raw.is_absolute() else (ws / raw).resolve()


def ensure_layout(root: Path) -> None:
    for name in ["checkpoints", "stages", "proof", "deliverables", "original"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    lessons = root / "LESSONS.json"
    if not lessons.exists():
        lessons.write_text(
            json.dumps({"schema_version": SCHEMA_VERSION, "lessons": []}, indent=2) + "\n",
            encoding="utf-8",
        )


def extract_field(text: str, heading: str, default: str = "") -> str:
    pattern = rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    if not match:
        return default
    body = match.group(1).strip()
    if body.startswith("- "):
        body = body[2:]
    return body or default


def render_state(
    root: Path,
    *,
    objective: str,
    target: str,
    target_sha256: str,
    confirmed: str,
    decision: str,
    blocker: str,
    next_action: str,
    latest_checkpoint: str,
    active_stage: str,
) -> None:
    target_text = target or "none"
    if target_sha256:
        target_text += f"\n- SHA-256: `{target_sha256}`"
    content = f"""# Reverse State

Updated: {now()}

## Objective
- {objective or 'unknown'}

## Target
- {target_text}

## Confirmed now
- {confirmed or 'none'}

## Current decision
- {decision or 'none'}

## Blocker
- {blocker or 'none'}

## Next action
- {next_action or 'none'}

## Active stage
- {active_stage or 'none'}

## Latest checkpoint
- {latest_checkpoint or 'none'}
"""
    (root / "STATE.md").write_text(content, encoding="utf-8")


def current_state(root: Path) -> dict[str, str]:
    p = root / "STATE.md"
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8", errors="replace")
    target = extract_field(text, "Target")
    target = target.splitlines()[0].removeprefix("- ").strip()
    sha_match = re.search(r"SHA-256:\s*`?([0-9a-fA-F]{64})", text)
    return {
        "objective": extract_field(text, "Objective"),
        "target": "" if target == "none" else target,
        "target_sha256": sha_match.group(1).lower() if sha_match else "",
        "confirmed": extract_field(text, "Confirmed now"),
        "decision": extract_field(text, "Current decision"),
        "blocker": extract_field(text, "Blocker"),
        "next_action": extract_field(text, "Next action"),
        "latest_checkpoint": extract_field(text, "Latest checkpoint"),
        "active_stage": extract_field(text, "Active stage"),
    }


def cmd_init(args: argparse.Namespace) -> int:
    root = state_root(args.workspace, args.state_dir)
    ensure_layout(root)
    state = current_state(root)
    target = ""
    digest = ""
    if args.target:
        p = Path(args.target).expanduser()
        if not p.is_absolute():
            p = (Path(args.workspace).expanduser().resolve() / p).resolve()
        if not p.is_file():
            raise SystemExit(f"target not found: {p}")
        target = str(p)
        digest = sha256_file(p)
    if not (root / "STATE.md").exists() or args.replace_state:
        render_state(
            root,
            objective=args.objective or state.get("objective", ""),
            target=target or state.get("target", ""),
            target_sha256=digest or state.get("target_sha256", ""),
            confirmed="none",
            decision="state initialized; choose the next decisive probe",
            blocker="none",
            next_action=args.next or "choose the smallest probe that can change the current decision",
            latest_checkpoint="none",
            active_stage="none",
        )
    print(f"State root: {root}")
    print(f"State: {root / 'STATE.md'}")
    if target:
        print(f"Target SHA-256: {digest}")
    return 0


def cmd_stage(args: argparse.Namespace) -> int:
    root = state_root(args.workspace, args.state_dir)
    ensure_layout(root)
    sid = f"{stamp()}-{slug(args.name)}"
    stage = root / "stages" / sid
    counter = 1
    while stage.exists():
        counter += 1
        stage = root / "stages" / f"{sid}-{counter}"
    stage.mkdir(parents=True)
    meta = {
        "schema_version": SCHEMA_VERSION,
        "id": stage.name,
        "created_utc": now(),
        "name": args.name,
        "purpose": args.purpose or "",
        "status": "active",
    }
    (stage / "STAGE.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    state = current_state(root)
    render_state(
        root,
        objective=args.objective or state.get("objective", ""),
        target=state.get("target", ""),
        target_sha256=state.get("target_sha256", ""),
        confirmed=state.get("confirmed", "none"),
        decision=args.purpose or f"run stage {stage.name}",
        blocker="none",
        next_action=f"complete or checkpoint stage `{stage.name}`",
        latest_checkpoint=state.get("latest_checkpoint", "none"),
        active_stage=stage.name,
    )
    print(stage.name)
    print(stage)
    return 0


def resolve_stage(root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    raw = Path(value).expanduser()
    candidate = raw.resolve() if raw.is_absolute() else (root / "stages" / raw).resolve()
    stages = (root / "stages").resolve()
    try:
        candidate.relative_to(stages)
    except ValueError as exc:
        raise SystemExit(f"stage must be inside {stages}: {candidate}") from exc
    if not candidate.is_dir():
        raise SystemExit(f"stage not found: {candidate}")
    return candidate


def unique_destination(folder: Path, name: str) -> Path:
    dst = folder / name
    if not dst.exists():
        return dst
    stem, suffix = dst.stem, dst.suffix
    for i in range(2, 10000):
        alt = folder / f"{stem}-{i}{suffix}"
        if not alt.exists():
            return alt
    raise SystemExit(f"cannot allocate destination for {name}")


def parse_promote(spec: str) -> tuple[str, str]:
    if "=" in spec:
        path, role = spec.rsplit("=", 1)
    elif ":" in spec:
        path, role = spec.rsplit(":", 1)
    else:
        raise SystemExit(f"promotion must be PATH:proof or PATH:deliverable: {spec}")
    role = role.strip().lower()
    if role not in {"proof", "deliverable"}:
        raise SystemExit(f"unsupported promotion role: {role}")
    return path.strip(), role


def promote_artifact(
    root: Path, stage: Path | None, workspace: Path, spec: str
) -> dict[str, str]:
    raw, role = parse_promote(spec)
    src = Path(raw).expanduser()
    if not src.is_absolute():
        base = stage if stage is not None else workspace
        src = (base / src).resolve()
    else:
        src = src.resolve()
    if not src.exists():
        raise SystemExit(f"promotion source not found: {src}")
    dest_dir = root / ("proof" if role == "proof" else "deliverables")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = unique_destination(dest_dir, src.name)

    inside_stage = False
    if stage is not None:
        try:
            src.relative_to(stage)
            inside_stage = True
        except ValueError:
            pass
    if inside_stage:
        shutil.move(str(src), str(dest))
    elif src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return {
        "role": role,
        "source": str(src),
        "path": str(dest),
        "sha256": tree_digest(dest),
        "kind": "directory" if dest.is_dir() else "file",
    }


def safe_remove_stage(stage: Path, root: Path) -> None:
    stages = (root / "stages").resolve()
    resolved = stage.resolve()
    if resolved == stages:
        raise SystemExit("refusing to remove stages root")
    try:
        resolved.relative_to(stages)
    except ValueError as exc:
        raise SystemExit(f"refusing to remove path outside stages: {resolved}") from exc
    shutil.rmtree(resolved)


def checkpoint_markdown(
    *,
    cid: str,
    stage: Path | None,
    status: str,
    objective: str,
    summary: str,
    decision: str,
    limitations: str,
    recipe: list[str],
    next_action: str,
    promoted: list[dict[str, str]],
    cleanup: str,
) -> str:
    promo_lines = [
        f"- `{p['path']}` — {p['role']}, {p['kind']}, sha256 `{p['sha256']}`"
        for p in promoted
    ] or ["- none"]
    recipe_lines = [f"- `{r}`" for r in recipe] or ["- none"]
    return f"""# Checkpoint {cid}

- Created UTC: {now()}
- Status: {status}
- Stage: {stage.name if stage else 'none'}
- Objective: {objective or 'unknown'}

## Observation
{summary or 'none'}

## Decision
{decision or 'none'}

## Limitations
{limitations or 'none'}

## Reproduction recipe
{os.linesep.join(recipe_lines)}

## Promoted artifacts
{os.linesep.join(promo_lines)}

## Stage cleanup
{cleanup}

## Next action
{next_action or 'none'}
"""


def cmd_checkpoint(args: argparse.Namespace) -> int:
    root = state_root(args.workspace, args.state_dir)
    ensure_layout(root)
    stage = resolve_stage(root, args.stage)
    current = current_state(root)
    objective = args.objective or current.get("objective", "")
    label = args.name or (stage_label(stage.name) if stage else args.status)
    cid_stem = f"{stamp()}-{slug(label)}"
    workspace = Path(args.workspace).expanduser().resolve()

    # Validate every promotion source before moving the first one. This avoids
    # the common partial-promotion failure caused by a typo in a later spec.
    parsed_sources: list[Path] = []
    for spec in args.promote:
        raw, _ = parse_promote(spec)
        src = Path(raw).expanduser()
        if not src.is_absolute():
            src = ((stage if stage is not None else workspace) / src).resolve()
        else:
            src = src.resolve()
        if not src.exists():
            raise SystemExit(f"promotion source not found: {src}")
        parsed_sources.append(src)
    if len(set(parsed_sources)) != len(parsed_sources):
        raise SystemExit("the same artifact cannot be promoted more than once in one checkpoint")

    promoted = [promote_artifact(root, stage, workspace, spec) for spec in args.promote]

    should_delete = False
    if stage is not None:
        if args.discard_stage:
            should_delete = True
        elif args.keep_stage:
            should_delete = False
        else:
            should_delete = args.status in {"success", "abandoned"}

    cleanup = "no stage"
    stage_name = stage.name if stage else "none"
    if stage is not None and should_delete:
        safe_remove_stage(stage, root)
        cleanup = "unpromoted stage artifacts deleted"
    elif stage is not None:
        cleanup = "stage preserved for resume"

    checkpoint = unique_file(root / "checkpoints", cid_stem, ".md")
    cid = checkpoint.stem
    checkpoint.write_text(
        checkpoint_markdown(
            cid=cid,
            stage=stage,
            status=args.status,
            objective=objective,
            summary=args.summary,
            decision=args.decision,
            limitations=args.limitations,
            recipe=args.recipe,
            next_action=args.next,
            promoted=promoted,
            cleanup=cleanup,
        ),
        encoding="utf-8",
    )

    blocker = args.summary if args.status == "blocked" else "none"
    confirmed = args.summary if args.status == "success" else current.get("confirmed", "none")
    active_stage = stage_name if stage is not None and not should_delete else "none"
    render_state(
        root,
        objective=objective,
        target=current.get("target", ""),
        target_sha256=current.get("target_sha256", ""),
        confirmed=confirmed,
        decision=args.decision or f"stage {args.status}",
        blocker=blocker,
        next_action=args.next,
        latest_checkpoint=str(checkpoint),
        active_stage=active_stage,
    )
    print(f"Checkpoint: {checkpoint}")
    print(f"Cleanup: {cleanup}")
    for p in promoted:
        print(f"Promoted {p['role']}: {p['path']}")
    return 0


def cmd_preserve(args: argparse.Namespace) -> int:
    root = state_root(args.workspace, args.state_dir)
    ensure_layout(root)
    src = Path(args.path).expanduser()
    if not src.is_absolute():
        src = (Path(args.workspace).expanduser().resolve() / src).resolve()
    if not src.is_file():
        raise SystemExit(f"artifact not found: {src}")
    digest = sha256_file(src)
    dest = root / "original" / src.name
    if dest.exists():
        existing = sha256_file(dest)
        if existing != digest:
            dest = unique_destination(root / "original", f"{src.stem}-{digest[:12]}{src.suffix}")
    if not dest.exists():
        shutil.copy2(src, dest)
    state = current_state(root)
    render_state(
        root,
        objective=state.get("objective", ""),
        target=str(dest),
        target_sha256=digest,
        confirmed=state.get("confirmed", "none"),
        decision="original artifact preserved before mutation",
        blocker="none",
        next_action=args.next or state.get("next_action", ""),
        latest_checkpoint=state.get("latest_checkpoint", "none"),
        active_stage=state.get("active_stage", "none"),
    )
    print(f"Preserved: {dest}")
    print(f"SHA-256: {digest}")
    return 0


def normalize_key(*parts: str) -> str:
    text = "|".join(re.sub(r"\s+", " ", p.strip().lower()) for p in parts)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def cmd_lesson(args: argparse.Namespace) -> int:
    root = state_root(args.workspace, args.state_dir)
    ensure_layout(root)
    p = root / "LESSONS.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise SystemExit(f"invalid lessons store: {p}: {exc}") from exc
    lessons = data.setdefault("lessons", [])
    key = normalize_key(args.when, args.signal, args.do)
    existing = next((x for x in lessons if x.get("key") == key), None)
    basis = [b for b in args.basis if b]
    targets = [t for t in args.target if t]
    if existing:
        existing["boundary"] = args.boundary or existing.get("boundary", "")
        existing["basis"] = sorted(set(existing.get("basis", []) + basis))
        existing["targets"] = sorted(set(existing.get("targets", []) + targets))
        existing["last_seen_utc"] = now()
        existing["count"] = int(existing.get("count", 1)) + 1
        action = "merged"
    else:
        existing = {
            "id": f"LESSON-{stamp()}-{key[:6]}",
            "key": key,
            "when": args.when,
            "signal": args.signal,
            "do": args.do,
            "boundary": args.boundary,
            "basis": basis,
            "targets": targets,
            "created_utc": now(),
            "last_seen_utc": now(),
            "count": 1,
        }
        lessons.append(existing)
        action = "added"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Lesson {action}: {existing['id']}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = state_root(args.workspace, args.state_dir)
    if not root.exists():
        raise SystemExit(f"state root not found: {root}")
    active = sorted(p.name for p in (root / "stages").iterdir() if p.is_dir()) if (root / "stages").exists() else []
    checkpoints = list((root / "checkpoints").glob("*.md")) if (root / "checkpoints").exists() else []
    proof = list((root / "proof").iterdir()) if (root / "proof").exists() else []
    deliverables = list((root / "deliverables").iterdir()) if (root / "deliverables").exists() else []
    print((root / "STATE.md").read_text(encoding="utf-8") if (root / "STATE.md").exists() else "STATE.md missing")
    print(f"Active stages: {len(active)}" + (f" ({', '.join(active)})" if active else ""))
    print(f"Checkpoints: {len(checkpoints)}")
    print(f"Proof artifacts: {len(proof)}")
    print(f"Deliverables: {len(deliverables)}")
    return 0


def add_common_location_args(parser: argparse.ArgumentParser) -> None:
    # SUPPRESS preserves a value supplied before the subcommand while also
    # allowing the intuitive ``command --workspace ...`` form used in docs.
    parser.add_argument("--workspace", default=argparse.SUPPRESS)
    parser.add_argument("--state-dir", default=argparse.SUPPRESS)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compact reverse-work state and stage lifecycle helper")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--state-dir", default=".reverse")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create the minimal state layout")
    add_common_location_args(p)
    p.add_argument("--objective", default="")
    p.add_argument("--target", default="")
    p.add_argument("--next", default="")
    p.add_argument("--replace-state", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("stage", help="create one disposable stage directory")
    add_common_location_args(p)
    p.add_argument("--name", required=True)
    p.add_argument("--purpose", default="")
    p.add_argument("--objective", default="")
    p.set_defaults(func=cmd_stage)

    p = sub.add_parser("checkpoint", help="distill a milestone, promote selected artifacts, and clean the stage")
    add_common_location_args(p)
    p.add_argument("--stage", default="")
    p.add_argument("--name", default="")
    p.add_argument("--status", choices=["success", "abandoned", "blocked"], required=True)
    p.add_argument("--objective", default="")
    p.add_argument("--summary", required=True)
    p.add_argument("--decision", default="")
    p.add_argument("--limitations", default="")
    p.add_argument("--recipe", action="append", default=[])
    p.add_argument("--next", default="")
    p.add_argument("--promote", action="append", default=[], metavar="PATH:ROLE")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--keep-stage", action="store_true")
    group.add_argument("--discard-stage", action="store_true")
    p.set_defaults(func=cmd_checkpoint)

    p = sub.add_parser("preserve", help="copy and hash an original before mutation")
    add_common_location_args(p)
    p.add_argument("--path", required=True)
    p.add_argument("--next", default="")
    p.set_defaults(func=cmd_preserve)

    p = sub.add_parser("lesson", help="add or merge one concrete reusable lesson")
    add_common_location_args(p)
    p.add_argument("--when", required=True)
    p.add_argument("--signal", required=True)
    p.add_argument("--do", required=True)
    p.add_argument("--boundary", required=True)
    p.add_argument("--basis", action="append", default=[])
    p.add_argument("--target", action="append", default=[])
    p.set_defaults(func=cmd_lesson)

    p = sub.add_parser("status", help="show concise current state and counts")
    add_common_location_args(p)
    p.set_defaults(func=cmd_status)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
