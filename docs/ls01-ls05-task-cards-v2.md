# LS01–LS05 task cards v2

These fifteen cards normalize the reviewed rich-text task set to the §3.1 repository contract. Prompts are paste-once text. Expected answers, gold artifacts and oracle-only fixtures are never agent-visible. The authoritative deterministic allocation is `docs/deterministic-rubrics-v2.tsv`: coverage 10, core science 40, direction/decision 15, summary consistency 5 and script/reproducibility 10.

A structurally complete card is not automatically released. The formal status and blocker shown on each card are fail-closed and are controlled by `docs/input-problem-inventory-v1.tsv` plus independent acceptance evidence.

## LS01-1｜CRISPR guide 活性与脱靶风险排名 — `ls01-grna-offtarget-rank`

**Formal status:** `ready` — Ranking rule, task-specific gold and accepted static oracle are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls01-grna-offtarget-rank |
| Domain / sub-domain | molecular biology / CRISPR design |
| Level / time | L2, 40 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | source: custom fixture |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/RANKING_RULE.md` — 970 bytes
- `inputs/candidates.csv` — 246 bytes
- `inputs/off_targets.csv` — 295 bytes

**Total:** 1,511 bytes (0.00 MiB).

### Prompt（运行时仅复制本框）

> Read the two supplied CSV files and rank all candidate guides by on-target activity and annotated off-target risk. Do not fetch external data or alter inputs. Write output/ranked_guides.csv with rank,guide_id,on_target_score,risk_class,decision,rationale, output/analysis.py, and output/report.md. Rankings must be unique; every input guide must appear once; explicitly treat coding/exonic near matches and mismatch count as safety evidence and state any trade-off rather than hiding it.

### Deliverables / Output contract

output/ranked_guides.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ all guides exactly once

□ unique integer ranks 1..N

□ numeric values traceable to inputs

□ decisions/rationales nonempty

□ script reruns cleanly

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | All input guide IDs appear exactly once; required columns parse. |
| Core science | 40 | Guide ranks reproduce frozen activity/off-target risk rule, including coding near matches and mismatch weighting. |
| Direction / decision | 15 | Recommended/reject decisions agree with rank and frozen safety thresholds. |
| Summary consistency | 5 | Report states top choice and essential trade-off consistently with table. |
| Script / reproducibility | 10 | analysis.py exists, parses statically, uses relative inputs/output paths and recreates declared machine-readable artifacts. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS01-2｜引物—转录本特异性审计 — `ls01-primer-transcript-audit`

**Formal status:** `ready` — The malformed CDS metadata is an intentional auditable defect; expected binding and defect calls are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls01-primer-transcript-audit |
| Domain / sub-domain | molecular biology / primer specificity |
| Level / time | L2, 40 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | custom |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/primer_candidates.csv` — 247 bytes
- `inputs/transcripts.fa` — 276 bytes

**Total:** 523 bytes (0.00 MiB).

### Prompt（运行时仅复制本框）

> Audit every primer pair against the supplied transcript isoforms. Write output/primer_audit.csv with pair_id,transcripts_matched,amplicon_length,cds_compatible,status,reason, output/analysis.py, and output/report.md. Use only supplied sequences; report malformed or internally inconsistent sequence metadata rather than silently repairing it.

### Deliverables / Output contract

output/primer_audit.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ every pair once

□ sequence/coordinate validation reported

□ no fabricated bases

□ finite lengths

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | All primer pairs and transcript identifiers are covered without duplicates. |
| Core science | 40 | Primer binding, orientation, amplicon lengths and transcript/CDS compatibility match frozen sequence calculations. |
| Direction / decision | 15 | Pass/fail/malformed decisions agree with computed binding and metadata validation. |
| Summary consistency | 5 | Report identifies selected pair or explicit no-valid-pair outcome consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS01-3｜表达载体 ORF 与克隆兼容性审计 — `ls01-vector-orf-audit`

**Formal status:** `ready` — ORF/tag audit rules, construct-level gold and accepted static oracle are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls01-vector-orf-audit |
| Domain / sub-domain | molecular biology / construct QC |
| Level / time | L2, 35 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | custom |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/AUDIT_RULE.md` — 704 bytes
- `inputs/constructs.csv` — 262 bytes

**Total:** 966 bytes (0.00 MiB).

### Prompt（运行时仅复制本框）

> Audit each construct for start/stop codons, reading frame, tag/linker compatibility and cloning flags represented in the input. Write output/construct_audit.csv with construct_id,frame_ok,start_ok,stop_ok,tag_ok,overall_status,issues, output/analysis.py, and output/report.md. Do not infer sequence features that are absent from the input.

### Deliverables / Output contract

output/construct_audit.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ every construct once

□ boolean fields valid

□ issues agree with status

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Every construct is present once with required audit fields. |
| Core science | 40 | Start/stop, frame, tag/linker and cloning checks match frozen rules. |
| Direction / decision | 15 | Overall status and issue labels agree with component checks. |
| Summary consistency | 5 | Report names usable constructs and blocking defects consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS02-1｜嵌合有害 nonsense SNV 识别 — `ls02-deleterious-mutation`

**Formal status:** `ready` — GRCh38 chr9, GENCODE v47 chr9 annotation, read evidence and transcript-aware gold are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls02-deleterious-mutation |
| Domain / sub-domain | genomics / variant calling |
| Level / time | L3, 90 min |
| Priority | P0 |
| Anchor / related | D / P, T, A, R, O |
| Source idea | CompBioBench deleterious-mutation-q2 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/deleterious.mutation.q2.R1.fq.gz` — 53,964,925 bytes
- `inputs/reference/GRCh38_chr9.fa.gz` — 36,554,007 bytes
- `inputs/reference/README.md` — 584 bytes
- `inputs/reference/gencode.v47.chr9.annotation.gtf.gz` — 2,358,409 bytes

**Total:** 92,877,925 bytes (88.58 MiB).

### Prompt（运行时仅复制本框）

> Analyze the supplied chr9 exome reads to identify the high-confidence mosaic nonsense SNV in a highly loss-of-function-intolerant protein-coding gene. Write output/variant.tsv with chrom,pos,ref,alt,gene,consequence,alt_reads,total_reads,allele_fraction, output/evidence.json, output/analysis.py, and output/report.md. Report allele fraction as 0–1 and document reference/annotation versions.

### Deliverables / Output contract

output/variant.tsv

output/evidence.json

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ one valid variant

□ coordinates/reference consistent

□ read counts support AF

□ consequence/gene supported

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Required variant/evidence artifacts parse and cover the nominated call. |
| Core science | 40 | Chromosome, position, alleles, HGNC gene, nonsense consequence, read counts and allele fraction match frozen gold/tolerances. |
| Direction / decision | 15 | High-confidence mosaic/deleterious call agrees with evidence and constraint rule. |
| Summary consistency | 5 | Report gives the same gene/variant/AF and calibrated caveat. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS02-2｜浅层双端测序大片段缺失定位 — `ls02-find-deletion`

**Formal status:** `ready` — GRCh38 chr22, breakpoint evidence, tolerances and accepted static oracle are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls02-find-deletion |
| Domain / sub-domain | genomics / structural variation |
| Level / time | L3, 75 min |
| Priority | P0 |
| Anchor / related | D / P, T, A, R, O |
| Source idea | CompBioBench find-deletion-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/find.deletion.r1.fq.gz` — 16,705,359 bytes
- `inputs/find.deletion.r2.fq.gz` — 16,701,241 bytes
- `inputs/reference/GRCh38_chr22.fa.gz` — 11,147,284 bytes
- `inputs/reference/README.md` — 295 bytes

**Total:** 44,554,179 bytes (42.49 MiB).

### Prompt（运行时仅复制本框）

> Locate the large deletion in the supplied shallow paired-end hg38 data. Write output/deletion.tsv with chrom,start_100kb,end_100kb,size_bp,supporting_signals, output/qc.json, output/analysis.py, and output/report.md. Round breakpoints to the nearest 100 kb and distinguish evidence from precision limits.

### Deliverables / Output contract

output/deletion.tsv

output/qc.json

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ one interval, start<end, hg38 coordinates, support nonempty, rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Required interval/QC artifacts parse and contain one nominated event. |
| Core science | 40 | Chromosome, rounded breakpoints and size match frozen gold within declared tolerances; support fields are present. |
| Direction / decision | 15 | Deletion/no-deletion decision agrees with coverage/pair evidence. |
| Summary consistency | 5 | Report repeats interval and precision limit consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS02-3｜VCF 基因组版本推断 — `ls02-infer-genome-build`

**Formal status:** `ready` — hg18/hg19/hg38 chr20 references and match-rate gold are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls02-infer-genome-build |
| Domain / sub-domain | genomics / coordinate normalization |
| Level / time | L2, 40 min |
| Priority | P0 |
| Anchor / related | D / P, T, A, O |
| Source idea | CompBioBench vcf-infer-build-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/references/README.md` — 563 bytes
- `inputs/references/hg18_chr20.fa.gz` — 19,496,195 bytes
- `inputs/references/hg19_chr20.fa.gz` — 18,072,551 bytes
- `inputs/references/hg38_chr20.fa.gz` — 18,840,364 bytes
- `inputs/references/reference_manifest.json` — 1,108 bytes
- `inputs/vcf.infer.build.q1.vcf.gz` — 3,788,749 bytes

**Total:** 60,199,530 bytes (57.41 MiB).

### Prompt（运行时仅复制本框）

> Determine whether the supplied chr20 VCF uses hg18, hg19, hg38 or T2T coordinates. Write output/build_call.json with build,confidence,n_variants_checked,n_ref_matches,n_ref_mismatches,evidence, output/analysis.py, and output/report.md. Base the call on reproducible allele/coordinate checks and do not treat chromosome naming alone as proof.

### Deliverables / Output contract

output/build_call.json

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ allowed build label

□ counts nonnegative

□ evidence present

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Build artifact parses and diagnostic counts are complete. |
| Core science | 40 | Reference-allele checks and final build match frozen diagnostic loci/gold. |
| Direction / decision | 15 | Confidence/call direction agrees with match-versus-mismatch evidence. |
| Summary consistency | 5 | Report states build and strongest evidence consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS03-1｜高表达隐蔽外显子识别 — `ls03-cryptic-exon`

**Formal status:** `ready` — GRCh38 chr9, Ensembl 112 coding exons, junction supports and accepted static oracle are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls03-cryptic-exon |
| Domain / sub-domain | transcriptomics / splicing |
| Level / time | L3, 90 min |
| Priority | P0 |
| Anchor / related | D / P, T, A, R, O |
| Source idea | CompBioBench cryptic-exon-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/cryptic.exon.q1.fq.gz` — 16,920,968 bytes
- `inputs/reference/GRCh38_chr9.fa.gz` — 36,554,007 bytes
- `inputs/reference/README.md` — 505 bytes
- `inputs/reference/ensembl112_protein_coding_exons.tsv.gz` — 6,339,899 bytes

**Total:** 59,815,379 bytes (57.04 MiB).

### Prompt（运行时仅复制本框）

> Identify the protein-coding HGNC gene containing the highly expressed cryptic exon supported by two novel splice junctions. Write output/cryptic_exon.tsv with gene,chrom,start,end,left_junction_reads,right_junction_reads,expression_evidence, output/junctions.tsv, output/analysis.py, and output/report.md. Novelty must be assessed against the supplied annotation version.

### Deliverables / Output contract

output/cryptic_exon.tsv

output/junctions.tsv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ one gene/interval

□ two flanking novel junctions

□ read support finite

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Gene, exon and both junction artifacts are complete and parseable. |
| Core science | 40 | HGNC gene, exon coordinates and two novel junctions/read supports match frozen gold/tolerances. |
| Direction / decision | 15 | Cryptic-exon decision agrees with novelty and bilateral junction support. |
| Summary consistency | 5 | Report repeats gene/exon and evidence consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS03-2｜bulk ATAC-seq 样本标签互换检测 — `ls03-atac-sample-swap`

**Formal status:** `ready` — AmexT v47 annotation, 105-pair schema, GEO cross-check and Cloaca/Stomach gold are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls03-atac-sample-swap |
| Domain / sub-domain | epigenomics / sample QC |
| Level / time | L3, 75 min |
| Priority | P0 |
| Anchor / related | D / P, A, V, O |
| Source idea | CompBioBench sample-swap-atac-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/AmexT_v47-AmexG_v6.0-DD.gtf.gz` — 51,302,807 bytes
- `inputs/REFERENCE_NOTES.md` — 811 bytes
- `inputs/sample.swap.atac.q1.chrom.sizes` — 1,133 bytes
- `inputs/sample.swap.atac.q1.tsv.gz` — 75,204,929 bytes

**Total:** 126,509,680 bytes (120.65 MiB).

### Prompt（运行时仅复制本框）

> Determine whether two organ labels are swapped in the axolotl bulk ATAC-seq data. Write output/swap_call.json with swap_detected,organ_a,organ_b,confidence,evidence, output/sample_similarity.csv, output/analysis.py, and output/report.md. If evidence does not support a unique swap, return swap_detected=false and explain uncertainty.

### Deliverables / Output contract

output/swap_call.json

output/sample_similarity.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ valid organ labels or null

□ symmetric swap

□ finite similarity matrix

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | All expected samples/organs and similarity entries are covered. |
| Core science | 40 | Normalized similarity structure and swapped pair match frozen reference analysis. |
| Direction / decision | 15 | Swap/no-swap decision and organ order are internally consistent. |
| Summary consistency | 5 | Report states pair or no-swap with matching confidence. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS03-3｜增强子—启动子三维距离与转录动态 — `ls03-genome-coordinates`

**Formal status:** `ready` — Distance/contact/lag definitions and the non-causal observational conclusion are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls03-genome-coordinates |
| Domain / sub-domain | regulatory genomics / live-cell dynamics |
| Level / time | L2, 45 min |
| Priority | P0 |
| Anchor / related | D / P, A, V, O |
| Source idea | CompBioBench genome-coords-q1 adapted |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/ANALYSIS_RULE.md` — 741 bytes
- `inputs/single_cell_dynamics_question.csv` — 18,361,955 bytes

**Total:** 18,362,696 bytes (17.51 MiB).

### Prompt（运行时仅复制本框）

> Analyze enhancer-promoter 3D distance and transcription dynamics across cells and time. Write output/cell_metrics.csv, output/lag_analysis.csv with lag,association,n_observations, output/analysis.py, and output/report.md. Use 260 nm as the supplied contact threshold. Separate temporal association from causation and state what the observational data cannot establish.

### Deliverables / Output contract

output/cell_metrics.csv

output/lag_analysis.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ all cells represented

□ finite metrics

□ lag direction defined

□ no categorical causal claim unsupported by intervention

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | All cells/timepoints required by the card contribute to metrics; lag table parses. |
| Core science | 40 | Contact fractions, transcription summaries and lag associations match frozen calculations/tolerances. |
| Direction / decision | 15 | Association direction is correct and no unsupported causal direction is asserted. |
| Summary consistency | 5 | Report states the supported temporal conclusion and limitation consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS04-1｜视网膜单细胞差异组成分析 — `ls04-differential-composition`

**Formal status:** `ready` — Marker panel, annotation rule, composition counts and depleted-cell gold are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls04-differential-composition |
| Domain / sub-domain | single-cell / composition |
| Level / time | L3, 90 min |
| Priority | P0 |
| Anchor / related | D / P, T, A, R, O |
| Source idea | CompBioBench differential-composition-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/ANNOTATION_RULE.md` — 724 bytes
- `inputs/MARKER_PANEL.tsv` — 673 bytes
- `inputs/differential.composition.q1.1.mtx.gz` — 29,076,744 bytes
- `inputs/differential.composition.q1.2.mtx.gz` — 31,011,024 bytes
- `inputs/differential.composition.q1.genes.txt.gz` — 223,316 bytes

**Total:** 60,312,481 bytes (57.52 MiB).

### Prompt（运行时仅复制本框）

> Compare the two retinal single-cell expression matrices and identify the cell population that is severely depleted in sample 2. Write output/composition.csv with sample,cell_type,n_cells,fraction, output/depleted_call.json, output/analysis.py, and output/report.md. Document QC, normalization, annotation evidence and uncertainty.

### Deliverables / Output contract

output/composition.csv

output/depleted_call.json

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ both samples

□ fractions valid/sum within tolerance

□ one call or explicit ambiguity

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Both samples and all frozen cell-type labels are represented; fractions parse. |
| Core science | 40 | Cell counts/fractions and depleted population match frozen annotation/composition gold. |
| Direction / decision | 15 | Depletion direction is sample-2 relative to sample-1 and agrees with fractions. |
| Summary consistency | 5 | Report states depleted population and magnitude consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS04-2｜Perturb-seq 查询—参考映射 — `ls04-perturbseq-reference-map`

**Formal status:** `ready` — Feature alignment, pseudobulk transform, Hungarian assignment and mapping gold are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls04-perturbseq-reference-map |
| Domain / sub-domain | single-cell / Perturb-seq mapping |
| Level / time | L3, 90 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | CompBioBench perturb-seq-align-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/perturb.seq.align.q1.query.h5ad` — 19,163,116 bytes
- `inputs/perturb.seq.align.q1.ref.h5ad` — 41,142,620 bytes

**Total:** 60,305,736 bytes (57.51 MiB).

### Prompt（运行时仅复制本框）

> Map query perturbation groups to the labeled reference across the cell-type shift and identify the query guide IDs corresponding to PABPC1, NUDT21 and LEO1. Write output/guide_mapping.csv with target_gene,query_guide_id,score,runner_up_score,confidence, output/analysis.py, and output/report.md. Prevent target metadata leakage and quantify ambiguity.

### Deliverables / Output contract

output/guide_mapping.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ exactly three target genes

□ unique guide call per target

□ finite scores

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Exactly PABPC1, NUDT21 and LEO1 occur once with unique query guide calls. |
| Core science | 40 | Three guide identities and mapping scores/ranking match frozen leak-free reference analysis. |
| Direction / decision | 15 | Confidence/ambiguity decisions agree with best and runner-up scores. |
| Summary consistency | 5 | Report repeats all three mappings consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS04-3｜空间转录组目标 Spot 反卷积 — `ls04-spatial-deconvolution`

**Formal status:** `ready` — NNLS mixture weights, support threshold and accepted static oracle are frozen.

| 字段 | 内容 |
| --- | --- |
| ID | ls04-spatial-deconvolution |
| Domain / sub-domain | single-cell / spatial transcriptomics |
| Level / time | L2, 45 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | CompBioBench spatial-sim-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/spatial.sim.tar.gz` — 2,174,692 bytes

**Total:** 2,174,692 bytes (2.07 MiB).

### Prompt（运行时仅复制本框）

> Use the supplied single-cell reference and Visium data to identify the cell type or mixture represented at Spot_710-1. Write output/spot_710_composition.csv with cell_type,weight,evidence, output/analysis.py, and output/report.md. Weights must be nonnegative and sum to 1 within 0.01; do not force a single type if a mixture is supported.

### Deliverables / Output contract

output/spot_710_composition.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ target spot exists

□ valid labels

□ normalized weights

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Target spot exists; every reported type is valid; weights cover the full call. |
| Core science | 40 | Cell-type identity/mixture weights match frozen spatial reference within tolerance. |
| Direction / decision | 15 | Single-type versus mixture decision agrees with weights and uncertainty rule. |
| Summary consistency | 5 | Report repeats composition and uncertainty consistently. |
| Script / reproducibility | 10 | Standard static rerunnable-script checks. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS05-1｜PDB 蛋白几何字母形状识别 — `ls05-protein-shape`

**Formal status:** `ready_local_extension` — Geometry/PCA shape gold and view-metadata contract are frozen; report separately as a local-extension calibration task.

| 字段 | 内容 |
| --- | --- |
| ID | ls05-protein-shape |
| Domain / sub-domain | structural biology / geometry health check |
| Level / time | L1, 20 min |
| Priority | P0 |
| Anchor / related | D / P, V, O |
| Source idea | CompBioBench protein-shape-q1 |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/protein.shape.q1.pdb` — 1,558,926 bytes

**Total:** 1,558,926 bytes (1.49 MiB).

### Prompt（运行时仅复制本框）

> Inspect the supplied PDB geometry and determine which one of B,D,F,H,J,L,N,P,R,T,V,X,Z it most resembles. Write output/shape_call.json with letter,confidence,orientation_notes and output/shape_view.png. Use only the supplied structure.

### Deliverables / Output contract

output/shape_call.json

output/shape_view.png.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

### Hard gates

□ allowed letter

□ valid nonempty PNG

□ confidence 0–1

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | Call JSON and PNG exist and parse; allowed letter vocabulary enforced. |
| Core science | 40 | Letter identity matches frozen visual/geometric gold. |
| Direction / decision | 15 | Orientation/confidence decision is valid and consistent with call. |
| Summary consistency | 5 | Orientation note concisely supports the same letter. |
| Script / reproducibility | 10 | No script points for L1 unless optional script meets standard; remaining points require valid reproducible view metadata. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS05-2｜结构模型置信度综合排名 — `ls05-structure-model-ranking`

**Formal status:** `ready_local_extension` — Frozen rule, gold, accepted oracle and 3/3 acceptance tests present; synthetic fixture, not upstream benchmark.

| 字段 | 内容 |
| --- | --- |
| ID | ls05-structure-model-ranking |
| Domain / sub-domain | structural biology / model confidence |
| Level / time | L2, 35 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | benchmark-informed local extension (not an upstream benchmark item) |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/SCORING_RULE.md` — 1,518 bytes
- `inputs/model_metrics.csv` — 164 bytes
- `inputs/residue_errors.csv` — 162 bytes

**Total:** 1,844 bytes (0.00 MiB).

### Prompt（运行时仅复制本框）

> Using only the files in inputs/, rank every supplied structural model exactly according to inputs/SCORING_RULE.md. Write output/model_ranking.csv with rank,model_id,global_score,interface_score,critical_residue_risk,decision, output/analysis.py, and output/report.md. Explain how chain-mapping completeness and critical-region uncertainty affect the ranking. Do not claim coordinate-level, interface, or experimental properties that are not present in the inputs.

### Deliverables / Output contract

output/model_ranking.csv

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ every model once

□ unique ranks

□ input metrics preserved

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | 10: every model occurs once, ranks are unique, and all required artifacts parse. |
| Core science | 40 | 40: exact rank tuple/order (20) plus nine frozen global/interface/critical-risk fields prorated (20). |
| Direction / decision | 15 | 15: three preferred/alternate/reject decisions prorated against frozen gold. |
| Summary consistency | 5 | 5: report names model_A and identifies model_B's incomplete mapping consistently. |
| Script / reproducibility | 10 | 10: analysis.py parses and contains no absolute user path; submission code is never imported by oracle. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.

## LS05-3｜低置信度口袋与突变优先级评估 — `ls05-low-confidence-pocket`

**Formal status:** `ready_local_extension` — Frozen pLDDT/PAE rule, gold, accepted oracle and 3/3 acceptance tests present; synthetic fixture, not upstream benchmark.

| 字段 | 内容 |
| --- | --- |
| ID | ls05-low-confidence-pocket |
| Domain / sub-domain | structural biology / pocket uncertainty |
| Level / time | L2, 35 min |
| Priority | P0 |
| Anchor / related | D / P, A, O |
| Source idea | benchmark-informed local extension (not an upstream benchmark item) |
| Card version | task-cards-v2.md |

### Inputs (authoritative packaged inventory)
- `inputs/SCORING_RULE.md` — 1,753 bytes
- `inputs/confidence.csv` — 142 bytes
- `inputs/mutation_candidates.csv` — 167 bytes

**Total:** 2,062 bytes (0.00 MiB).

### Prompt（运行时仅复制本框）

> Using only the files in inputs/, assess whether the nominated pocket is reliable enough to prioritize mutations, following inputs/SCORING_RULE.md exactly. Write output/mutation_priorities.csv with rank,mutation,pocket_support,confidence_penalty,decision, output/pocket_assessment.json, output/analysis.py, and output/report.md. Propagate pLDDT/PAE uncertainty and do not describe predicted ΔΔG/activity as measured effects.

### Deliverables / Output contract

output/mutation_priorities.csv

output/pocket_assessment.json

output/analysis.py

output/report.md.

所有 CSV/TSV/JSON 必须可解析；ID 唯一；数值 finite；缺失值使用空字段或 null。

可重跑脚本必须只使用相对 inputs/ 与 output/ 路径；grader 不直接 import 未受信提交代码。

### Hard gates

□ all candidates once

□ ranks unique

□ confidence evidence traceable

□ rerun

### Ablation（不进入 Prompt）

`C0` uses no added life-science capability. In `T1`, task-appropriate Agent Skills are predeclared from the approved workbook catalogue and installed from their fixed GitHub commit/path before a fresh Codex task starts; MCP/SCP rows are excluded. Selection uses task metadata only and cannot change after outputs are observed. Every installed skill must be removed and the isolated Codex baseline verified before the next run.

### DeterministicArtifactScore（0–80, authoritative v2）

| Component | Points | Deterministic requirement |
| --- | ---: | --- |
| Coverage / schema | 10 | 10: every mutation occurs once, ranks are unique, and all required artifacts parse. |
| Core science | 40 | 40: exact order (10), eight pocket-support/penalty fields prorated (20), and false/false calibrated pocket assessment with reason (10). |
| Direction / decision | 15 | 15: four defer/out-of-scope decisions prorated against frozen gold. |
| Summary consistency | 5 | 5: report states low confidence and deferral without prohibited experimental overclaim. |
| Script / reproducibility | 10 | 10: analysis.py parses and contains no absolute user path; submission code is never imported by oracle. |

No scientific points may be emitted until a static oracle, tolerances and correct/empty/wrong controls are independently accepted 3/3. Missing core artifact gives zero deterministic points.

### JudgeScore（0–20）

| Dimension | 0 | 3 | 5 |
| --- | --- | --- | --- |
| Evidence | No task-specific evidence, fabricated/untraceable support, or contradiction with machine-readable artifacts. | At least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete. | Every main claim links to the relevant input/result artifact; decisive measurements/rows and evidence-bound uncertainty are explicit. |
| Method | Missing or materially invalid method. | Broadly valid method with incomplete choices, direction, units or limitations. | Correct, auditable method with all consequential choices, direction, units and limitations stated. |
| Restraint | Unsupported causal/clinical/experimental claim. | Mostly calibrated but one important boundary is vague. | Claims stay within the supplied evidence and all important limitations are explicit. |
| Readability | Unusable or internally confusing report. | Understandable with notable ambiguity or clutter. | Concise, internally consistent and easy to audit against formal artifacts. |

The judge records main-claim count, supported-claim count, evidence locations and a short rationale. Judge points cannot repair a deterministic hard-gate failure.
