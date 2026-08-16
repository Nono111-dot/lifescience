from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ACCEPTED = True


def check(workspace: Path) -> dict:
    output = workspace / "output"
    gold = json.loads((Path(__file__).parent / "gold.json").read_text(encoding="utf-8"))
    try:
        call = json.loads((output / "swap_call.json").read_text(encoding="utf-8"))
    except Exception:
        call = {}
    pair = tuple(sorted((str(call.get("organ_a", "")), str(call.get("organ_b", "")))))
    call_pair = call.get("swap_detected") is True and pair == ("Cloaca", "Stomach")
    confidence = str(call.get("confidence", "")).lower() in {"high", "medium", "高", "中"}
    evidence = call.get("evidence")
    evidence_ok = isinstance(evidence, (str, list, dict)) and bool(evidence)

    try:
        with (output / "sample_similarity.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except Exception:
        rows = []
    required = {"organ_a", "organ_b", "swap_score", "rank", "evidence_type"}
    schema = bool(rows) and required.issubset(rows[0])
    pairs = {}
    finite = True
    ordered = True
    if schema:
        for row in rows:
            a, b = row.get("organ_a", ""), row.get("organ_b", "")
            ordered &= bool(a and b and a < b)
            try:
                score = float(row["swap_score"])
                rank = int(row["rank"])
                finite &= math.isfinite(score) and rank >= 1
            except (TypeError, ValueError):
                finite = False
                continue
            pairs[(a, b)] = (score, rank, row.get("evidence_type", ""))
    coverage = schema and len(rows) == len(pairs) == gold["candidate_pair_count"] and ordered and finite
    top = pairs.get(("Cloaca", "Stomach"), (None, None, ""))
    unique_top = coverage and top[1] == 1 and sum(1 for _, rank, _ in pairs.values() if rank == 1) == 1 and bool(top[2])

    report = (output / "report.md").read_text(encoding="utf-8", errors="replace").lower() if (output / "report.md").is_file() else ""
    report_ok = all(term in report for term in ("cloaca", "stomach")) and ("swap" in report or "互换" in report) and any(term in report for term in ("promoter", "marker", "reference", "geo", "accessibility")) and any(term in report for term in ("uncert", "limit", "局限", "置信"))
    core = (20 if call_pair else 0) + (10 if coverage else 0) + (10 if unique_top else 0)
    decision = call_pair and unique_top and confidence and evidence_ok
    checks = {
        "call_exact_cloaca_stomach": call_pair,
        "confidence_calibrated": confidence,
        "task_specific_evidence_present": evidence_ok,
        "all_105_unique_ordered_finite_pairs": coverage,
        "cloaca_stomach_unique_rank_1": unique_top,
        "report_consistent_with_method_and_uncertainty": report_ok,
    }
    return {
        "core_science": core,
        "direction": 15 if decision else 0,
        "summary": 5 if report_ok else 0,
        "hardgate_pass": call_pair and coverage and unique_top,
        "failure_codes": ["LS03_ATAC_" + key.upper() for key, ok in checks.items() if not ok],
        "criteria": checks,
    }
