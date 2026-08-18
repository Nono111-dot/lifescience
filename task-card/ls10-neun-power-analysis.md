# Task card: `ls10-neun-power-analysis`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

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
