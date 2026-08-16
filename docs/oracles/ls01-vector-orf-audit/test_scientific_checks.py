from __future__ import annotations

import csv
from pathlib import Path
import tempfile

import scientific_checks as checker


ROWS = [
    {"construct_id": "c01", "frame_ok": "true", "start_ok": "true", "stop_ok": "true", "tag_ok": "false", "overall_status": "fail", "issues": "TAG"},
    {"construct_id": "c02", "frame_ok": "false", "start_ok": "true", "stop_ok": "false", "tag_ok": "true", "overall_status": "fail", "issues": "STOP;FRAME"},
    {"construct_id": "c03", "frame_ok": "false", "start_ok": "true", "stop_ok": "true", "tag_ok": "false", "overall_status": "fail", "issues": "FRAME;TAG"},
]


def make_workspace(root: Path, rows=ROWS) -> Path:
    output = root / "output"; output.mkdir(parents=True)
    with (output / "construct_audit.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0])); writer.writeheader(); writer.writerows(rows)
    (output / "report.md").write_text("c01, c02, and c03 all fail; no construct passes or is usable.\n", encoding="utf-8")
    return root


def test_acceptance_three_reference_repetitions_and_negative_controls():
    for _ in range(3):
        with tempfile.TemporaryDirectory() as directory:
            result = checker.check(make_workspace(Path(directory)))
            assert result["hardgate_pass"] and result["core_science"] == 40 and result["direction"] == 15
    with tempfile.TemporaryDirectory() as directory:
        empty = checker.check(Path(directory))
        assert not empty["hardgate_pass"] and empty["core_science"] < 40
    wrong_rows = [dict(row) for row in ROWS]
    wrong_rows[1]["frame_ok"] = "true"
    wrong_rows[1]["issues"] = "STOP"
    with tempfile.TemporaryDirectory() as directory:
        wrong = checker.check(make_workspace(Path(directory), wrong_rows))
        assert not wrong["hardgate_pass"] and "FRAME_OK_MISMATCH" in wrong["failure_codes"]


if __name__ == "__main__":
    test_acceptance_three_reference_repetitions_and_negative_controls()
    print("PASS: 3/3 reference plus empty and scientifically wrong controls")
