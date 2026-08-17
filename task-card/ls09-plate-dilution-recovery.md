# Task card: `ls09-plate-dilution-recovery`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls09-plate-dilution-recovery`

- Inputs: `dilution_request.csv`, `pipettes.csv`, `plate_map.csv`, `run_log.csv`, `source_inventory.csv`; total 1,112 bytes. They define requested concentrations/volumes, P20/P300 limits, completed/failed wells, transfer history and remaining stocks. Provenance/scientific basis: source-supported synthetic local extension; no patient data and no decoy.
- Prompt: **Diagnose the failed dilution run and produce a physically feasible recovery plan. Write `output/root_cause.json`, `output/recovery_plan.csv` with `step,source,destination,transfer_uL,transfer_pipette,diluent_source,diluent_uL,diluent_pipette,final_concentration,final_volume_uL`, `output/analysis.py`, and `output/report.md`. Enforce pipette ranges, mass balance and supplied solvent/volume limits.**
- Deliverables: structured root cause; one row per required recovery destination; separate pipettes for solute and diluent transfers; report and rerunnable script.
- Hard gates: root cause traceable to the run log; only failed/requested wells are recovered; dilution mass balance and both pipette ranges pass; no source overdraw.
- Deterministic 80: coverage/schema 10; root cause 14, recovery plan 10, concentration/mass balance 10, pipette plus inventory feasibility 6; recover/abort decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[liquid-handling]`, `[mass-balance]`, `[run-log-audit]`, `[reproducible-code]`; expected to reduce double-processing, wrong-pipette and stock-overdraw errors.
