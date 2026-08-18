# Task card: `ls03-atac-sample-swap`

> Canonical participant-facing card generated from `docs/task-cards/ls01-ls05-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

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
