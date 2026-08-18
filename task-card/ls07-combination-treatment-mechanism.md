# Task card: `ls07-combination-treatment-mechanism`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls07-combination-treatment-mechanism`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 1,692 bytes
- `inputs/Reactome_2022.background.txt` — 65,942 bytes
- `inputs/Reactome_2022.gmt` — 778,913 bytes
- `inputs/Reactome_2022.manifest.json` — 1,515 bytes
- `inputs/counts_raw_unfiltered.csv` — 6,016,681 bytes
- `inputs/ensg_to_gene_name.tsv` — 2,360,408 bytes
- `inputs/sample_layout.csv` — 2,860 bytes

**Total:** 9,228,011 bytes (8.80 MiB).

### Prompt

> Using the files in `inputs/`, perform the approved `Cisplatin_IC50_CBD_IC50` versus `DMSO` differential-expression analysis and enrichment with GSEApy 1.1.4 against the evaluator-supplied frozen `Reactome_2022` resource and supplied background universe. Identify the best-supported primary cellular mechanism. Do not download or substitute a current pathway library or identifier mapping.
>
> Write all results under `output/`: `pathway_enrichment.csv`, `mechanism_call.json`, `resource_manifest.json`, `analysis.py`, and `report.md`. The report must be no more than 500 words and must distinguish pathway enrichment from demonstrated causation.
- Deliverables: pathway table with declared tested universe/release; mechanism JSON referencing a table row; report; rerunnable script. Missing statistics are empty/null.
- Hard gates: exact pinned gene-set release and universe used; corrected enrichment statistics valid; mechanism call supported by a reported row; no causal overclaim.
- Deterministic 80: coverage/schema 10; overlap/statistics/ranking and primary mechanism 40 against the pinned reference; evidence direction/restraint 15; summary consistency 5; static/rerunnable script 10.
- Ablation expectation: `[pathway-analysis]`, `[gene-set-reference]`, `[network-interpretation]`, `[reproducible-code]`; expected to reduce stale-release, universe and causal-language errors.
- Readiness closure: the Reactome library/background, DE mapping, complete 1,818-pathway enrichment table and top-mechanism call are frozen in the task-local oracle; local results are explicitly separated from historical live-Enrichr anchors.
