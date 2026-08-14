from __future__ import annotations

import ast
import csv
from pathlib import Path

# BLOCKED after codex/C0 trial-2: the evaluation environment does not contain
# the pinned Opentrons simulator required by the card. Do not score formal runs
# until the simulator contract is frozen and the regression suite is rerun.
ACCEPTED = False

WELLS = [f"{row}{col}" for col in range(1, 7) for row in "ABCD"]
STAGES = {
    "lysis": ("reagents:A1", 80.0),
    "beads": ("reagents:A2", 120.0),
    "supernatant": (None, 250.0),
    "wash1_add": ("reagents:A3", 180.0),
    "wash1_remove": (None, 180.0),
    "wash2_add": ("reagents:A3", 180.0),
    "wash2_remove": (None, 180.0),
    "elution": ("reagents:A4", 40.0),
}
TIP_POLICY = {
    "lysis": "fresh_lysis_tip",
    "beads": "fresh_bead_tip",
    "supernatant": "fresh_supernatant_tip",
    "wash1_add": "fresh_wash1_tip",
    "wash1_remove": "reuse_wash1_tip",
    "wash2_add": "fresh_wash2_tip",
    "wash2_remove": "reuse_wash2_tip",
    "elution": "fresh_elution_tip",
}


def _read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def check(workspace: Path):
    output = workspace / "output"
    failures = []
    criteria = {}

    try:
        rows = _read_csv(output / "transfer_plan.csv")
    except Exception:
        rows = []
    required_cols = {"step", "source", "destination", "volume_uL", "pipette", "tip_policy"}
    headers_ok = bool(rows) and required_cols.issubset(rows[0])
    observed = {}
    numeric_ok = True
    if headers_ok:
        for row in rows:
            try:
                volume = float(row["volume_uL"])
            except (TypeError, ValueError):
                numeric_ok = False
                continue
            parts = row["step"].split(":", 1)
            if len(parts) != 2:
                numeric_ok = False
                continue
            observed[(parts[0], parts[1])] = (row, volume)

    exact = headers_ok and numeric_ok and len(rows) == 192 and len(observed) == 192
    balance_ok = exact
    pipette_ok = exact
    tips_ok = exact
    if exact:
        for well in WELLS:
            for stage, (source, volume) in STAGES.items():
                row, got_volume = observed.get((stage, well), ({}, -1.0))
                expected_source = f"processing:{well}" if source is None else source
                expected_dest = "waste:A1" if stage in {"supernatant", "wash1_remove", "wash2_remove"} else f"processing:{well}"
                if row.get("source") != expected_source or row.get("destination") != expected_dest or abs(got_volume - volume) > 1e-6:
                    balance_ok = False
                if row.get("pipette") != "p300_single_gen2" or not (20 <= got_volume <= 300):
                    pipette_ok = False
                if row.get("tip_policy", "") != TIP_POLICY[stage]:
                    tips_ok = False

    protocol_ok = False
    protocol_text = ""
    try:
        protocol_text = (output / "protocol.py").read_text(encoding="utf-8")
        tree = ast.parse(protocol_text)
        required_tokens = [
            '"2.16"', "p300_single_gen2", "nest_12_reservoir_15ml",
            "nest_96_wellplate_2ml_deep", "opentrons_96_tiprack_300ul",
            "magnetic module gen2", '"4"', '"7"', ".engage(", ".disengage(", ".delay(",
        ]
        protocol_ok = isinstance(tree, ast.Module) and all(token in protocol_text for token in required_tokens)
    except Exception:
        protocol_ok = False

    simulation_text = ""
    try:
        simulation_text = (output / "simulation.txt").read_text(encoding="utf-8").lower()
    except Exception:
        pass
    simulation_ok = "simulation completed without errors" in simulation_text and "192 transfer rows validated" in simulation_text

    report_text = ""
    try:
        report_text = (output / "report.md").read_text(encoding="utf-8").lower()
    except Exception:
        pass
    summary_ok = all(term in report_text for term in ["24 samples", "192", "144 tips", "simulation completed"])

    criteria.update({
        "exact_192_transfer_contract": exact,
        "liquid_balance_and_well_mapping": balance_ok,
        "pipette_range": pipette_ok,
        "tip_policy": tips_ok,
        "protocol_static_contract": protocol_ok,
        "simulation_record": simulation_ok,
        "report_consistency": summary_ok,
    })
    for name, ok in criteria.items():
        if not ok:
            failures.append("LS09_SOP_" + name.upper())

    core = 0
    core += 16 if exact else 0
    core += 12 if balance_ok else 0
    core += 6 if pipette_ok else 0
    core += 6 if tips_ok else 0
    direction = (8 if protocol_ok else 0) + (7 if simulation_ok else 0)
    summary = 5 if summary_ok else 0
    hardgate = exact and balance_ok and pipette_ok and tips_ok and protocol_ok and simulation_ok
    return {"core_science": core, "direction": direction, "summary": summary,
            "hardgate_pass": hardgate, "failure_codes": failures, "criteria": criteria}
