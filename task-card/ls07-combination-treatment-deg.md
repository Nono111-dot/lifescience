# Task card: `ls07-combination-treatment-deg`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls07-combination-treatment-deg`

- Inputs: `counts_raw_unfiltered.csv` (raw integer gene-by-sample counts), `sample_layout.csv` (sample/condition design), `ensg_to_gene_name.tsv` (Ensembl-to-symbol support mapping); total 8,443,658 bytes. Provenance: BixBench capsule data; no decoy file.
- Prompt: **Run the frozen combination-treatment contrast against its specified comparator using the sample layout. Write `output/differential_expression.csv` with `gene_id,gene_name,baseMean,log2FoldChange,pvalue,padj,pass`, `output/summary.json` with the number passing `padj<0.05`, `abs(log2FoldChange)>0.5`, and `baseMean>10`, `output/analysis.py`, and `output/report.md`. Preserve independent-filtering missing values as null.**
- Deliverables: unique gene rows; JSON count and explicit contrast/design metadata; report; rerunnable script. CSV missing numeric values are empty.
- Hard gates: design and contrast recorded exactly; gene IDs unique; threshold rule uses strict inequalities exactly; summary count equals passing rows.
- Deterministic 80: coverage/schema 10; frozen reference values and pass count 40 using the pinned DESeq2 environment/tolerances; direction/threshold decision 15; summary consistency 5; static/rerunnable script 10.
- Ablation expectation: `[transcriptome-analysis]`, `[experimental-design]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce contrast, filtering and provenance errors.
- Readiness closure: the prompt-authoritative PyDESeq2 0.5.0 analysis, full-row reference, 555-gene threshold result and 677/679 upstream discrepancy adjudication are frozen in the task-local oracle.
