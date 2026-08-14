# Life-science evaluation task cards v1

Current formal evaluation scope is LS06–LS10 only (10 tasks). LS01–LS05 cards below are retained as candidate-development material and must not be scheduled in the current run matrix. Use `ls06-ls10-runbook-v2.md` as the controlling execution document.

These cards follow the evaluation workflow revision 135. The operator pastes only the **Prompt** block. Rubric, gates and source notes remain outside the run workspace. All formal artifacts must be written under `output/`; inputs are read-only. JSON/CSV numeric values must be finite, identifiers unique, and missing values represented as empty/`null`, never invented. L2/L3 tasks must include a rerunnable `output/analysis.py` and `output/report.md` (≤300 words unless noted).

The authoritative deterministic rubric is `deterministic-rubrics-v2.tsv`: **coverage 10 + task-specific core scientific calculation 40 + direction/decision 15 + summary consistency 5 + rerunnable script 10 = 80**. This replaces the older per-card draft allocations below; the blind 20-point rubric is unchanged. Oracles must emit all five component scores separately.

## LS01-1 `ls01-grna-offtarget-rank`

- Domain/subdomain: molecular biology / CRISPR design; P0; L2, 40 min; anchor D/P/A/O; source: custom fixture.
- Inputs: `inputs/candidates.csv`, `inputs/off_targets.csv`.
- Prompt: **Read the two supplied CSV files and rank all candidate guides by on-target activity and annotated off-target risk. Do not fetch external data or alter inputs. Write `output/ranked_guides.csv` with `rank,guide_id,on_target_score,risk_class,decision,rationale`, `output/analysis.py`, and `output/report.md`. Rankings must be unique; every input guide must appear once; explicitly treat coding/exonic near matches and mismatch count as safety evidence and state any trade-off rather than hiding it.**
- Hard gates: all guides exactly once; unique integer ranks 1..N; numeric values traceable to inputs; decisions/rationales nonempty; script reruns cleanly.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS01-2 `ls01-primer-transcript-audit`

- Domain/subdomain: molecular biology / primer specificity; P0; L2, 40 min; D/P/A/O; custom.
- Inputs: `inputs/transcripts.fa`, `inputs/primer_candidates.csv`.
- Prompt: **Audit every primer pair against the supplied transcript isoforms. Write `output/primer_audit.csv` with `pair_id,transcripts_matched,amplicon_length,cds_compatible,status,reason`, `output/analysis.py`, and `output/report.md`. Use only supplied sequences; report malformed or internally inconsistent sequence metadata rather than silently repairing it.**
- Gates: every pair once; sequence/coordinate validation reported; no fabricated bases; finite lengths; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS01-3 `ls01-vector-orf-audit`

- Domain/subdomain: molecular biology / construct QC; P0; L2, 35 min; D/P/A/O; custom.
- Inputs: `inputs/constructs.csv`.
- Prompt: **Audit each construct for start/stop codons, reading frame, tag/linker compatibility and cloning flags represented in the input. Write `output/construct_audit.csv` with `construct_id,frame_ok,start_ok,stop_ok,tag_ok,overall_status,issues`, `output/analysis.py`, and `output/report.md`. Do not infer sequence features that are absent from the input.**
- Gates: every construct once; boolean fields valid; issues agree with status; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS02-1 `ls02-deleterious-mutation`

- Domain/subdomain: genomics / variant calling; P0; L3, 90 min; D/P/T/A/R/O; CompBioBench `deleterious-mutation-q2`.
- Inputs: `inputs/deleterious.mutation.q2.R1.fq.gz` plus evaluator-pinned chr9 reference bundle (to be added).
- Prompt: **Analyze the supplied chr9 exome reads to identify the high-confidence mosaic nonsense SNV in a highly loss-of-function-intolerant protein-coding gene. Write `output/variant.tsv` with `chrom,pos,ref,alt,gene,consequence,alt_reads,total_reads,allele_fraction`, `output/evidence.json`, `output/analysis.py`, and `output/report.md`. Report allele fraction as 0–1 and document reference/annotation versions.**
- Gates: one valid variant; coordinates/reference consistent; read counts support AF; consequence/gene supported; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS02-2 `ls02-find-deletion`

- Domain/subdomain: genomics / structural variation; P0; L3, 75 min; D/P/T/A/R/O; CompBioBench `find-deletion-q1`.
- Inputs: paired FASTQ files plus pinned hg38 bundle (to be added).
- Prompt: **Locate the large deletion in the supplied shallow paired-end hg38 data. Write `output/deletion.tsv` with `chrom,start_100kb,end_100kb,size_bp,supporting_signals`, `output/qc.json`, `output/analysis.py`, and `output/report.md`. Round breakpoints to the nearest 100 kb and distinguish evidence from precision limits.**
- Gates: one interval, start<end, hg38 coordinates, support nonempty, rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS02-3 `ls02-infer-genome-build`

- Domain/subdomain: genomics / coordinate normalization; P0; L2, 40 min; D/P/T/A/O; CompBioBench `vcf-infer-build-q1`.
- Inputs: `inputs/vcf.infer.build.q1.vcf.gz` plus pinned diagnostic reference bundle (to be added).
- Prompt: **Determine whether the supplied chr20 VCF uses hg18, hg19, hg38 or T2T coordinates. Write `output/build_call.json` with `build,confidence,n_variants_checked,n_ref_matches,n_ref_mismatches,evidence`, `output/analysis.py`, and `output/report.md`. Base the call on reproducible allele/coordinate checks and do not treat chromosome naming alone as proof.**
- Gates: allowed build label; counts nonnegative; evidence present; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS03-1 `ls03-cryptic-exon`

- Domain/subdomain: transcriptomics / splicing; P0; L3, 90 min; D/P/T/A/R/O; CompBioBench `cryptic-exon-q1`.
- Inputs: `inputs/cryptic.exon.q1.fq.gz` plus pinned human genome/transcriptome index (to be added).
- Prompt: **Identify the protein-coding HGNC gene containing the highly expressed cryptic exon supported by two novel splice junctions. Write `output/cryptic_exon.tsv` with `gene,chrom,start,end,left_junction_reads,right_junction_reads,expression_evidence`, `output/junctions.tsv`, `output/analysis.py`, and `output/report.md`. Novelty must be assessed against the supplied annotation version.**
- Gates: one gene/interval; two flanking novel junctions; read support finite; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS03-2 `ls03-atac-sample-swap`

- Domain/subdomain: epigenomics / sample QC; P0; L3, 75 min; D/P/A/V/O; CompBioBench `sample-swap-atac-q1`.
- Inputs: compressed ATAC count table and chromosome sizes.
- Prompt: **Determine whether two organ labels are swapped in the axolotl bulk ATAC-seq data. Write `output/swap_call.json` with `swap_detected,organ_a,organ_b,confidence,evidence`, `output/sample_similarity.csv`, `output/analysis.py`, and `output/report.md`. If evidence does not support a unique swap, return `swap_detected=false` and explain uncertainty.**
- Gates: valid organ labels or null; symmetric swap; finite similarity matrix; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS03-3 `ls03-genome-coordinates`

- Domain/subdomain: regulatory genomics / live-cell dynamics; P0; L2, 45 min; D/P/A/V/O; CompBioBench `genome-coords-q1` adapted.
- Inputs: `inputs/single_cell_dynamics_question.csv`.
- Prompt: **Analyze enhancer-promoter 3D distance and transcription dynamics across cells and time. Write `output/cell_metrics.csv`, `output/lag_analysis.csv` with `lag,association,n_observations`, `output/analysis.py`, and `output/report.md`. Use 260 nm as the supplied contact threshold. Separate temporal association from causation and state what the observational data cannot establish.**
- Gates: all cells represented; finite metrics; lag direction defined; no categorical causal claim unsupported by intervention; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS04-1 `ls04-differential-composition`

- Domain/subdomain: single-cell / composition; P0; L3, 90 min; D/P/T/A/R/O; CompBioBench `differential-composition-q1`.
- Inputs: two Matrix Market matrices and gene list; pinned marker reference to be added.
- Prompt: **Compare the two retinal single-cell expression matrices and identify the cell population that is severely depleted in sample 2. Write `output/composition.csv` with `sample,cell_type,n_cells,fraction`, `output/depleted_call.json`, `output/analysis.py`, and `output/report.md`. Document QC, normalization, annotation evidence and uncertainty.**
- Gates: both samples; fractions valid/sum within tolerance; one call or explicit ambiguity; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS04-2 `ls04-perturbseq-reference-map`

- Domain/subdomain: single-cell / Perturb-seq mapping; P0; L3, 90 min; D/P/A/O; CompBioBench `perturb-seq-align-q1`.
- Inputs: query and reference `.h5ad` files.
- Prompt: **Map query perturbation groups to the labeled reference across the cell-type shift and identify the query guide IDs corresponding to PABPC1, NUDT21 and LEO1. Write `output/guide_mapping.csv` with `target_gene,query_guide_id,score,runner_up_score,confidence`, `output/analysis.py`, and `output/report.md`. Prevent target metadata leakage and quantify ambiguity.**
- Gates: exactly three target genes; unique guide call per target; finite scores; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS04-3 `ls04-spatial-deconvolution`

- Domain/subdomain: single-cell / spatial transcriptomics; P0; L2, 45 min; D/P/A/O; CompBioBench `spatial-sim-q1`.
- Inputs: `inputs/spatial.sim.tar.gz`.
- Prompt: **Use the supplied single-cell reference and Visium data to identify the cell type or mixture represented at `Spot_710-1`. Write `output/spot_710_composition.csv` with `cell_type,weight,evidence`, `output/analysis.py`, and `output/report.md`. Weights must be nonnegative and sum to 1 within 0.01; do not force a single type if a mixture is supported.**
- Gates: target spot exists; valid labels; normalized weights; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS05-1 `ls05-protein-shape`

- Domain/subdomain: structural biology / geometry health check; P0; L1, 20 min; D/P/V/O; CompBioBench `protein-shape-q1`.
- Inputs: `inputs/protein.shape.q1.pdb`.
- Prompt: **Inspect the supplied PDB geometry and determine which one of `B,D,F,H,J,L,N,P,R,T,V,X,Z` it most resembles. Write `output/shape_call.json` with `letter,confidence,orientation_notes` and `output/shape_view.png`. Use only the supplied structure.**
- Gates: allowed letter; valid nonempty PNG; confidence 0–1.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS05-2 `ls05-structure-model-ranking`

- Domain/subdomain: structural biology / model confidence; P0; L2, 35 min; D/P/A/O; benchmark-informed local extension (not an upstream benchmark item).
- Inputs: model and residue metric CSVs plus the frozen `SCORING_RULE.md`; provenance and limits are documented in `ls05-local-extension-provenance.md`.
- Prompt: **Using only the files in `inputs/`, rank every supplied structural model exactly according to `inputs/SCORING_RULE.md`. Write `output/model_ranking.csv` with `rank,model_id,global_score,interface_score,critical_residue_risk,decision`, `output/analysis.py`, and `output/report.md`. Explain how chain-mapping completeness and critical-region uncertainty affect the ranking. Do not claim coordinate-level, interface, or experimental properties that are not present in the inputs.**
- Gates: every model once; unique ranks; input metrics preserved; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS05-3 `ls05-low-confidence-pocket`

- Domain/subdomain: structural biology / pocket uncertainty; P0; L2, 35 min; D/P/A/O; benchmark-informed local extension (not an upstream benchmark item).
- Inputs: confidence and mutation-candidate CSVs plus the frozen `SCORING_RULE.md`; provenance and limits are documented in `ls05-local-extension-provenance.md`.
- Prompt: **Using only the files in `inputs/`, assess whether the nominated pocket is reliable enough to prioritize mutations, following `inputs/SCORING_RULE.md` exactly. Write `output/mutation_priorities.csv` with `rank,mutation,pocket_support,confidence_penalty,decision`, `output/pocket_assessment.json`, `output/analysis.py`, and `output/report.md`. Propagate pLDDT/PAE uncertainty and do not describe predicted ΔΔG/activity as measured effects.**
- Gates: all candidates once; ranks unique; confidence evidence traceable; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS06-1 `ls06-eno1-effect-size`

- Domain/subdomain: proteomics / effect size; P0; L2, 35 min; D/P/A/O; BixBench `bix-37-q1/q4`.
- Inputs: two workbooks; proteomics workbook is the analysis target.
- Prompt: **Using the supplied proteomics results, calculate ENO1 tumor-versus-normal fold change and log2 fold change. Write `output/eno1_effect.json` with `gene,tumor_value,normal_value,fold_change,log2_fold_change,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. State the fold-change direction and do not substitute the unrelated workbook.**
- Gates: ENO1 exact; source traceable; positive FC; log2 consistency; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS06-2 `ls06-eno1-significance-audit`

- Domain/subdomain: proteomics / multiple testing; P0; L2, 30 min; D/P/A/O; BixBench `bix-37-q3`.
- Inputs: same two workbooks; proteomics workbook is target.
- Prompt: **Retrieve ENO1's adjusted p-value from the supplied proteomics results and give a threshold-calibrated interpretation at FDR 0.05. Write `output/eno1_significance.json` with `gene,adjusted_p_value,fdr_threshold,significant,source_file,source_sheet`, `output/analysis.py`, and `output/report.md`. Do not relabel a raw p-value as adjusted.**
- Gates: exact gene/source; finite p in [0,1]; significance boolean consistent; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS07-1 `ls07-combination-treatment-deg`

- Domain/subdomain: transcriptomics / differential expression; P1; L3, 75 min; D/P/T/A/O; BixBench `bix-43-q3`.
- Inputs: counts, sample layout and Ensembl mapping.
- Prompt: **Run the frozen combination-treatment contrast against its specified comparator using the sample layout. Write `output/differential_expression.csv` with `gene_id,gene_name,baseMean,log2FoldChange,pvalue,padj,pass`, `output/summary.json` with the number passing `padj<0.05`, `abs(log2FoldChange)>0.5`, and `baseMean>10`, `output/analysis.py`, and `output/report.md`. Preserve independent-filtering missing values as null.**
- Gates: design/contrast recorded; unique gene IDs; pass rule exact; summary equals rows; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS07-2 `ls07-combination-treatment-mechanism`

- Domain/subdomain: systems biology / pathway mechanism; P1; L3, 90 min; D/P/T/A/R/O; BixBench `bix-43-q5`.
- Inputs: same expression inputs plus evaluator-pinned Reactome gene sets (to be added).
- Prompt: **Using the frozen differential-expression rule and supplied Reactome release, identify the best-supported primary mechanism of the combination treatment. Write `output/pathway_enrichment.csv` with `pathway_id,pathway_name,overlap,p_value,padj,direction`, `output/mechanism_call.json`, `output/analysis.py`, and `output/report.md` (≤500 words). Distinguish enrichment from demonstrated causation.**
- Gates: pinned release/universe; valid corrected statistics; mechanism supported by table; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS08-1 `ls08-multiome-column-match`

- Domain/subdomain: multi-omics / modality alignment; P1; L3, 75 min; D/P/A/O; CompBioBench `multiome-match-atac-rna-q1`.
- Inputs: ATAC-bin and RNA-TPM tables.
- Prompt: **Recover the one-to-one matching between the eight permuted ATAC population columns and RNA populations. Write `output/column_mapping.csv` with `rna_population,atac_column,match_score,runner_up_score`, `output/score_matrix.csv`, `output/analysis.py`, and `output/report.md`. Enforce a bijection and explain the shared biological signal used.**
- Gates: all eight each side exactly once; finite scores; bijection; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS08-2 `ls08-enhancer-promoter-integration`

- Domain/subdomain: multi-omics / regulatory integration; P1; L2, 45 min; D/P/A/O; CompBioBench `ep-interactions-q1`.
- Inputs: Hi-C and CRISPR-expression CSVs.
- Prompt: **Integrate the supplied Hi-C and CRISPR-expression evidence for all candidate enhancer-promoter pairs and identify the least supported causal pair. Write `output/pair_evidence.csv` with `pair_id,contact_evidence,perturbation_effect,combined_support,rank`, `output/least_supported.json`, `output/analysis.py`, and `output/report.md`. Treat physical contact and perturbation evidence as distinct.**
- Gates: every candidate once; unique ranks; call matches minimum combined support; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS09-1 `ls09-opentrons-sop`

- Domain/subdomain: lab automation / Opentrons planning; P1; L2, 45 min; D/P/X/O; custom.
- Inputs: SOP and labware CSV plus missing validated definitions/deck map to be added.
- Prompt: **Translate the supplied SOP into an auditable Opentrons protocol plan. Write `output/protocol.py`, `output/transfer_plan.csv` with `step,source,destination,volume_uL,pipette,tip_policy`, `output/simulation.txt`, and `output/report.md`. Respect labware, deck, pipette and volume constraints; abort with explicit errors rather than guessing missing physical details.**
- Gates: simulation success; valid wells/volumes/pipettes; liquid balance; no undeclared labware; deterministic script.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS09-2 `ls09-plate-dilution-recovery`

- Domain/subdomain: lab automation / liquid handling recovery; P1; L2, 40 min; D/P/A/O; custom.
- Inputs: dilution request, pipettes and run log plus missing plate/source map to be added.
- Prompt: **Diagnose the failed dilution run and produce a physically feasible recovery plan. Write `output/root_cause.json`, `output/recovery_plan.csv` with `step,source,destination,transfer_uL,transfer_pipette,diluent_source,diluent_uL,diluent_pipette,final_concentration,final_volume_uL`, `output/analysis.py`, and `output/report.md`. Enforce pipette ranges, mass balance and supplied solvent/volume limits.**
- Gates: root cause traceable; all transfers feasible; concentrations/mass balance correct; no overdraw; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS10-1 `ls10-neun-power-analysis`

- Domain/subdomain: biostatistics / power; P1; L2, 40 min; D/P/A/O; BixBench `bix-19-q1/q2`.
- Inputs: `inputs/NeuN_quantification.csv`.
- Prompt: **Estimate the standardized mean difference (Cohen's d) between the two supplied groups and the required equal sample size per group for a two-sided independent t-test at alpha 0.05 and power 0.80. Write `output/power_result.json` with `group_labels,n_each,means,sds,pooled_sd,cohens_d,alpha,power,alternative,required_n_per_group`, `output/analysis.py`, and `output/report.md`. Round required n upward.**
- Gates: correct grouping; signed d convention stated; finite stats; ceiling rule; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## LS10-2 `ls10-treatment-response-model`

- Domain/subdomain: biostatistics / logistic regression; P1; L2, 45 min; D/P/A/O; BixBench `bix-51-q3/q4`.
- Inputs: `inputs/data.xlsx`.
- Prompt: **Fit a logistic regression for the binary treatment-response outcome using BMI, age and gender. Use complete cases, document outcome coding and gender reference level, and report the age log-odds coefficient and two-sided p-value. Write `output/model_coefficients.csv` with `term,estimate,std_error,z,p_value,odds_ratio`, `output/model_metadata.json`, `output/analysis.py`, and `output/report.md`.**
- Gates: specified model only; coding/reference documented; unique terms; coefficient/p-value finite; rerun.
- Deterministic 80: authoritative five-component allocation is the task row in `deterministic-rubrics-v2.tsv`.
- Ablation: C0/T0 baseline. In T1/T2 expose the full experiment-approved 222-catalog subset; the agent autonomously decides which and how many capabilities to install/call, including choosing none. Record all choices; the operator provides no capability routing.

## Shared acceptance before a card enters the main result

1. A reference submission passes its oracle in 3/3 clean reruns.
2. Empty output and at least one format-correct scientific error fail in 3/3 reruns.
3. A second reviewer confirms prompt, hard gates, source provenance and lack of answer leakage.
4. Two operators complete the run within 1.5× the card limit without scientific intervention.
5. The frozen artifact can be rescored offline with no network access.
