# Task card: `ls06-eno1-significance-audit`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls06-eno1-significance-audit`

### Inputs (authoritative packaged inventory)
- `inputs/MeRIP_RNA_result.xlsx` — 1,155,180 bytes
- `inputs/Proteomic_data .xlsx` — 646,418 bytes
- `inputs/README.md` — 970 bytes

**Total:** 1,802,568 bytes (1.72 MiB).

- Prompt: **Retrieve ENO1's adjusted p-value from the supplied proteomics results and give a threshold-calibrated interpretation at FDR 0.05. Write `output/eno1_significance.json` with `gene,adjusted_p_value,fdr_threshold,significant,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. Do not relabel a raw p-value as adjusted.**
- Deliverables: one JSON object; report; rerunnable script. `significant` is a JSON boolean.
- Hard gates: exact ENO1/source; adjusted rather than raw p-value; finite p in `[0,1]`; boolean agrees with FDR 0.05.
- Deterministic 80: coverage/schema 10; adjusted p-value 40 (absolute tolerance `0.0005`); FDR decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[tabular-analysis]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce wrong-column and raw-versus-adjusted-p errors.
