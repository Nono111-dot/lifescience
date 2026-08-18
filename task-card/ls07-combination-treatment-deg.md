# Task card: `ls07-combination-treatment-deg`

> Canonical participant-facing standalone card. The packaged-input inventory below matches the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls07-combination-treatment-deg`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 1,193 bytes
- `inputs/counts_raw_unfiltered.csv` — 6,016,681 bytes
- `inputs/ensg_to_gene_name.tsv` — 2,360,408 bytes
- `inputs/sample_layout.csv` — 2,860 bytes

**Total:** 8,381,142 bytes (7.99 MiB).

### Prompt

> Use the files in `inputs/` to perform differential-expression analysis for `Cisplatin_IC50_CBD_IC50` versus `DMSO`. Use only the three replicates from each of those groups, with combination treatment as numerator and DMSO as denominator, and use `Group` as the only design term. Before fitting, retain genes for which at least one of the six selected samples has a raw count greater than 10. Use PyDESeq2 0.5.0 with `refit_cooks=True` and the standard `DeseqStats` contrast. A gene passes when `padj < 0.05`, `abs(log2FoldChange) > 0.5`, and `baseMean > 10`.
>
> Write all results under `output/`: `differential_expression.csv`, `summary.json`, `analysis.py`, and `report.md`. Do not use samples from other groups. Preserve unavailable adjusted p-values as null rather than converting them to zero. The report must be no more than 500 words and distinguish statistical association from causation.
- Deliverables: unique gene rows; JSON count and explicit contrast/design metadata; report; rerunnable script. CSV missing numeric values are empty.
- Hard gates: design and contrast recorded exactly; gene IDs unique; threshold rule uses strict inequalities exactly; summary count equals passing rows.
- Deterministic 80: coverage/schema 10; frozen reference values and pass count 40 using the pinned DESeq2 environment/tolerances; direction/threshold decision 15; summary consistency 5; static/rerunnable script 10.
- Ablation expectation: `[transcriptome-analysis]`, `[experimental-design]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce contrast, filtering and provenance errors.
- Readiness closure: the prompt-authoritative PyDESeq2 0.5.0 analysis, full-row reference, 555-gene threshold result and 677/679 upstream discrepancy adjudication are frozen in the task-local oracle.
