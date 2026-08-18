# Task card: `ls03-genome-coordinates`

> Canonical participant-facing card generated from `docs/task-cards/ls01-ls05-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

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
