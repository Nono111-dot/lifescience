# LS06–LS10 task cards v2

Controlling source: evaluation workflow revision 138, especially §3.1. Scope: ten tasks, two each for LS06–LS10. Prompts below are the only text pasted into a run. Oracle-side expected values, hidden mappings and reference submissions are not agent-visible.

## Shared scoring and experiment contract

- `Domain`: `life_science` for every card.
- Machine-readable missing values: JSON `null` or empty CSV cells; never the strings `NaN`, `Inf` or invented zeroes.
- Paths are workspace-relative. An analysis script must read only `inputs/` and recreate the declared machine-readable artifacts under `output/` in a clean copy.
- Deterministic score is always 80: coverage/schema 10, core science 40, direction/decision 15, summary consistency 5, static/rerunnable script 10. The independent checker is the named `docs/oracles/<task-id>/scientific_checks.py`; submission code is not imported by the static checker.
- Blind `JudgeScore` is 20: Evidence, Method, Restraint and Readability are each 0/3/5. The judge sees report artifacts only and must not see harness, condition, capability trace or deterministic score.
- C0 is Codex with no added domain skill. T1 uses the same Codex client/model/build with task-appropriate Agent Skills predeclared from the approved workbook and installed from fixed GitHub commits before a fresh task starts; MCP/SCP rows are excluded. The operator records install/load/invocation evidence and performs the mandatory post-run reset.
- Source/license boundary: BixBench and CompBioBench files retain their upstream terms; this repository does not assert a new license over them. The LS09 synthetic fixtures are locally authored and intended for CC0-1.0 only after scientific review.
- Input byte identity is frozen by `docs/inputs/SHA256SUMS.tsv` and the per-run `INPUT_MANIFEST.sha256.tsv`.

## Readiness summary

| ID | Sub-domain | Level / time | Anchor / related | Source idea | Formal status |
|---|---|---:|---|---|---|
| `ls06-eno1-effect-size` | `proteomics_and_metabolomics` | L2 / 35 min | X / D,A,V,O,G | BixBench `bix-37-q1/q4` | ready |
| `ls06-eno1-significance-audit` | `proteomics_and_metabolomics` | L2 / 30 min | A / D,X,V,I,O | BixBench `bix-37-q3` | ready |
| `ls07-combination-treatment-deg` | `transcriptomics` | L3 / 75 min | X / D,P,T,A,G | BixBench `bix-43-q3` | ready: PyDESeq2 0.5.0 full-row reference frozen |
| `ls07-combination-treatment-mechanism` | `systems_and_synthetic_biology` | L3 / 90 min | I / T,A,X,V,G | BixBench `bix-43-q5` | ready: frozen Reactome universe and full enrichment reference |
| `ls08-multiome-column-match` | `single_cell_and_spatial` | L3 / 75 min | X / D,P,A,V,G | CompBioBench `multiome-match-atac-rna-q1` | ready: mapping/normalization rule and score matrix frozen |
| `ls08-enhancer-promoter-integration` | `epigenomics_and_regulation` | L2 / 45 min | I / D,A,X,V,O | CompBioBench `ep-interactions-q1` | ready: aggregation, residual-z and tie rule frozen |
| `ls09-opentrons-sop` | `systems_and_synthetic_biology` | L2 / 45 min | P / T,A,V,O,G | source-supported local extension; Opentrons official protocol/API rules | ready: Opentrons 7.1.0 reference simulation passed 3/3 |
| `ls09-plate-dilution-recovery` | `systems_and_synthetic_biology` | L2 / 40 min | R / D,P,A,X,V | source-supported local extension; dilution mass balance and Opentrons volume rules | ready |
| `ls10-neun-power-analysis` | `biomedical_and_clinical_bioinformatics` | L2 / 40 min | X / D,A,V,I,G | BixBench `bix-19-q1/q2` | ready |
| `ls10-treatment-response-model` | `biomedical_and_clinical_bioinformatics` | L2 / 45 min | X / D,A,V,I,G | BixBench `bix-51-q3/q4` | ready |

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

## `ls06-eno1-significance-audit`

### Inputs (authoritative packaged inventory)
- `inputs/MeRIP_RNA_result.xlsx` — 1,155,180 bytes
- `inputs/Proteomic_data .xlsx` — 646,418 bytes
- `inputs/README.md` — 970 bytes

**Total:** 1,802,568 bytes (1.72 MiB).

- Prompt: **Retrieve ENO1's adjusted p-value from the supplied proteomics results and give a threshold-calibrated interpretation at FDR 0.05. Write `output/eno1_significance.json` with `gene,adjusted_p_value,fdr_threshold,significant,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. Do not relabel a raw p-value as adjusted.**
- Deliverables: one JSON object; report; rerunnable script. `significant` is a JSON boolean.
- Hard gates: exact ENO1/source; adjusted rather than raw p-value; finite p in `[0,1]`; boolean agrees with FDR 0.05.
- Deterministic 80: coverage/schema 10; adjusted p-value 40 (absolute tolerance `0.0005`); FDR decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[tabular-analysis]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce wrong-column and raw-versus-adjusted-p errors.

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

## `ls08-enhancer-promoter-integration`

### Inputs (authoritative packaged inventory)
- `inputs/INTEGRATION_RULE.md` — 1,011 bytes
- `inputs/README.md` — 1,131 bytes
- `inputs/ep.interactions.q1.expr.csv` — 3,792 bytes
- `inputs/ep.interactions.q1.hic.csv` — 6,388 bytes

**Total:** 12,322 bytes (0.01 MiB).

- Prompt: **Integrate the supplied Hi-C and CRISPR-expression evidence for all candidate enhancer-promoter pairs and identify the least supported causal pair. Write `output/pair_evidence.csv` with `pair_id,contact_evidence,perturbation_effect,combined_support,rank`, `output/least_supported.json`, `output/analysis.py`, and `output/report.md`. Treat physical contact and perturbation evidence as distinct.**
- Deliverables: every candidate pair exactly once, unique ranks, one least-supported call, report and rerunnable script; units/scales and tie policy stated.
- Hard gates: modalities joined by the true pair key; all candidates covered once; least-supported call equals minimum combined support under the frozen rule; contact is not described as perturbational proof.
- Deterministic 80: coverage/schema 10; modality values, combined score and ranking 40; least-supported decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[regulatory-integration]`, `[causal-evidence-audit]`, `[tabular-analysis]`, `[reproducible-code]`; expected to reduce bad joins, scale mixing and causal overclaim.
- Readiness closure: background distance regression, robust residual z-score, guide aggregation, physical-evidence threshold and ranking/tie rule are frozen and independently recomputed by the checker.

## `ls09-opentrons-sop`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 1,699 bytes
- `inputs/instrument.csv` — 123 bytes
- `inputs/labware.csv` — 329 bytes
- `inputs/reagent_map.csv` — 200 bytes
- `inputs/sample_map.csv` — 274 bytes
- `inputs/simulator_contract.json` — 1,108 bytes
- `inputs/sop.md` — 1,481 bytes

**Total:** 5,214 bytes (0.00 MiB).

### Prompt

> Read every file under `inputs/`. Translate the frozen 24-sample magnetic-bead cleanup SOP into an auditable OT-2 Opentrons protocol. Use no external data and do not alter inputs. Write `output/protocol.py`, `output/transfer_plan.csv` with exactly the columns `step,source,destination,volume_uL,pipette,tip_policy`, `output/simulation.txt`, and `output/report.md`. `transfer_plan.csv` is a net liquid-transfer stage table, not a command log: write exactly one row per SOP net-transfer stage per sample (`lysis`, `beads`, `supernatant`, `wash1_add`, `wash1_remove`, `wash2_add`, `wash2_remove`, `elution`), for 8 × 24 = 192 rows. Do not add one row per mix stroke, aspirate command, dispense command, delay, magnet action, or tip action; represent those operations in `protocol.py` and summarize them in `report.md`. Identify each row as `<stage>:<well>` and use the frozen role/well identifiers. Respect the declared deck, Magnetic Module compatibility, API level, pipette range, well capacity, reagent dead volumes, liquid balance, and tip policy. Run the evaluator-pinned simulator using the supplied invocation and record its unedited outcome in `simulation.txt`; if that simulator or invocation is unavailable, record the failure and abort rather than claiming success.
- Deliverables: static Opentrons protocol; 192-row net-transfer plan; verbatim simulator record; report. All wells/volumes/pipettes/tip policies must be explicit.
- Hard gates: exact net-transfer contract and liquid balance; valid deck/labware/wells/pipette range and contamination-safe tip policy; static protocol contract; pinned simulation success.
- Deterministic 80: coverage/schema 10; transfer contract, balance, pipette and tip policy 40; protocol/simulation decision 15; report consistency 5; static protocol plus isolated pinned simulation 10.
- Ablation expectation: `[protocol-planning]`, `[liquid-handling]`, `[labware-validation]`, `[simulation]`; expected to reduce unsafe tips, invalid volumes, deck and false-success errors.
- Readiness closure: the reference protocol completed three real Opentrons 7.1.0 simulations and wrong/empty/legacy-tip controls fail; both C0 and T1 receive the same pre-provisioned simulator. The macOS-arm64 versus production Linux-x86_64 platform difference is retained as a disclosed campaign deviation.

## `ls09-plate-dilution-recovery`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 1,204 bytes
- `inputs/dilution_request.csv` — 94 bytes
- `inputs/pipettes.csv` — 62 bytes
- `inputs/plate_map.csv` — 187 bytes
- `inputs/run_log.csv` — 587 bytes
- `inputs/source_inventory.csv` — 182 bytes

**Total:** 2,316 bytes (0.00 MiB).

### Prompt

> Read every file under `inputs/`. Diagnose the stopped dilution run and generate only the recovery work that remains physically necessary. Use no external data and do not alter inputs. Write `output/root_cause.json` with `failed_well,failure_mode,liquid_moved,completed_wells,recovery_wells`; `failure_mode` may be a concise controlled phrase that states the failed operation and whether it occurred before aspiration. Write `output/recovery_plan.csv` with exactly `step,source,destination,transfer_uL,transfer_pipette,diluent_source,diluent_uL,diluent_pipette,final_concentration,final_volume_uL`; the two pipette fields identify the physical instrument for each distinct liquid movement. Also write rerunnable `output/analysis.py` and `output/report.md`. Enforce the plate map, event ordering, `C_source*V_transfer=C_final*V_final`, source inventory, solvent identity, and frozen pipette ranges. Do not redo completed wells. Abort explicitly rather than inventing a missing transfer.
- Deliverables: structured root cause; one row per required recovery destination; separate pipettes for solute and diluent transfers; report and rerunnable script.
- Hard gates: root cause traceable to the run log; only failed/requested wells are recovered; dilution mass balance and both pipette ranges pass; no source overdraw.
- Deterministic 80: coverage/schema 10; root cause 14, recovery plan 10, concentration/mass balance 10, pipette plus inventory feasibility 6; recover/abort decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[liquid-handling]`, `[mass-balance]`, `[run-log-audit]`, `[reproducible-code]`; expected to reduce double-processing, wrong-pipette and stock-overdraw errors.

## `ls10-neun-power-analysis`

### Inputs (authoritative packaged inventory)
- `inputs/NeuN_quantification.csv` — 218 bytes
- `inputs/README.md` — 770 bytes

**Total:** 988 bytes (0.00 MiB).

- Prompt: **Estimate the standardized mean difference (Cohen's d) between the two supplied groups and the required equal sample size per group for a two-sided independent t-test at alpha 0.05 and power 0.80. Write `output/power_result.json` with `group_labels,n_each,means,sds,pooled_sd,cohens_d,alpha,power,alternative,required_n_per_group`, `output/analysis.py`, and `output/report.md`. Round required n upward.**
- Deliverables: one JSON object with group-keyed or label-aligned arrays; report; rerunnable script. Sample SD convention and signed-d order must be stated.
- Hard gates: both groups mapped correctly; finite means/SD/pooled SD/effect size; two-sided alpha/power specification exact; sample size rounded upward.
- Deterministic 80: coverage/schema 10; means 8, SDs 8, pooled SD 6, absolute Cohen d 8 (`5e-3` tolerance), required n/group 10; specification/direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[power-analysis]`, `[effect-size]`, `[reproducible-code]`; expected to reduce SD convention, sidedness and rounding errors.

## `ls10-treatment-response-model`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 806 bytes
- `inputs/data.xlsx` — 22,788 bytes

**Total:** 23,594 bytes (0.02 MiB).

- Prompt: **Fit a logistic regression for the binary treatment-response outcome using BMI, age and gender. Use complete cases, document outcome coding and gender reference level, and report the age log-odds coefficient and two-sided p-value. Write `output/model_coefficients.csv` with `term,estimate,std_error,z,p_value,odds_ratio`, `output/model_metadata.json`, `output/analysis.py`, and `output/report.md`.**
- Deliverables: unique coefficient rows; metadata with formula, outcome coding, reference level, complete-case count and implementation/version; report; rerunnable script.
- Hard gates: specified model only; binary outcome coding and gender reference documented; age term unique and finite; coefficient, odds ratio and significance interpretation mutually consistent.
- Deterministic 80: coverage/schema 10; age estimate, SE, two-sided p-value and odds ratio 10 each (`rel_tol=3e-3`, `abs_tol=5e-5`); age direction/decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[regression-diagnostics]`, `[categorical-coding]`, `[reproducible-code]`; expected to reduce outcome/reference-level and coefficient-interpretation errors.

## Release gate

A card enters the main result only if its reference submission passes 3/3 clean reruns, empty output and at least one format-correct scientific error fail 3/3, one domain reviewer and one grader reviewer accept it, and a timed calibration run can be frozen and rescored. On 2026-08-17, all ten cards have accepted static checkers; campaign-level reviewer and platform deviations remain governed by `formal-eval-release-status-2026-08-17.md`.
