# Task card: `ls02-deleterious-mutation`

> Canonical participant-facing card generated from `docs/ls01-ls05-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

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
