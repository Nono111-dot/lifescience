# Task card: `ls04-spatial-deconvolution`

> Canonical individual task card materialized from `docs/task-cards/ls01-ls05-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

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
| Card version | task-cards-v1.md |

### Inputs

inputs/spatial.sim.tar.gz （2.07 MiB）

**输入说明：** inputs/spatial.sim.tar.gz.

仓库清单总大小：约 2.07 MiB。输入只读；缺失参考包、许可或版本信息以状态框为准。

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
