import csv
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("checker", HERE / "scientific_checks.py")
checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)


def make_reference(root: Path, wrong=False, legacy_72_tips=False):
    out = root / "output"; out.mkdir(parents=True, exist_ok=True)
    fields = ["step", "source", "destination", "volume_uL", "pipette", "tip_policy"]
    with (out / "transfer_plan.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields); w.writeheader()
        for well in checker.WELLS:
            for stage, (source, volume) in checker.STAGES.items():
                if wrong and stage == "lysis" and well == "A1": volume = 81
                w.writerow({"step": f"{stage}:{well}", "source": source or f"processing:{well}",
                            "destination": "waste:A1" if stage in {"supernatant","wash1_remove","wash2_remove"} else f"processing:{well}",
                            "volume_uL": volume, "pipette": "p300_single_gen2",
                            "tip_policy": ("fresh_wash_tip" if stage in {"wash1_add","wash2_add"} else "fresh_sample_tip") if legacy_72_tips else checker.TIP_POLICY[stage]})
    (out / "protocol.py").write_text('metadata={"apiLevel":"2.16"}\n# p300_single_gen2 nest_12_reservoir_15ml nest_96_wellplate_2ml_deep opentrons_96_tiprack_300ul magnetic module gen2 "4" "7"\ndef run(p):\n p.engage(); p.delay(minutes=1); p.disengage()\n', encoding="utf-8")
    (out / "simulation.txt").write_text("Simulation completed without errors; 192 transfer rows validated\n", encoding="utf-8")
    tip_count = 72 if legacy_72_tips else 144
    (out / "report.md").write_text(f"24 samples; 192 transfers; {tip_count} tips; simulation completed.\n", encoding="utf-8")


def test_acceptance_three_runs_and_negative_controls():
    reference = HERE / "testdata" / "reference"
    wrong = HERE / "testdata" / "wrong"
    legacy = HERE / "testdata" / "legacy_72_tips"
    empty = HERE / "testdata" / "empty"
    for _ in range(3):
        make_reference(reference)
        result = checker.check(reference)
        assert result["hardgate_pass"] and result["core_science"] == 40 and result["direction"] == 15 and result["summary"] == 5
    make_reference(wrong, wrong=True)
    assert not checker.check(wrong)["hardgate_pass"]
    assert not checker.check(empty)["hardgate_pass"]
    make_reference(legacy, legacy_72_tips=True)
    legacy_result = checker.check(legacy)
    assert not legacy_result["hardgate_pass"]
    assert "LS09_SOP_TIP_POLICY" in legacy_result["failure_codes"]


def test_trial2_is_frozen_as_contract_regression_not_agent_science_error():
    regression = json.loads((HERE / "regressions" / "codex-c0-trial-2.json").read_text(encoding="utf-8"))
    assert regression["observed_transfer_plan_rows"] == 1032
    assert regression["environment_error"] == "ModuleNotFoundError: No module named 'opentrons'"
    assert regression["agent_release_decision"] == "ABORT BEFORE EXECUTION"
    assert regression["review"]["plan_row_failure_attributable_to_agent"] is False
    assert regression["review"]["simulation_failure_attributable_to_agent"] is False
    assert checker.ACCEPTED is False


if __name__ == "__main__":
    test_acceptance_three_runs_and_negative_controls()
    test_trial2_is_frozen_as_contract_regression_not_agent_science_error()
    print("PASS: unit controls; trial-2 frozen as contract regression; formal oracle BLOCKED")
