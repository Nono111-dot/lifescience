# Task card: `ls06-eno1-significance-audit`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls06-eno1-significance-audit`

- Inputs: the same two workbooks and roles as the preceding card; the MeRIP workbook remains a decoy. Target sheet exposes both raw and adjusted p-value columns.
- Prompt: **Retrieve ENO1's adjusted p-value from the supplied proteomics results and give a threshold-calibrated interpretation at FDR 0.05. Write `output/eno1_significance.json` with `gene,adjusted_p_value,fdr_threshold,significant,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. Do not relabel a raw p-value as adjusted.**
- Deliverables: one JSON object; report; rerunnable script. `significant` is a JSON boolean.
- Hard gates: exact ENO1/source; adjusted rather than raw p-value; finite p in `[0,1]`; boolean agrees with FDR 0.05.
- Deterministic 80: coverage/schema 10; adjusted p-value 40 (absolute tolerance `0.0005`); FDR decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[tabular-analysis]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce wrong-column and raw-versus-adjusted-p errors.
