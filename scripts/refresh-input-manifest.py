#!/usr/bin/env python3
"""Regenerate the canonical agent-visible input size/SHA-256 manifest."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "docs" / "inputs"
MANIFEST = INPUTS / "SHA256SUMS.tsv"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    with (ROOT / "docs" / "contracts" / "selected-tasks-v1.tsv").open(encoding="utf-8", newline="") as handle:
        task_ids = [row["task_id"] for row in csv.DictReader(handle, delimiter="\t")]
    paths = sorted(
        path
        for task_id in task_ids
        for path in (INPUTS / task_id).rglob("*")
        if path.is_file()
    )
    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        for path in paths:
            writer.writerow((path.relative_to(ROOT).as_posix(), path.stat().st_size, digest(path)))
    print(f"wrote {len(paths)} rows to {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
