#!/usr/bin/env python3
"""Prepare one fail-closed C0/T1 workspace without deleting prior evidence."""

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--condition", choices=("C0", "T1"), required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    campaign = args.campaign.resolve()
    source = repo / "docs" / "inputs" / args.task_id
    run_dir = campaign / "runs" / args.run_id
    workspace = run_dir / "workspace"
    inputs = workspace / "inputs"
    output = workspace / "output"
    logs = run_dir / "logs"

    if not source.is_dir():
        raise SystemExit(f"BLOCKED_INPUT_DIRECTORY_MISSING:{source}")
    if not run_dir.is_dir():
        raise SystemExit(f"BLOCKED_RUN_DIRECTORY_MISSING:{run_dir}")
    if any(inputs.iterdir()) if inputs.exists() else False:
        raise SystemExit("BLOCKED_INPUT_WORKSPACE_NOT_EMPTY")
    if any(output.iterdir()) if output.exists() else False:
        raise SystemExit("BLOCKED_OUTPUT_WORKSPACE_NOT_EMPTY")

    inputs.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    for path in source.rglob("*"):
        target = inputs / path.relative_to(source)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    rows = []
    for path in sorted(p for p in inputs.rglob("*") if p.is_file()):
        rows.append((path.relative_to(workspace).as_posix(), path.stat().st_size, digest(path)))
    manifest = workspace / "INPUT_MANIFEST.sha256.tsv"
    manifest.write_text(
        "path\tbytes\tsha256\n" + "".join(f"{p}\t{n}\t{h}\n" for p, n, h in rows),
        encoding="utf-8",
    )
    metadata = {
        "run_id": args.run_id,
        "task_id": args.task_id,
        "condition": args.condition,
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "input_file_count": len(rows),
        "input_manifest_sha256": digest(manifest),
        "output_initially_empty": True,
        "gold_oracle_copied": False,
        "release_status": "pending_external_gates",
    }
    (logs / "workspace_preparation.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
