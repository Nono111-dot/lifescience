# Task card: `ls06-eno1-effect-size`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls06-eno1-effect-size`

### Inputs (authoritative packaged inventory)
- `inputs/MeRIP_RNA_result.xlsx` — 1,155,180 bytes
- `inputs/Proteomic_data .xlsx` — 646,418 bytes
- `inputs/README.md` — 1,248 bytes

**Total:** 1,802,846 bytes (1.72 MiB).

- Prompt: **Using the supplied proteomics results, calculate ENO1 tumor-versus-normal fold change and log2 fold change. Write `output/eno1_effect.json` with `gene,tumor_value,normal_value,fold_change,log2_fold_change,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. State the fold-change direction and do not substitute the unrelated workbook.**
- Deliverables: one JSON object with finite numeric values and source identifiers; UTF-8 Markdown report; rerunnable Python script. No additional artifact is required.
- Hard gates: exact ENO1/source row; all four core values within checker tolerance; fold-change/log2 direction internally consistent; source file and sheet traceable.
- Deterministic 80: coverage/schema 10; Normal, Tumor, fold change and log2 fold change 10 each (raw values relative tolerance `5e-6`, fold change `2e-3`, log2 absolute tolerance `0.011`); direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[tabular-analysis]`, `[workbook-reader]`, `[reproducible-code]`; expected to reduce wrong-sheet, arithmetic and non-rerunnable-output errors without disclosing a route.
