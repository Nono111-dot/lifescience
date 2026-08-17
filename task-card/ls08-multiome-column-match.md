# Task card: `ls08-multiome-column-match`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls08-multiome-column-match`

- Inputs: gzipped ATAC-bin table (15,259,355 bytes) and RNA-TPM table (1,432,352 bytes), eight populations per modality. Provenance: Genentech CompBioBench data at the frozen 2026-08-14 `main` retrieval; column permutation is hidden from the agent.
- Prompt: **Recover the one-to-one matching between the eight permuted ATAC population columns and RNA populations. Write `output/column_mapping.csv` with `rna_population,atac_column,match_score,runner_up_score`, `output/score_matrix.csv`, `output/analysis.py`, and `output/report.md`. Enforce a bijection and explain the shared biological signal used.**
- Deliverables: eight unique mapping rows; complete finite score matrix; report; rerunnable script. Score definition and preprocessing must be stated.
- Hard gates: all eight labels on each side appear exactly once; mapping is a bijection; all reported scores finite; mapping direction is RNA-to-ATAC.
- Deterministic 80: coverage/schema 10; full score matrix and hidden permutation 40 under the frozen preprocessing/tolerance; bijection/direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[multi-omics-integration]`, `[feature-alignment]`, `[assignment-optimization]`, `[reproducible-code]`; expected to reduce label leakage, many-to-one and normalization errors.
- Readiness closure: feature mapping, top-2,000 RNA variance selection, cosine score matrix and Hungarian one-to-one permutation are frozen in the task-local rule and oracle.
