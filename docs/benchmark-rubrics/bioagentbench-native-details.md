# BioAgentBench single-cell: native task and selected-set provenance audit

Audit date: 2026-08-14

Upstream inspected at Git commit `6d098b602b8a8fdc33a9d25e410a502be7ed9ce0`:

- `README.md`
- `src/task_metadata.json`
- `src/dataset.py`
- `tasks/single-cell/run_analysis.py`
- `tasks/single-cell/run_script.sh`
- `tasks/single-cell/environment.yml`
- official OSF result archive linked by the metadata

The upstream repository license file is **CC BY 4.0**. Dataset-specific upstream terms may also apply and must be checked before redistribution.

## Relationship to the current 25 selected tasks

The current `docs/selected-tasks-v1.tsv` contains:

- 9 BixBench-derived rows,
- 9 CompBioBench-derived rows,
- 7 custom/new-fixture rows,
- **0 rows whose declared upstream is BioAgentBench**.

No selected `upstream_id` equals BioAgentBench's `single-cell` task ID. No current input directory contains the six skeletal-muscle 10X sample accessions used by that task (`GSM6611295`–`GSM6611300`). Therefore none of the 25 tasks is a direct copy, subset, or verified derivative of BioAgentBench single-cell.

The following current tasks are topically adjacent but must **not** be relabelled as BioAgentBench sources:

| current task | declared source | overlap in topic only | decisive difference |
|---|---|---|---|
| `ls04-differential-composition` | CompBioBench | single-cell preprocessing / cell types | Retinal composition-depletion question, not skeletal-muscle exercise response. |
| `ls04-perturbseq-reference-map` | CompBioBench | single-cell data and guide-linked expression | Perturb-seq guide mapping, not clustering/annotation/pre-post DE. |
| `ls04-spatial-deconvolution` | CompBioBench | cell-type inference | Spatial spot deconvolution, not dissociated muscle scRNA-seq. |
| `ls08-multiome-column-match` | CompBioBench | single-cell multi-omics | RNA–ATAC column matching, not RNA-only muscle analysis. |

Conclusion: BioAgentBench was considered during benchmark review, but it contributed **no actual selected question or input** to the current 25-task manifest.

## Native BioAgentBench single-cell task

### Native prompt

`src/task_metadata.json` defines one end-to-end task, `single-cell`:

> Analyze single-cell RNA-seq data from pre- and post-exercise skeletal muscle samples. Perform clustering, cell type identification, and differential expression analysis within each cell type between conditions.

The requested native output is a CSV with:

```text
cluster_id,predicted_cell_type,gene_name,logfoldchanges,pvals,pvals_adj,direction,abs_logfc
```

The metadata includes one illustrative example row. That example is part of the prompt/schema and is not a general grading rule.

The README expands the intended workflow to quality control, normalization, dimensionality reduction, clustering, marker-based cell-type identification, and within-cell-type pre/post differential expression. It asks for all differentially expressed genes across cell types with predicted cell type and direction.

### Native inputs and reference material

The pipeline uses six human skeletal-muscle 10X samples, three subjects with paired pre/post acute-exercise samples:

| subject | pre | post |
|---|---|---|
| 1 | GSM6611295 | GSM6611296 |
| 2 | GSM6611297 | GSM6611298 |
| 3 | GSM6611299 | GSM6611300 |

For each sample, the task downloads Matrix Market counts, barcodes and feature files. It also downloads `Cell_marker_Seq.xlsx` as its cell-marker reference. The repository's scripts fetch these resources live; the code does not state database release identifiers or expected hashes.

`environment.yml` names packages such as Scanpy, AnnData, Leiden, igraph, scipy and scikit-learn but does not pin versions. Consequently the environment file is not a complete reproducibility lock.

### Native truth/results

`src/task_metadata.json` labels an OSF archive as `results`, not as a separately curated biological truth set. The inspected archive:

- is 6,443 bytes compressed;
- has SHA-256 `7e5d83f06b4ea4458a1ef281b27597aa6025621893f5403e595ae7400912d672` as downloaded on 2026-08-14;
- contains only `results/all_clusters_de_genes.csv`;
- contains 163 data rows and the eight requested columns;
- contains reference-pipeline calls from 11 reported cluster/cell-type combinations.

Reported cell-type labels in that file include Endothelial cell, Fibroblast, Smooth muscle cell, Dendritic cell, Macrophage, B cell and Natural killer cell. These are **pipeline outputs**, not independently curated cell-level truth labels.

The repository README explicitly warns not to expect its “Truth” files or evaluations to be correct unless explicitly stated. The single-cell material is not identified as consensus ground truth, simulated truth, or independently adjudicated truth.

## What the reference pipeline actually does

The native `run_analysis.py` is a reproducibility script for its reference result, not a hidden evaluator. Its material choices include:

- concatenate the six samples with sample/condition/subject metadata;
- calculate QC metrics;
- filter cells at at least 300 genes, at most 15% mitochondrial counts, total counts at least 1,000 and at most 15,000;
- retain genes present in at least 20 cells;
- normalize each cell to 10,000 counts and log-transform;
- select 2,000 highly variable genes, scale, PCA, 20-neighbour graph using 30 PCs;
- Leiden clustering at resolution 0.3, three iterations;
- annotate clusters by a custom weighted match against `Cell_marker_Seq.xlsx`;
- run Scanpy Wilcoxon pre/post DE within each cluster with Bonferroni correction and adjusted p-value below 0.05, requiring at least five cells per condition;
- collate significant rows to `all_clusters_de_genes.csv`.

Important limitations for evaluation use:

- Package versions and random seeds are not pinned.
- The marker database is downloaded live and is not release-pinned.
- Cell-type annotations are generated by the same heuristic pipeline that produces the reference CSV.
- Subjects are paired in the biological design, but the within-cluster DE implementation groups cells by condition and does not model subject pairing or donor-level pseudoreplication.
- Clustering labels are arbitrary and may permute across valid reruns.
- Different valid QC, integration, annotation and DE approaches can produce non-identical but scientifically reasonable results.

## Native evaluation method versus a proposed extended rubric

| aspect | native BioAgentBench material | proposed use in this project |
|---|---|---|
| Evaluation executable | No independent single-cell scorer was found in the inspected repository. | A new static/deterministic oracle would have to be written and acceptance-tested. It must be labelled a project extension, not native BioAgentBench. |
| Reference artifact | One 163-row `all_clusters_de_genes.csv` produced by `run_analysis.py`. | May serve as a calibration/reference-pipeline artifact after reproduction, never as unquestioned biological truth. |
| Comparison rule | README says non-consensus tasks may be evaluated for correctness and “at least some overlapping outputs,” but supplies no single-cell formula, threshold or tolerance. | Predeclare label matching, gene-list overlap/precision-recall, direction agreement, numeric tolerances and allowed alternative labels; do not invent them after seeing agent output. |
| QC / normalization | Present in the reference script; absent from the final result CSV. | Require separate QC and method artifacts if these steps are to receive deterministic credit. |
| Clustering | Reference Leiden result; cluster IDs appear in result CSV. | Never compare raw cluster numbers directly. Use a permutation-invariant mapping or compare biologically interpretable label sets. |
| Cell types | Heuristic marker-database labels in the reference CSV. | Review marker evidence and define synonym/ontology handling; consider label-set/Jaccard scoring only after domain review. |
| Differential expression | Reference significant-gene rows and continuous statistics. | Score gene-ID coverage, direction and a predeclared top-K/set overlap; exact full-row equality is not scientifically justified by the native benchmark. |
| Reproducibility | Docker/Conda recipes exist, but versions/resources/seeds are not frozen. | Freeze data/reference hashes, versions, seed and a reviewed rerun before formal use. |
| Report quality | Not part of the native output contract. | Can be added as this project's blind JudgeScore, clearly marked non-native. |

There is no native `eval_mode`, per-field score allocation, numeric tolerance, hard-gate definition or pass threshold for this task in the inspected repository. Any Coverage 10 / core 40 / direction 15 / summary 5 / script 10 mapping would be a **new evaluation design**, not a recovered native rubric.

## Replacement-candidate assessment

### Scientific fit

This task is a plausible replacement candidate if the project wants a genuine end-to-end single-cell workflow covering:

- raw 10X ingestion and QC;
- normalization and dimension reduction;
- unsupervised clustering;
- marker-supported cell-type annotation;
- condition-specific DE within cell types;
- integration of a multi-stage workflow into one artifact.

It is closest to the intended LS04 single-cell-analysis capability area, but it does not test spatial deconvolution, Perturb-seq mapping, differential composition, or multiome RNA–ATAC matching. Replacing any of those tasks would change the scientific construct being measured and requires an explicit selection decision.

It is not a drop-in candidate for the current LS06–LS10 formal-run subset. Using it there would change both domain allocation and experimental scope.

### Readiness as a replacement

Current verdict: **candidate, not ready**.

Before selection it would require:

1. Downloading and hashing the six-sample data and marker reference under verified redistribution terms.
2. Pinning all package versions, random seeds and the marker-database release.
3. Independently rerunning and reviewing the native pipeline.
4. Auditing the paired-subject design and deciding whether to preserve the native cell-level Wilcoxon analysis or replace it with an approved donor-aware method. A replacement would be a derived task, not a native reproduction.
5. Defining a permutation-invariant, synonym-aware comparison rather than exact cluster-ID matching.
6. Predeclaring gene-list overlap/direction metrics and tolerances using reference, empty and scientifically wrong submissions.
7. Adding strict output contracts for QC, cluster/cell-type evidence, DE results, script and report if the project's 80+20 framework is used.
8. Passing 3/3 reference, empty and deliberate-error acceptance tests plus a second domain review.

Until those steps are complete, the native result archive can support exploratory calibration and rubric design, but not a formal deterministic score.

## Provenance conclusion

- Current selected questions actually sourced from BioAgentBench single-cell: **0/25**.
- BioAgentBench single-cell is an end-to-end workflow task with a reproducible reference script and downloadable result artifact.
- It does not ship an independently curated truth set or an explicit scoring implementation for this task.
- It may be considered as a future LS04 replacement only after an explicit scope decision and substantial grader/resource hardening.
