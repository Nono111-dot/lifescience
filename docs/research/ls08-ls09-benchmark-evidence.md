# LS08–LS09 benchmark evidence audit

Audit date: 2026-08-14. This note separates material actually published by the three approved benchmarks from evaluator additions. No missing liquid-handling parameters or hidden answers are inferred.

## Frozen sources inspected

| Benchmark | Frozen source | What was inspected |
|---|---|---|
| CompBioBench v1 | [`Genentech/compbiobench-data-v1`](https://huggingface.co/datasets/Genentech/compbiobench-data-v1), dataset revision shown by HF as `c673f0855fce09d320f1677f168f7864eec52c1a`; local manifest SHA-256 `AC8A5DCF813E9E89556701648140A84B2757FE449E35650168DE54BAED75CE1C` | all 100 manifest rows; the two LS08 rows and their four data files |
| CompBioBench runner/leaderboard | [`Genentech/compbiobench-runner`](https://github.com/Genentech/compbiobench-runner) commit `dc350ed37ccd7d7ce96347d139f06dc4bf283f26`; [`compbiobench-leaderboard-v1`](https://huggingface.co/spaces/Genentech/compbiobench-leaderboard-v1) commit `6a63e6d2cae531d9e9bf46b341606ed6b304ba3f` | isolation instructions, output contract, public leaderboard code and files |
| BixBench | [`futurehouse/BixBench`](https://huggingface.co/datasets/futurehouse/BixBench), downloaded `BixBench.jsonl` SHA-256 `0D1204DCDAE7193A9132CED5A3502008F6B3B163DEBC1B65B2AA2D86CB132DC9` | every JSONL record, including prompts and metadata; case-insensitive search for Opentrons, pipetting, dilution, liquid handling and plate-map concepts |
| BioAgentBench | [`bioagent-bench/bioagent-bench`](https://github.com/bioagent-bench/bioagent-bench) commit `6d098b602b8a8fdc33a9d25e410a502be7ed9ce0` | all task metadata and the complete `tasks/single-cell/` workflow/results-generation code |

CompBioBench explicitly says that questions should run in isolated workspaces with web access and that official evaluation is whitespace-stripped **exact string match**. Its public question/data repository and public leaderboard do not publish the answer key or per-question verifier. BioAgentBench also warns that its generated “truth” should not be assumed correct unless explicitly stated.

## LS08 findings

### `ls08-multiome-column-match`

Benchmark provenance is confirmed: CompBioBench `multiome-match-atac-rna-q1` supplies the two files already present in the repository. The official task requires an eight-element, zero-based RNA-to-ATAC permutation. It marks `internet_required=True` and asks for a single semicolon-separated exact-match answer.

What the benchmark provides:

- the exact original prompt;
- RNA TPM (`genes × 8 populations`) and ATAC 10-kb-bin counts (`bins × 8 populations`);
- the expected answer shape and direction (RNA column index → ATAC column index);
- a bijection by construction.

What it does **not** publicly provide:

- the hidden eight-value permutation;
- a gene-coordinate/reference bundle needed for a pinned offline gene-activity calculation;
- a reference script, score matrix, tolerance, or public verifier;
- `column_mapping.csv`, `score_matrix.csv`, `analysis.py`, or `report.md` schemas. Those are local extensions, not benchmark artifacts.

**Readiness: blocked for formal 80-point scoring.** The existing two input files are runnable under the original exact-answer benchmark, but an independently accepted 80-point oracle cannot be produced from the published evidence alone. A formal run requires either (a) the curator-supplied hidden answer/verifier plus its provenance, or (b) a version-pinned annotation/reference and a reviewer-approved derivation whose result is independently reconciled with the official hidden answer. An agent-derived permutation must not be promoted to gold merely because it looks plausible.

### `ls08-enhancer-promoter-integration`

Benchmark provenance is confirmed: CompBioBench `ep-interactions-q1` supplies the Hi-C-like and CRISPR-expression CSVs already present. The original prompt says there are eight candidates `EP1–EP8`, but both supplied files contain only `EP1–EP7`, and the choices are A–G. This is a source-level inconsistency that the local card must disclose rather than silently repair.

What the benchmark provides:

- 200 background Hi-C rows and candidate rows `EP1–EP7`;
- control/perturbed RNA counts for four guides and three replicates per candidate;
- an exact-answer choice A–G;
- no internet requirement.

What it does **not** publicly provide:

- the hidden answer;
- the rule used to combine contact and perturbation evidence;
- normalization, uncertainty, ranking, or tie-breaking rules;
- a public reference implementation or verifier;
- the local expanded artifact schemas.

The data make one candidate visibly discordant, so the task is useful for a dry run or expert adjudication. That observation is not a substitute for the unpublished official key or for a predeclared 40-point combined-support rule.

**Readiness: blocked for formal 80-point scoring; usable only as a clearly labelled calibration/dry-run task.** Do not mark `scientific_checks.py` as accepted until the official answer is obtained and an independent reviewer approves a non-post-hoc combination rule and its tolerances.

## LS09 findings

### Search result across all three benchmarks

No Opentrons, robotic pipetting, liquid-handling, dilution-recovery, serial-dilution, assay-plate, or plate-map task was found in the complete CompBioBench manifest or BixBench JSONL. BioAgentBench contains ten end-to-end bioinformatics pipelines; its single-cell task is human skeletal-muscle scRNA-seq clustering, cell-type annotation and differential expression. It is not laboratory automation and supplies no Opentrons or dilution reference.

Therefore neither current LS09 task originates in, or can be completed from, the three approved benchmarks.

### `ls09-opentrons-sop`

The local `sop.md` and `labware.csv` are custom fixtures. They do not specify a complete executable protocol environment: robot model, API version, pipette and mount, module/labware loading relationship, source wells and starting volumes, destination mapping, tip inventory, aspiration/dispense geometry, or the fixed simulator/runtime. The three benchmarks supply none of these missing values.

**Readiness: blocked; no formal or calibration run.** Filling those fields by evaluator judgement would create a new custom task, contrary to the instruction not to invent missing benchmark material.

### `ls09-plate-dilution-recovery`

The three local CSVs are custom fixtures. They state only two target conditions, two pipette ranges and a stopped-well log entry. They do not contain the actual plate map, completed transfer ledger, source/intermediate concentrations and remaining volumes, solvent constraints, intermediate-dilution design, or a benchmark reference recovery plan. The three benchmarks supply none of these missing values.

**Readiness: blocked; no formal or calibration run.** A “correct” recovery plan cannot be uniquely reconstructed without inventing experimental state.

## Decision table

| Task | Input provenance | Official answer/verifier public? | Can prepare formal oracle now? | Scheduling decision |
|---|---|---:|---:|---|
| `ls08-multiome-column-match` | CompBioBench confirmed | No | No | block; request key/verifier and pinned annotation |
| `ls08-enhancer-promoter-integration` | CompBioBench confirmed, source says EP1–EP8 but files/choices contain EP1–EP7 | No | No | calibration only after card discloses inconsistency; formal block |
| `ls09-opentrons-sop` | no match; custom fixture | No | No | block and replace with a benchmark-grounded task, or formally authorize new task construction |
| `ls09-plate-dilution-recovery` | no match; custom fixture | No | No | block and replace with a benchmark-grounded task, or formally authorize new task construction |

No task-local oracle was implemented in this audit: doing so would require inventing an unpublished key, a post-hoc scoring rule, or missing wet-lab state. Existing fail-closed oracle entry points should remain blocked.
