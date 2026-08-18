# 25题 benchmark 原生评分依据

本目录只记录上游公开材料能够支持的评分边界，不把本项目任务卡、推断答案或建议性的 `80+20` rubric 冒充为 benchmark 原生标准。

## 文件

- `25-task-native-rubrics.tsv`：25个本地 task ID 与上游题目的逐题映射。`native_*` 列是上游事实；`recommendation` 是本项目建议，不是上游评分。
- `compbiobench-details.md`：12个 CompBioBench 来源题的完整公开题面、答案形式、`internet_required` 与公开 verifier 边界。
- `bixbench-native-details.md`：6个本地BixBench任务所映射上游问题的`ideal`、`eval_mode`、输入复算边界及artifact扩展建议。
- `bioagentbench-native-details.md`：核查当前清单与BioAgentBench single-cell的真实映射，并说明其results/truth边界。
- `review-notes.md`：来源统计、冲突、正式评分决策和替换建议。

## 来源与版本边界

1. **CompBioBench**：题面和元数据取自 `Genentech/compbiobench-data-v1/compbiobench.v1.tsv`（本次核查下载时间：2026-08-14）。数据集声明 CC-BY-4.0。公开表包含 `question_id`、question、`internet_required`、输入文件等，但不包含 gold。公开 runner 负责隔离运行与答案抽取，不包含正确答案或本地 verifier。正确性只能提交到私有 server-side leaderboard 获取。因此表中的 CompBioBench `native_gold_or_range` 均明确写作 private/not public；任何本地 gold 必须标为“独立复算/人工复核”，不能声称是 benchmark 官方答案。
2. **BixBench**：取自仓库本地保存的官方数据行 `.tmp_tests/BixBench.jsonl`，version `1.5`。该文件公开 `question_id`、question、ideal、distractors 与 `eval_mode`，所以表中可如实给出 ideal/range。这里只记录 `eval_mode` 名称；未发现公开的 verifier 实现，不能推断 `str_verifier` 或 `llm_verifier` 的全部归一化、容错或提示词细节。
3. **Custom**：`new-fixture` 不是三个 benchmark 的原题，没有 benchmark 原生 prompt、gold 或 verifier。允许做格式/完整性审计；科学答案必须另立来源、独立复算和双人review。
4. 用户提到的 BioAgent-Bench single-cell 集合并未出现在 `docs/contracts/selected-tasks-v1.tsv` 的任何一行，因此当前25题没有可诚实归因于它的原生评分标准。若要采用其评分，需先把具体 task ID 映射到本地题目，不能仅凭领域相似性移植。

## 如何使用

- 先按 `native_eval_mode` 复现上游单一终点，保留原始答案格式。
- `allowed_deterministic_checks` 只列出可由题面或输入直接支持的检查；其中“独立复算”不是官方 verifier。
- Coverage 10、paired delta 40、direction 15、summary 5、script 10 属于本项目 artifact rubric。它可以在原生终点之上设计，但必须放在单独文件中并标注 extension；不得倒推为 benchmark 原生评分。
- 遇到 `known_conflict` 不应静默修题。先冻结原题与数据版本，记录冲突，再决定向作者确认、独立专家裁决或替换题目。

## 关键发现

- 12道 CompBioBench 来源题均无公开 gold/verifier；只有输出形态和题面约束可直接确定。
- 6个本地 BixBench task 实际合并了9个上游 question ID；合并题必须先分别评分原生终点。
- `ep-interactions-q1` 声称有 EP1–EP8，却只给 A–G/EP1–EP7，正式使用前必须解决。
- `genome-coords-q1` 从观察时间序列选择因果陈述，公开题面没有发布裁决规则，属于解释敏感项。
- 7道 custom 题没有 benchmark 原生科学评分，其中 primer、Opentrons、plate dilution 还存在输入/状态不足。

## 公开链接

- CompBioBench data: https://huggingface.co/datasets/Genentech/compbiobench-data-v1
- CompBioBench runner: https://github.com/Genentech/compbiobench-runner
- CompBioBench leaderboard: https://huggingface.co/spaces/Genentech/compbiobench-leaderboard-v1
- BixBench dataset: https://huggingface.co/datasets/futurehouse/BixBench
- BioAgent-Bench single-cell tasks: https://github.com/bioagent-bench/bioagent-bench/tree/master/tasks/single-cell
