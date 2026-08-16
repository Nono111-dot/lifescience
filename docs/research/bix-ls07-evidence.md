# LS07 benchmark evidence audit (BixBench `bix-43`)

Audit date: 2026-08-14

Resource-remediation update: 2026-08-16

Scope: determine whether the three selected benchmarks already provide enough evidence to freeze the LS07 differential-expression and Reactome tasks. This note records only material present in BixBench v1.5 and its official capsule; absent parameters are not inferred.

## Sources inspected

- Local upstream record: `BixBench.jsonl`, all five records `bix-43-q1` through `bix-43-q5`.
- Official Hugging Face capsule: `CapsuleFolder-15ff11e5-2db1-45b6-b3a3-46bc2a74b821.zip`, downloaded from `futurehouse/BixBench` main on 2026-08-14. Downloaded-file SHA-256: `e2aa7a6fe176807f6e1a61fb7ff395d78570e8bd8e41cf3568501357a92369ae`.
- Executed notebook in that capsule and the three data files already frozen under both LS07 input directories.
- BixBench records cite Zenodo record 8353706 and the associated paper, but neither is used below to fill an unspecified benchmark parameter.

Input SHA-256 values:

| file | SHA-256 |
|---|---|
| `counts_raw_unfiltered.csv` | `c233e3e1c68efea27818d97cc45dd1cceeb0bbb9e8693951b6964cd1a8f6ac17` |
| `ensg_to_gene_name.tsv` | `bcee755a136bec21e8e60886acbbb841751633b67ba786f61e52857295cc9c17` |
| `sample_layout.csv` | `cb0212290186c6c5ecbd4d06f18e7fd0ad93d101ab0f07e7171e566e5cfa2584` |

Case is insignificant; hashes are shown in lowercase elsewhere in the repository.

## What the benchmark actually specifies

### Differential-expression design

The executed notebook supplies the following reproducible analysis intent:

- Input genes are retained when at least one sample has a raw count greater than 10: `(raw_counts > 10).sum(axis=1) > 0`.
- Only the six samples whose IDs match groups 3 and 9 are used for the selected comparison.
- Design contains `Group` only; the artificial `batch` column is visualized but is **not** included in the fitted model.
- Tested contrast is `Group: Cisplatin_IC50_CBD_IC50` versus `DMSO`, with three replicates per group.
- The notebook uses PyDESeq2 `0.5.0`, `DefaultInference(n_cpus=8)`, `refit_cooks=True`, and `DeseqStats` defaults. The install output also pins Python 3.10-era dependencies for that executed run, but the capsule does not provide a lockfile.
- The notebook filter is `padj < 0.05`, `abs(log2FoldChange) >= 0.5`, `baseMean >= 10`.
- The benchmark question `bix-43-q3` instead says adjusted p-value `< 0.05`, absolute log2 fold change `> 0.5`, baseMean `> 10`, and gives ideal answer `677`.

### Material inconsistency affecting LS07-1

The executed notebook prints `len(comp_8) == 679`, while BixBench v1.5 gives `677` as the ideal answer. The likely source is the strictness mismatch (`>=` in notebook versus `>` in the question), but the benchmark does not publish a per-gene gold table proving which two rows account for the difference. Therefore this audit does not convert that likelihood into hidden gold.

BixBench's native verifier for q3 is `str_verifier`: it checks the final scalar answer, not a complete differential-expression artifact. It does not provide a task-local grader for unique gene IDs, all DE statistics, independent-filtering nulls, direction, summary consistency, or a rerunnable script.

### Gene mapping and enrichment

The notebook:

- Queries the live Ensembl REST API one gene at a time for display names. The executed output contains 23 HTTP 400 failures. The request does not pin an Ensembl release.
- Runs GSEApy `1.1.4` `enrichr` against the remote Enrichr library named `Reactome_2022`, organism `Human`, default background (`None`) and cutoff `0.05`.
- Does not supply a frozen GMT, full gene universe, Enrichr database snapshot, API response, or mapping-release manifest.
- Gives the top Reactome term as `TP53 Regulates Transcription Of Cell Cycle Genes R-HSA-6791312`, overlap `8/49`, p-value approximately `0.000140`, adjusted p-value approximately `0.133280`, odds ratio approximately `6.023533`, with overlap genes `BTG2;CDKN1A;PCNA;RGCC;CCNE2;CCNE1;PLK2;BAX`.

The corresponding BixBench ideals are:

- q2 odds ratio: `6.02` (`str_verifier`)
- q4 overlap: `8/49` (`str_verifier`)
- q5 primary mechanism: `TP53-mediated cell cycle regulation` (`llm_verifier`)

The notebook's displayed Reactome table reports 955 rows but the notebook serialization contains a truncated rich display, not a machine-readable complete enrichment table or the underlying Reactome_2022 gene-set file.

## Can the required resources be frozen from the benchmark alone?

| requirement | present? | evidence / consequence |
|---|---:|---|
| Counts and sample layout | Yes | Local files are already frozen and hashed. |
| Selected comparison and replicate membership | Yes | Explicit contrast plus sample metadata. |
| Model design | Yes | `Group` only; batch excluded. |
| Analysis implementation version | Partly | PyDESeq2 0.5.0 is visible, but no complete environment lock is supplied. |
| Exact pass-count gold | Conflicted | Notebook prints 679; q3 ideal is 677; threshold operators differ. |
| Per-gene DE gold table | No | Neither JSONL nor capsule exports it. |
| Stable Ensembl mapping release | No | Notebook performs unversioned live API calls with failures. The local TSV's provenance/release is not stated by the benchmark. |
| Reactome/Enrichr gene-set snapshot | No | Only the symbolic library name `Reactome_2022` is specified. |
| Gene universe/background | No | `background=None`; the server-side effective universe is not frozen. |
| Full pathway enrichment gold table | No | Notebook display is truncated; no exported table. |
| Native full-artifact oracle | No | Native q2-q4 verification is scalar string matching; q5 is LLM-judged. |

## Readiness decision

### `ls07-combination-treatment-deg`: blocked for formal 80-point scoring

The benchmark is sufficient to preserve inputs, contrast, model design, PyDESeq2 version and the expected scalar count candidates. It is **not** sufficient to construct an independent full-artifact oracle without either rerunning and independently reviewing the pinned analysis or introducing assumptions. Because the upstream notebook and q3 gold disagree, `scientific_checks.py` must remain absent/unaccepted until an adjudication rule is approved and a per-gene reference table is produced from that rule.

Minimum non-invented remediation:

1. Decide whether the task follows the q3 text (`>`; ideal 677) or the notebook implementation (`>=`; observed 679). Record this as a benchmark adjudication, not a hidden inference.
2. Reproduce the chosen rule in a locked PyDESeq2 0.5.0 environment from the frozen counts and six specified samples.
3. Export and hash the complete per-gene reference table and environment lock.
4. Have a second reviewer compare the rerun to the executed notebook and q3 record before setting `ACCEPTED=True`.

### `ls07-combination-treatment-mechanism`: resource-provisioned, blocked for formal 80-point scoring

The top pathway identity, overlap, odds ratio and overlap genes are recoverable as scalar benchmark evidence. A complete official Reactome resource and deterministic local background have now been added outside the original benchmark capsule, with their provenance boundary made explicit. The benchmark still does not supply an Ensembl release, an adjudicated DE result, or a full enrichment table, so it cannot by itself satisfy the scientific reference hard gate.

Remaining non-invented remediation:

1. Adjudicate the LS07-1 DE threshold conflict and freeze the resulting per-gene table.
2. Decide whether the capsule's supplied display-name mapping is acceptable despite the missing upstream release label; do not silently call a live mapping API.
3. Reproduce and export the complete enrichment table under GSEApy 1.1.4 against the packaged GMT/background, then independently review the q2/q4/q5 benchmark anchors.

Until then, the existing fail-closed `scientific_checks.py` behavior is correct: its structural checks may support calibration, but `ACCEPTED=False` prevents a formal scientific score. No fabricated full-result gold or passing acceptance record was added.

## 2026-08-16 resource remediation

The official Enrichr endpoint for the library named `Reactome_2022` was retrieved and frozen as `docs/inputs/ls07-combination-treatment-mechanism/Reactome_2022.gmt`.

- Download URL: `https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=Reactome_2022`
- Bytes: `778913`
- SHA-256: `cfe1adc75aa3137ba74c1b35a3098e88ea1708b204e5edfd788092b7ef5c08f8`
- Pathways: `1818`
- Explicit local background: sorted unique union of all GMT gene symbols, `10489` genes
- Background SHA-256: `1ef29c29901cdc2e1efdfd378141ea6811f49e2d70b35e63be2a4b0e9c41c0cc`
- License boundary: Reactome annotation files are CC0; Enrichr attribution/citations and the BixBench expression-input boundary are recorded in `Reactome_2022.manifest.json`.

This resolves the missing gene-set snapshot and unspecified local-universe **input** defects. It does not retroactively reproduce Enrichr's historical server-side default background, resolve the 677/679 DE conflict, establish an Ensembl release for the capsule mapping, or create a complete enrichment gold table. Therefore `ACCEPTED` remains `False` until a locked DE/enrichment reference run and the full acceptance suite are independently reviewed.
