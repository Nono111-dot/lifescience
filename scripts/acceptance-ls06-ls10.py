"""Acceptance controls for the four benchmark-gold scientific checkers.

Runs each reference three times, then empty and format-correct scientific-wrong
controls. Test workspaces live under ignored work/ and never enter agent inputs.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "work" / "checker_acceptance"


CASES = {
    "ls06-eno1-effect-size": {
        "reference": {"eno1_effect.json": {"gene": "ENO1", "tumor_value": 350385456.451912,
            "normal_value": 72896133.2946858, "fold_change": 4.81, "log2_fold_change": 2.27,
            "source_file": "Proteomic_data .xlsx", "source_sheet": "Tumor vs Normal"},
            "report.md": "ENO1 is 4.81-fold higher (increased) in tumor."},
        "wrong": {"eno1_effect.json": {"gene": "ENO1", "tumor_value": 72896133.2946858,
            "normal_value": 350385456.451912, "fold_change": 0.21, "log2_fold_change": -2.27,
            "source_file": "Proteomic_data .xlsx", "source_sheet": "Tumor vs Normal"},
            "report.md": "ENO1 is lower in tumor."},
    },
    "ls06-eno1-significance-audit": {
        "reference": {"eno1_significance.json": {"gene": "ENO1", "adjusted_p_value": 0.226,
            "fdr_threshold": 0.05, "significant": False, "source_file": "Proteomic_data .xlsx",
            "source_sheet": "Tumor vs Normal"}, "report.md": "Adjusted p=0.226; not significant at FDR 0.05."},
        "wrong": {"eno1_significance.json": {"gene": "ENO1", "adjusted_p_value": 0.0226,
            "fdr_threshold": 0.05, "significant": True, "source_file": "Proteomic_data .xlsx",
            "source_sheet": "Tumor vs Normal"}, "report.md": "Adjusted p=0.0226; significant."},
    },
    "ls10-neun-power-analysis": {
        "reference": {"power_result.json": {"group_labels": ["KD", "CTRL"], "means": {"KD": 214.5, "CTRL": 210.625},
            "sds": {"KD": 10.9414023651, "CTRL": 22.8531804601}, "pooled_sd": 17.9162236933,
            "cohens_d": 0.2162844172, "alpha": 0.05, "power": 0.8, "alternative": "two-sided",
            "required_n_per_group": 337}, "report.md": "Cohen d=0.216; 337 per group at alpha 0.05 and 80% power."},
        "wrong": {"power_result.json": {"group_labels": ["KD", "CTRL"], "means": {"KD": 214.5, "CTRL": 210.625},
            "sds": {"KD": 10.94, "CTRL": 22.85}, "pooled_sd": 16.0, "cohens_d": 0.9,
            "alpha": 0.05, "power": 0.8, "alternative": "two-sided", "required_n_per_group": 22},
            "report.md": "Cohen d=0.9; 22 per group."},
    },
    "ls10-treatment-response-model": {
        "reference": {"model_coefficients.csv": "term,estimate,std_error,z,p_value,odds_ratio\nage,-0.079508469,0.0262977303,-3.023,0.0024995441,0.9235701982\n",
            "model_metadata.json": {"terms": ["BMI", "age", "gender"], "outcome": "PR=1 positive response",
                "gender_reference": "female", "n_complete_cases": 80},
            "report.md": "Age coefficient -0.0795, p=0.0025; odds decrease with age."},
        "wrong": {"model_coefficients.csv": "term,estimate,std_error,z,p_value,odds_ratio\nage,0.0795,0.0263,3.0,0.25,1.08\n",
            "model_metadata.json": {"terms": ["BMI", "age", "gender"], "outcome": "PR=1",
                "gender_reference": "female", "n_complete_cases": 80}, "report.md": "Age increases response odds."},
    },
}


def load_checker(task: str):
    path = ROOT / "docs" / "oracles" / task / "scientific_checks.py"
    spec = importlib.util.spec_from_file_location(task.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def materialize(task: str, label: str, artifacts: dict) -> Path:
    ws = BASE / task / label; out = ws / "output"
    if ws.exists(): shutil.rmtree(ws)
    out.mkdir(parents=True)
    for name, value in artifacts.items():
        path = out / name
        if isinstance(value, dict): path.write_text(json.dumps(value), encoding="utf-8")
        else: path.write_text(value, encoding="utf-8")
    return ws


def main() -> int:
    failures = []
    for task, case in CASES.items():
        checker = load_checker(task)
        for run in range(1, 4):
            result = checker.check(materialize(task, f"reference-{run}", case["reference"]))
            if not result["hardgate_pass"] or result["core_science"] != 40 or result["direction"] != 15:
                failures.append(f"{task}:reference-{run}")
        empty = checker.check(materialize(task, "empty", {}))
        wrong = checker.check(materialize(task, "wrong", case["wrong"]))
        if empty["hardgate_pass"] or empty["core_science"] == 40: failures.append(f"{task}:empty")
        if wrong["hardgate_pass"] or wrong["core_science"] == 40: failures.append(f"{task}:wrong")
    if failures:
        print("FAIL", *failures, sep="\n"); return 1
    print("PASS: four tasks x (3 reference + empty + scientific-wrong)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
