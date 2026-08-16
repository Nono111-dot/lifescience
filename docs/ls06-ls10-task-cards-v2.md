# LS06–LS10 task cards v2

Controlling source: Feishu evaluation workflow revision 138, especially §3.1. Scope: ten tasks, two each for LS06–LS10. Prompts below are the only text pasted into a run. Oracle-side expected values, hidden mappings and reference submissions are not agent-visible.

## Shared scoring and experiment contract

- `Domain`: `life_science` for every card.
- Machine-readable missing values: JSON `null` or empty CSV cells; never the strings `NaN`, `Inf` or invented zeroes.
- Paths are workspace-relative. An analysis script must read only `inputs/` and recreate the declared machine-readable artifacts under `output/` in a clean copy.
- Deterministic score is always 80: coverage/schema 10, core science 40, direction/decision 15, summary consistency 5, static/rerunnable script 10. The independent checker is the named `docs/oracles/<task-id>/scientific_checks.py`; submission code is not imported by the static checker.
- Blind `JudgeScore` is 20: Evidence, Method, Restraint and Readability are each 0/3/5. The judge sees report artifacts only and must not see harness, condition, capability trace or deterministic score.
- C0/T0 are baseline conditions. T1 exposes the complete experiment-approved 222-item life-science catalog for autonomous discovery/installation; T2 adds approved MCP/SCP connections. The task card never recommends a package. The operator records actual discovery/install/call evidence and performs the mandatory post-run reset.
- Source/license boundary: BixBench and CompBioBench files retain their upstream terms; this repository does not assert a new license over them. The LS09 synthetic fixtures are locally authored and intended for CC0-1.0 only after scientific review.
- Input byte identity is frozen by `docs/inputs/SHA256SUMS.tsv` and the per-run `INPUT_MANIFEST.sha256.tsv`.

## Readiness summary

| ID | Sub-domain | Level / time | Anchor / related | Source idea | Formal status |
|---|---|---:|---|---|---|
| `ls06-eno1-effect-size` | `proteomics_and_metabolomics` | L2 / 35 min | X / D,A,V,O,G | BixBench `bix-37-q1/q4` | ready |
| `ls06-eno1-significance-audit` | `proteomics_and_metabolomics` | L2 / 30 min | A / D,X,V,I,O | BixBench `bix-37-q3` | ready |
| `ls07-combination-treatment-deg` | `transcriptomics` | L3 / 75 min | X / D,P,T,A,G | BixBench `bix-43-q3` | blocked: pinned DESeq2 reference acceptance |
| `ls07-combination-treatment-mechanism` | `systems_and_synthetic_biology` | L3 / 90 min | I / T,A,X,V,G | BixBench `bix-43-q5` | blocked: enrichment reference/oracle acceptance; Reactome input now frozen |
| `ls08-multiome-column-match` | `single_cell_and_spatial` | L3 / 75 min | X / D,P,A,V,G | CompBioBench `multiome-match-atac-rna-q1` | blocked: hidden mapping/normalization acceptance |
| `ls08-enhancer-promoter-integration` | `epigenomics_and_regulation` | L2 / 45 min | I / D,A,X,V,O | CompBioBench `ep-interactions-q1` | blocked: aggregation/tie-rule acceptance |
| `ls09-opentrons-sop` | `systems_and_synthetic_biology` | L2 / 45 min | P / T,A,V,O,G | source-supported local extension; Opentrons official protocol/API rules | blocked: cross-harness simulator provisioning/acceptance |
| `ls09-plate-dilution-recovery` | `systems_and_synthetic_biology` | L2 / 40 min | R / D,P,A,X,V | source-supported local extension; dilution mass balance and Opentrons volume rules | ready |
| `ls10-neun-power-analysis` | `biomedical_and_clinical_bioinformatics` | L2 / 40 min | X / D,A,V,I,G | BixBench `bix-19-q1/q2` | ready |
| `ls10-treatment-response-model` | `biomedical_and_clinical_bioinformatics` | L2 / 45 min | X / D,A,V,I,G | BixBench `bix-51-q3/q4` | ready |

## `ls06-eno1-effect-size`

- Inputs: `Proteomic_data .xlsx` (target; sheet `Tumor vs Normal`; columns include `gene`, `Normal`, `Tumor`, `Ratio`, `FC`, `log2FC`, `p.value`, `adj.Pval`) and `MeRIP_RNA_result.xlsx` (unrelated decoy; transcript/m6A table). Total 1,801,598 bytes. Provenance: BixBench capsule data; answer-bearing notebooks excluded.
- Prompt: **Using the supplied proteomics results, calculate ENO1 tumor-versus-normal fold change and log2 fold change. Write `output/eno1_effect.json` with `gene,tumor_value,normal_value,fold_change,log2_fold_change,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. State the fold-change direction and do not substitute the unrelated workbook.**
- Deliverables: one JSON object with finite numeric values and source identifiers; UTF-8 Markdown report; rerunnable Python script. No additional artifact is required.
- Hard gates: exact ENO1/source row; all four core values within checker tolerance; fold-change/log2 direction internally consistent; source file and sheet traceable.
- Deterministic 80: coverage/schema 10; Normal, Tumor, fold change and log2 fold change 10 each (raw values relative tolerance `5e-6`, fold change `2e-3`, log2 absolute tolerance `0.011`); direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[tabular-analysis]`, `[workbook-reader]`, `[reproducible-code]`; expected to reduce wrong-sheet, arithmetic and non-rerunnable-output errors without disclosing a route.

## `ls06-eno1-significance-audit`

- Inputs: the same two workbooks and roles as the preceding card; the MeRIP workbook remains a decoy. Target sheet exposes both raw and adjusted p-value columns.
- Prompt: **Retrieve ENO1's adjusted p-value from the supplied proteomics results and give a threshold-calibrated interpretation at FDR 0.05. Write `output/eno1_significance.json` with `gene,adjusted_p_value,fdr_threshold,significant,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. Do not relabel a raw p-value as adjusted.**
- Deliverables: one JSON object; report; rerunnable script. `significant` is a JSON boolean.
- Hard gates: exact ENO1/source; adjusted rather than raw p-value; finite p in `[0,1]`; boolean agrees with FDR 0.05.
- Deterministic 80: coverage/schema 10; adjusted p-value 40 (absolute tolerance `0.0005`); FDR decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[tabular-analysis]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce wrong-column and raw-versus-adjusted-p errors.

## `ls07-combination-treatment-deg`

- Inputs: `counts_raw_unfiltered.csv` (raw integer gene-by-sample counts), `sample_layout.csv` (sample/condition design), `ensg_to_gene_name.tsv` (Ensembl-to-symbol support mapping); total 8,443,658 bytes. Provenance: BixBench capsule data; no decoy file.
- Prompt: **Run the frozen combination-treatment contrast against its specified comparator using the sample layout. Write `output/differential_expression.csv` with `gene_id,gene_name,baseMean,log2FoldChange,pvalue,padj,pass`, `output/summary.json` with the number passing `padj<0.05`, `abs(log2FoldChange)>0.5`, and `baseMean>10`, `output/analysis.py`, and `output/report.md`. Preserve independent-filtering missing values as null.**
- Deliverables: unique gene rows; JSON count and explicit contrast/design metadata; report; rerunnable script. CSV missing numeric values are empty.
- Hard gates: design and contrast recorded exactly; gene IDs unique; threshold rule uses strict inequalities exactly; summary count equals passing rows.
- Deterministic 80: coverage/schema 10; frozen reference values and pass count 40 using the pinned DESeq2 environment/tolerances; direction/threshold decision 15; summary consistency 5; static/rerunnable script 10.
- Ablation expectation: `[transcriptome-analysis]`, `[experimental-design]`, `[multiple-testing-audit]`, `[reproducible-code]`; expected to reduce contrast, filtering and provenance errors.
- Readiness blocker: checker remains `ACCEPTED=False` until one pinned R/DESeq2 design reproduces the reference in 3/3 clean runs and wrong/empty controls fail. Do not formally run or replace this with a hand-authored reference table.

## `ls07-combination-treatment-mechanism`

- Inputs: the three LS07 expression files plus `Reactome_2022.gmt`, `Reactome_2022.background.txt`, and `Reactome_2022.manifest.json`. The official Enrichr-named snapshot contains 1,818 pathways and its explicit local background contains 10,489 unique gene symbols. No remote or newer library is a valid substitute.
- Prompt: **Using the frozen differential-expression rule, `Reactome_2022.gmt`, and `Reactome_2022.background.txt`, identify the best-supported primary mechanism of the combination treatment. Do not query a remote enrichment service or substitute a different release/background. Write `output/pathway_enrichment.csv` with `pathway_id,pathway_name,overlap,p_value,padj,direction`, `output/mechanism_call.json`, `output/analysis.py`, and `output/report.md` (maximum 600 words). Distinguish enrichment from demonstrated causation.**
- Deliverables: pathway table with declared tested universe/release; mechanism JSON referencing a table row; report; rerunnable script. Missing statistics are empty/null.
- Hard gates: exact pinned gene-set release and universe used; corrected enrichment statistics valid; mechanism call supported by a reported row; no causal overclaim.
- Deterministic 80: coverage/schema 10; overlap/statistics/ranking and primary mechanism 40 against the pinned reference; evidence direction/restraint 15; summary consistency 5; static/rerunnable script 10.
- Ablation expectation: `[pathway-analysis]`, `[gene-set-reference]`, `[network-interpretation]`, `[reproducible-code]`; expected to reduce stale-release, universe and causal-language errors.
- Readiness blocker: the Reactome library and explicit background are now packaged and hashed, resolving the missing-input defect. The complete DE/enrichment reference table, mapping adjudication, benchmark-anchor reconciliation, and 3/3 positive/negative oracle acceptance are still absent. Do not infer a full gold table merely from the published top-pathway scalar anchors.

## `ls08-multiome-column-match`

- Inputs: gzipped ATAC-bin table (15,259,355 bytes) and RNA-TPM table (1,432,352 bytes), eight populations per modality. Provenance: Genentech CompBioBench data at the frozen 2026-08-14 `main` retrieval; column permutation is hidden from the agent.
- Prompt: **Recover the one-to-one matching between the eight permuted ATAC population columns and RNA populations. Write `output/column_mapping.csv` with `rna_population,atac_column,match_score,runner_up_score`, `output/score_matrix.csv`, `output/analysis.py`, and `output/report.md`. Enforce a bijection and explain the shared biological signal used.**
- Deliverables: eight unique mapping rows; complete finite score matrix; report; rerunnable script. Score definition and preprocessing must be stated.
- Hard gates: all eight labels on each side appear exactly once; mapping is a bijection; all reported scores finite; mapping direction is RNA-to-ATAC.
- Deterministic 80: coverage/schema 10; full score matrix and hidden permutation 40 under the frozen preprocessing/tolerance; bijection/direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[multi-omics-integration]`, `[feature-alignment]`, `[assignment-optimization]`, `[reproducible-code]`; expected to reduce label leakage, many-to-one and normalization errors.
- Readiness blocker: checker remains `ACCEPTED=False` until the expected permutation and acceptable normalization policy pass independent reference/wrong/empty tests in 3/3 clean runs.

## `ls08-enhancer-promoter-integration`

- Inputs: `ep.interactions.q1.hic.csv` (contact evidence; 6,388 bytes) and `ep.interactions.q1.expr.csv` (CRISPR-expression evidence; 3,792 bytes). Provenance: Genentech CompBioBench frozen retrieval; no decoy file.
- Prompt: **Integrate the supplied Hi-C and CRISPR-expression evidence for all candidate enhancer-promoter pairs and identify the least supported causal pair. Write `output/pair_evidence.csv` with `pair_id,contact_evidence,perturbation_effect,combined_support,rank`, `output/least_supported.json`, `output/analysis.py`, and `output/report.md`. Treat physical contact and perturbation evidence as distinct.**
- Deliverables: every candidate pair exactly once, unique ranks, one least-supported call, report and rerunnable script; units/scales and tie policy stated.
- Hard gates: modalities joined by the true pair key; all candidates covered once; least-supported call equals minimum combined support under the frozen rule; contact is not described as perturbational proof.
- Deterministic 80: coverage/schema 10; modality values, combined score and ranking 40; least-supported decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[regulatory-integration]`, `[causal-evidence-audit]`, `[tabular-analysis]`, `[reproducible-code]`; expected to reduce bad joins, scale mixing and causal overclaim.
- Readiness blocker: checker remains `ACCEPTED=False` until aggregation, normalization and tie rules are frozen from benchmark-supported evidence and pass the acceptance suite. No rule may be invented merely to make one pair win.

## `ls09-opentrons-sop`

- Inputs: `sop.md`, `instrument.csv`, `labware.csv`, `reagent_map.csv`, `sample_map.csv`, and `simulator_contract.json`. They pin robot/API, pipette, deck slots, labware, wells, source volumes, 24 samples, Opentrons package 7.1.0, Protocol API 2.16, invocation, capture policy, and failure behavior. Provenance and scientific basis are in `docs/research/ls09-local-extension-provenance.md`; no answer-bearing decoy.
- Prompt: **Translate the supplied SOP into an auditable Opentrons protocol plan. The transfer plan represents exactly eight net liquid-transfer stages per sample; do not list individual mix strokes or low-level aspirate/dispense movements as extra rows. Write `output/protocol.py`, `output/transfer_plan.csv` with `step,source,destination,volume_uL,pipette,tip_policy`, `output/simulation.txt`, and `output/report.md`. Respect labware, deck, pipette, volume and contamination constraints. Run the supplied pinned simulator; if it is unavailable or fails, record the exact error and mark the protocol not execution-ready rather than claiming success.**
- Deliverables: static Opentrons protocol; 192-row net-transfer plan; verbatim simulator record; report. All wells/volumes/pipettes/tip policies must be explicit.
- Hard gates: exact net-transfer contract and liquid balance; valid deck/labware/wells/pipette range and contamination-safe tip policy; static protocol contract; pinned simulation success.
- Deterministic 80: coverage/schema 10; transfer contract, balance, pipette and tip policy 40; protocol/simulation decision 15; report consistency 5; static protocol plus isolated pinned simulation 10.
- Ablation expectation: `[protocol-planning]`, `[liquid-handling]`, `[labware-validation]`, `[simulation]`; expected to reduce unsafe tips, invalid volumes, deck and false-success errors.
- Readiness blocker: the repository now contains a pinned Opentrons 7.1.0 / API 2.16 simulator contract and hash-locked Linux CPython 3.10 dependency set. The checker remains `ACCEPTED=False` until that exact environment is provisioned identically in Codex and all scheduled Duanyan arms, the reference protocol is executed by the real simulator 3/3, and wrong/empty controls fail. A failed/missing simulator remains a valid run observation but cannot produce a formal score.

## `ls09-plate-dilution-recovery`

- Inputs: `dilution_request.csv`, `pipettes.csv`, `plate_map.csv`, `run_log.csv`, `source_inventory.csv`; total 1,112 bytes. They define requested concentrations/volumes, P20/P300 limits, completed/failed wells, transfer history and remaining stocks. Provenance/scientific basis: source-supported synthetic local extension; no patient data and no decoy.
- Prompt: **Diagnose the failed dilution run and produce a physically feasible recovery plan. Write `output/root_cause.json`, `output/recovery_plan.csv` with `step,source,destination,transfer_uL,transfer_pipette,diluent_source,diluent_uL,diluent_pipette,final_concentration,final_volume_uL`, `output/analysis.py`, and `output/report.md`. Enforce pipette ranges, mass balance and supplied solvent/volume limits.**
- Deliverables: structured root cause; one row per required recovery destination; separate pipettes for solute and diluent transfers; report and rerunnable script.
- Hard gates: root cause traceable to the run log; only failed/requested wells are recovered; dilution mass balance and both pipette ranges pass; no source overdraw.
- Deterministic 80: coverage/schema 10; root cause 14, recovery plan 10, concentration/mass balance 10, pipette plus inventory feasibility 6; recover/abort decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[liquid-handling]`, `[mass-balance]`, `[run-log-audit]`, `[reproducible-code]`; expected to reduce double-processing, wrong-pipette and stock-overdraw errors.

## `ls10-neun-power-analysis`

- Inputs: `NeuN_quantification.csv` (218 bytes), two labeled groups with observed measurements. Provenance: BixBench capsule data; no decoy.
- Prompt: **Estimate the standardized mean difference (Cohen's d) between the two supplied groups and the required equal sample size per group for a two-sided independent t-test at alpha 0.05 and power 0.80. Write `output/power_result.json` with `group_labels,n_each,means,sds,pooled_sd,cohens_d,alpha,power,alternative,required_n_per_group`, `output/analysis.py`, and `output/report.md`. Round required n upward.**
- Deliverables: one JSON object with group-keyed or label-aligned arrays; report; rerunnable script. Sample SD convention and signed-d order must be stated.
- Hard gates: both groups mapped correctly; finite means/SD/pooled SD/effect size; two-sided alpha/power specification exact; sample size rounded upward.
- Deterministic 80: coverage/schema 10; means 8, SDs 8, pooled SD 6, absolute Cohen d 8 (`5e-3` tolerance), required n/group 10; specification/direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[power-analysis]`, `[effect-size]`, `[reproducible-code]`; expected to reduce SD convention, sidedness and rounding errors.

## `ls10-treatment-response-model`

- Inputs: `data.xlsx` (22,788 bytes), sheet `Sheet1`; columns include `Efficacy`, `Age`, `Gender`, `BMI` and other non-model covariates. The target model uses only the named outcome/predictors; other columns are distractors. Provenance: BixBench capsule data.
- Prompt: **Fit a logistic regression for the binary treatment-response outcome using BMI, age and gender. Use complete cases, document outcome coding and gender reference level, and report the age log-odds coefficient and two-sided p-value. Write `output/model_coefficients.csv` with `term,estimate,std_error,z,p_value,odds_ratio`, `output/model_metadata.json`, `output/analysis.py`, and `output/report.md`.**
- Deliverables: unique coefficient rows; metadata with formula, outcome coding, reference level, complete-case count and implementation/version; report; rerunnable script.
- Hard gates: specified model only; binary outcome coding and gender reference documented; age term unique and finite; coefficient, odds ratio and significance interpretation mutually consistent.
- Deterministic 80: coverage/schema 10; age estimate, SE, two-sided p-value and odds ratio 10 each (`rel_tol=3e-3`, `abs_tol=5e-5`); age direction/decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[regression-diagnostics]`, `[categorical-coding]`, `[reproducible-code]`; expected to reduce outcome/reference-level and coefficient-interpretation errors.

## Release gate

A card enters the main result only if its reference submission passes 3/3 clean reruns, empty output and at least one format-correct scientific error fail 3/3, one domain reviewer and one grader reviewer accept it, and a timed calibration run can be frozen and rescored. On 2026-08-14, exactly five cards above meet this gate.
