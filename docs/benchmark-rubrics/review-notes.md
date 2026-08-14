# 25题评分标准review结论

## Provenance census

| Source | Local tasks | What can be called native scoring |
|---|---:|---|
| CompBioBench | 12 | Public prompt, inputs, requested answer shape and metadata. Gold and correctness verifier are private server-side; no public local oracle. |
| BixBench | 6 local tasks / 9 mapped upstream questions | Public `ideal`, `eval_mode` and, for range questions, the published range. Verifier implementation is not public. |
| Custom | 7 | No benchmark-native scientific score or gold. Only source-independent format checks are currently defensible. |
| BioAgentBench | 0 | No selected row currently maps to its `single-cell` task. Its truth/results cannot be transferred merely because a local task is also single-cell. |

## Review decisions

1. `25-task-native-rubrics.tsv` is authoritative for what the upstream benchmark actually exposes. It does not award the local 80-point artifact score.
2. `deterministic-rubrics-v2.tsv` is a proposed local extension. A row becomes active only after independent recomputation or an expert hidden checklist and §7.5 acceptance; it must never be labelled the benchmark's native rubric.
3. CompBioBench-derived tasks cannot receive an “official local correctness” score from public material. Options are: submit the exact native answer to the official private leaderboard; independently derive and dual-review local gold; or keep the task calibration-only/blocked.
4. BixBench ideal/ranges may anchor the corresponding endpoint, but they do not support unlisted full-table, method-version, summary or script claims. Those are separately reviewed extensions.
5. Custom tasks require a cited source workflow, complete fixture and two reviewers, or replacement with a task that has published truth/results. Do not infer a unique answer from plausible biology.

## Source conflicts that block formal scoring

- `ep-interactions-q1`: text says eight candidates, while available options/data enumerate only seven.
- `genome-coords-q1`: public materials do not expose the causal-statement adjudication rule.
- `bix-43-q3`: question uses strict thresholds and ideal 677, while the recovered execution notebook uses inclusive thresholds and prints 679; no per-gene official gold is published.
- `bix-43-q5`: remote `Reactome_2022`/Enrichr state, background universe and mapping snapshot are not frozen.
- Primer, Opentrons and plate-dilution custom fixtures lack state required for a unique scientific answer.

## Recommended path

- Preserve the original native endpoint as one explicit criterion wherever it is public.
- Add artifact coverage, cross-file consistency and rerunnable-script checks only as labelled local extensions.
- For seven custom tasks, either replace them with explicitly mapped BioAgentBench tasks using their published results/truth, or run a separate expert-authored task acceptance process.
- Do not start headline evaluation until each included task has one deterministic grader (Python or hidden deterministic checklist) and passes correct/empty/deliberate-wrong controls 3/3.
