# Task card: `ls07-combination-treatment-mechanism`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls07-combination-treatment-mechanism`

- Inputs: the three LS07 expression files plus `Reactome_2022.gmt`, `Reactome_2022.background.txt`, and `Reactome_2022.manifest.json`. The official Enrichr-named snapshot contains 1,818 pathways and its explicit local background contains 10,489 unique gene symbols. No remote or newer library is a valid substitute.
- Prompt: **Using the frozen differential-expression rule, `Reactome_2022.gmt`, and `Reactome_2022.background.txt`, identify the best-supported primary mechanism of the combination treatment. Do not query a remote enrichment service or substitute a different release/background. Write `output/pathway_enrichment.csv` with `pathway_id,pathway_name,overlap,p_value,padj,direction`, `output/mechanism_call.json`, `output/analysis.py`, and `output/report.md` (maximum 600 words). Distinguish enrichment from demonstrated causation.**
- Deliverables: pathway table with declared tested universe/release; mechanism JSON referencing a table row; report; rerunnable script. Missing statistics are empty/null.
- Hard gates: exact pinned gene-set release and universe used; corrected enrichment statistics valid; mechanism call supported by a reported row; no causal overclaim.
- Deterministic 80: coverage/schema 10; overlap/statistics/ranking and primary mechanism 40 against the pinned reference; evidence direction/restraint 15; summary consistency 5; static/rerunnable script 10.
- Ablation expectation: `[pathway-analysis]`, `[gene-set-reference]`, `[network-interpretation]`, `[reproducible-code]`; expected to reduce stale-release, universe and causal-language errors.
- Readiness closure: the Reactome library/background, DE mapping, complete 1,818-pathway enrichment table and top-mechanism call are frozen in the task-local oracle; local results are explicitly separated from historical live-Enrichr anchors.
