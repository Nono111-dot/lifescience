#!/usr/bin/env python3
"""Freeze one completed run and hash every artifact without executing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree_manifest(root: Path) -> list[tuple[str, int, str]]:
    return [
        (path.relative_to(root).as_posix(), path.stat().st_size, digest(path))
        for path in sorted(p for p in root.rglob("*") if p.is_file())
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()

    run_dir = args.campaign.resolve() / "runs" / args.run_id
    workspace = run_dir / "workspace"
    frozen = run_dir / "frozen"
    logs = run_dir / "logs"
    if not workspace.is_dir():
        raise SystemExit(f"BLOCKED_WORKSPACE_MISSING:{workspace}")
    if not (workspace / "INPUT_MANIFEST.sha256.tsv").is_file():
        raise SystemExit("BLOCKED_INPUT_MANIFEST_MISSING")
    if any(frozen.iterdir()) if frozen.exists() else False:
        raise SystemExit("BLOCKED_FROZEN_DIRECTORY_NOT_EMPTY")

    frozen.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    for path in workspace.rglob("*"):
        target = frozen / path.relative_to(workspace)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    rows = tree_manifest(frozen)
    manifest = logs / "frozen_workspace.sha256.tsv"
    manifest.write_text(
        "path\tbytes\tsha256\n" + "".join(f"{p}\t{n}\t{h}\n" for p, n, h in rows),
        encoding="utf-8",
    )
    record = {
        "run_id": args.run_id,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "file_count": len(rows),
        "manifest_sha256": digest(manifest),
        "submission_code_executed": False,
        "frozen_directory": str(frozen),
    }
    (logs / "freeze_record.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
