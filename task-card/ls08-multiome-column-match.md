# Task card: `ls08-multiome-column-match`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls08-multiome-column-match`

### Inputs (authoritative packaged inventory)
- `inputs/MATCHING_RULE.md` — 880 bytes
- `inputs/README.md` — 1,122 bytes
- `inputs/ensembl112_gene_coordinates.tsv` — 4,200,908 bytes
- `inputs/multiome.match.atac.rna.q1.atac.tsv.gz` — 15,259,355 bytes
- `inputs/multiome.match.atac.rna.q1.rna.tsv.gz` — 1,432,352 bytes

**Total:** 20,894,617 bytes (19.93 MiB).

- Prompt: **Recover the one-to-one matching between the eight permuted ATAC population columns and RNA populations. Write `output/column_mapping.csv` with `rna_population,atac_column,match_score,runner_up_score`, `output/score_matrix.csv`, `output/analysis.py`, and `output/report.md`. Enforce a bijection and explain the shared biological signal used.**
- Deliverables: eight unique mapping rows; complete finite score matrix; report; rerunnable script. Score definition and preprocessing must be stated.
- Hard gates: all eight labels on each side appear exactly once; mapping is a bijection; all reported scores finite; mapping direction is RNA-to-ATAC.
- Deterministic 80: coverage/schema 10; full score matrix and hidden permutation 40 under the frozen preprocessing/tolerance; bijection/direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[multi-omics-integration]`, `[feature-alignment]`, `[assignment-optimization]`, `[reproducible-code]`; expected to reduce label leakage, many-to-one and normalization errors.
- Readiness closure: feature mapping, top-2,000 RNA variance selection, cosine score matrix and Hungarian one-to-one permutation are frozen in the task-local rule and oracle.
