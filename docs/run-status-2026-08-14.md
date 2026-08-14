# Life-science evaluation status — 2026-08-14

## Outcome

The evaluation framework has been run in fail-closed mode. Four Codex C0 calibration workspaces were created, frozen, hashed, and scored. No run is labelled as a formal headline result because the desktop/UI harness and full LS06–LS10 readiness gates are not yet satisfied.

The calibration uncovered two genuine task/grader defects and verified their correction for `ls09-plate-dilution-recovery`. This is task validation evidence, not a Codex-versus-Duanyan comparison.

## Saved calibration results

| Task | Trial | Deterministic | Hard gate | Interpretation |
|---|---:|---:|---|---|
| `ls09-opentrons-sop` | 1 | 28/80 | fail | Found unsafe 72-tip gold assumption; Codex correctly calculated 144 tips and aborted against the original 96-tip fixture. The fixture/gold were revised. |
| `ls09-opentrons-sop` | 2 | 28/80 | fail | The revised fixture fixed tip capacity, but exposed undefined transfer-plan granularity and an unavailable pinned Opentrons simulator. This task remains blocked; the score is not a model-quality conclusion. |
| `ls09-plate-dilution-recovery` | 1 | 45/80 | fail | Found an exact-string false negative and an ambiguous one-pipette-field schema for two physical transfers. The contract/oracle were revised. |
| `ls09-plate-dilution-recovery` | 2 | 80/80 | pass | Correctly recovered only B2/B3, preserved completed wells, satisfied dilution balance, P20/P300 feasibility, inventory and report consistency. |

All four workspaces have append-only result directories containing `FROZEN_MANIFEST.sha256.tsv`, `oracle.json`, and `run-metadata.json`. The human-readable aggregate is `results/summary.md` (ignored by git because run evidence is local and may be large).

## Four formerly custom tasks

The following are now explicitly **source-supported local extensions**, not benchmark-native questions:

- `ls05-structure-model-ranking`: independent gold/checker plus reference, empty and wrong controls; 3/3 tests pass.
- `ls05-low-confidence-pocket`: independent gold/checker plus reference, empty and wrong controls; 3/3 tests pass.
- `ls09-plate-dilution-recovery`: corrected contract/checker; reference, semantic-regression, empty/wrong and ambiguous-pipette controls pass.
- `ls09-opentrons-sop`: scientifically improved tip accounting, but remains blocked pending an unambiguous plan contract and a pinned runnable Opentrons simulator.

LS05 scientific sources and boundaries are in `docs/ls05-local-extension-provenance.md`. LS09 sources and boundaries are in `docs/research/ls09-local-extension-provenance.md`.

## Why this is not yet a formal comparison

1. The controlling Feishu workflow requires a real new UI conversation for every run. The current process could not launch the WindowsApps Codex executable (`Access denied`), so isolated Codex subagents were used only for calibration.
2. Duanyan UI login, actual client/model/build, capability inventory export, autonomous installation trace, and post-run capability reset cannot be observed through the current repository interface. No Duanyan score has been fabricated.
3. The LS06–LS10 preflight still has missing/unaccepted scientific checkers outside the repaired LS09 recovery task.
4. `ls09-opentrons-sop` needs a fixed simulator environment and a contract that explicitly distinguishes net liquid-transfer stages from mix strokes.

## Required next formal step

Run `scripts/audit-evaluation-readiness.ps1` and require every scheduled row to be `formal_ready=true`. Then execute each accepted task in a fresh Codex UI and Duanyan UI workspace, capture wall time and capability/reset inventories, freeze with `scripts/freeze-and-score.ps1 -Mode formal`, and blind-judge only the report artifacts. A normally ending UI with no artifact remains a harness failure.

