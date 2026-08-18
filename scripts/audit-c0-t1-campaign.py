#!/usr/bin/env python3
"""Fail-closed structural preflight for the 25-task C0/T1 campaign."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def accepted_oracles() -> set[str]:
    accepted = set()
    for path in (DOCS / "oracles").glob("*/scientific_checks.py"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^ACCEPTED\s*=\s*True(?:\s*#.*)?$", text, flags=re.MULTILINE):
            accepted.add(path.parent.name)
    return accepted


def input_hash_audit(task_ids: list[str]) -> tuple[int, list[str]]:
    manifest = DOCS / "inputs" / "SHA256SUMS.tsv"
    if not manifest.is_file():
        return 0, ["INPUT_HASH_MANIFEST_MISSING"]
    failures = []
    rows = read_tsv(manifest)
    manifest_paths = {
        (row.get("path") or row.get("file") or row.get("relative_path") or "").replace("\\", "/")
        for row in rows
    }
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for task_id in task_ids
        for path in (DOCS / "inputs" / task_id).rglob("*")
        if path.is_file()
    }
    for rel in sorted(actual_paths - manifest_paths):
        failures.append(f"INPUT_UNMANIFESTED:{rel}")
    for rel in sorted(manifest_paths - actual_paths):
        failures.append(f"INPUT_MANIFEST_STALE:{rel}")
    checked = 0
    for row in rows:
        rel = row.get("path") or row.get("file") or row.get("relative_path")
        expected = row.get("sha256") or row.get("SHA256")
        if not rel or not expected:
            failures.append("INPUT_HASH_MANIFEST_SCHEMA")
            continue
        rel_path = Path(rel)
        path = ROOT / rel_path if rel_path.parts[:2] == ("docs", "inputs") else DOCS / "inputs" / rel_path
        if not path.is_file():
            failures.append(f"INPUT_MISSING:{rel}")
            continue
        checked += 1
        if sha256(path).lower() != expected.lower():
            failures.append(f"INPUT_HASH_MISMATCH:{rel}")
    return checked, failures


def main() -> int:
    inventory = read_tsv(DOCS / "input-problem-inventory-v1.tsv")
    queue = read_tsv(DOCS / "formal-run-queue-c0-t1-2026-08-16.tsv")
    capabilities = read_tsv(DOCS / "capability-runtime-mapping-v1.tsv")
    skill_plan = read_tsv(DOCS / "task-skill-plan-codex-t1-v1.tsv")
    task_ids = [row["task_id"] for row in inventory]
    pair_counts: dict[str, Counter] = defaultdict(Counter)
    for row in queue:
        pair_counts[row["task_id"]][row["condition"]] += 1

    failures = []
    if len(task_ids) != 25 or len(set(task_ids)) != 25:
        failures.append("TASK_SCOPE_NOT_25_UNIQUE")
    if len(queue) != 50:
        failures.append("RUN_QUEUE_NOT_50")
    for task_id in task_ids:
        if pair_counts[task_id] != Counter({"C0": 1, "T1": 1}):
            failures.append(f"UNPAIRED_QUEUE:{task_id}")
    if len(skill_plan) != 25 or {row["task_id"] for row in skill_plan} != set(task_ids):
        failures.append("T1_TASK_SKILL_PLAN_SCOPE_INVALID")

    mapped = [
        row for row in capabilities
        if row["source_repo"] and row["source_ref"] and row["source_path"] and row["codex_install_source"]
    ]
    source_verified = [row for row in capabilities if row["source_verification"] == "sha256_pass"]
    smoke_ready = [
        row for row in capabilities
        if row["install_smoke_status"] == row["invoke_smoke_status"] == row["uninstall_smoke_status"] == "pass"
    ]
    if len(mapped) != len(capabilities):
        failures.append("T1_INSTALL_SOURCE_MAPPING_INCOMPLETE")
    if len(source_verified) != len(capabilities):
        failures.append("T1_SOURCE_SHA_VERIFICATION_INCOMPLETE")

    capability_by_id = {row["catalog_item_id"]: row for row in capabilities}
    selected_ids = {
        item
        for row in skill_plan
        if row["selected_catalog_item_ids"] != "NONE"
        for item in row["selected_catalog_item_ids"].split(",")
    }
    if len(capabilities) != len(selected_ids):
        failures.append("T1_SELECTED_SKILL_MAPPING_SCOPE_MISMATCH")
    unknown_selected = sorted(selected_ids - set(capability_by_id))
    for item in unknown_selected:
        failures.append(f"T1_SELECTED_SKILL_UNKNOWN:{item}")
    for item in sorted(set(capability_by_id) - selected_ids):
        failures.append(f"T1_SKILL_MAPPING_UNUSED:{item}")
    ineligible_selected = sorted(
        item for item in selected_ids
        if item in capability_by_id
        and capability_by_id[item]["strict_t1_eligibility"] != "selected_executed"
    )
    for item in ineligible_selected:
        failures.append(f"T1_SELECTED_SKILL_EXTERNAL_DEPENDENCY:{item}")
    selected_install_ready = {
        item for item in selected_ids
        if item in capability_by_id and capability_by_id[item]["install_smoke_status"] == "pass"
    }
    selected_full_smoke = {
        item for item in selected_ids
        if item in capability_by_id
        and capability_by_id[item]["install_smoke_status"] == "pass"
        and capability_by_id[item]["invoke_smoke_status"] == "pass"
        and capability_by_id[item]["uninstall_smoke_status"] == "pass"
    }
    selected_reset_ready = {
        item for item in selected_ids
        if item in capability_by_id
        and capability_by_id[item]["uninstall_smoke_status"] == "pass"
    }
    if selected_install_ready != selected_ids:
        failures.append("T1_SELECTED_SKILL_INSTALL_SMOKE_INCOMPLETE")
    if selected_reset_ready != selected_ids:
        failures.append("T1_SELECTED_SKILL_RESET_SMOKE_INCOMPLETE")

    accepted = accepted_oracles()
    missing_accepted = sorted(set(task_ids) - accepted)
    for task_id in missing_accepted:
        failures.append(f"ORACLE_NOT_ACCEPTED:{task_id}")

    checked_inputs, input_failures = input_hash_audit(task_ids)
    failures.extend(input_failures)

    result = {
        "campaign": "25-task-c0-t1-v2",
        "task_count": len(task_ids),
        "run_count": len(queue),
        "paired_tasks": sum(pair_counts[t] == Counter({"C0": 1, "T1": 1}) for t in task_ids),
        "selected_skill_mapping_rows": len(capabilities),
        "install_source_mapped_rows": len(mapped),
        "source_sha_verified_rows": len(source_verified),
        "smoke_ready_rows": len(smoke_ready),
        "t1_tasks_with_selected_skill": sum(row["selected_catalog_item_ids"] != "NONE" for row in skill_plan),
        "t1_tasks_without_catalog_match": sum(row["selected_catalog_item_ids"] == "NONE" for row in skill_plan),
        "selected_unique_skills": len(selected_ids),
        "selected_install_smoke_ready": len(selected_install_ready),
        "selected_reset_smoke_ready": len(selected_reset_ready),
        "selected_full_smoke_ready": len(selected_full_smoke),
        "selected_not_invoked_in_scored_run": len(selected_ids - selected_full_smoke),
        "accepted_oracles": len(accepted & set(task_ids)),
        "input_files_checked": checked_inputs,
        "formal_release": not failures,
        "failure_codes": sorted(set(failures)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
