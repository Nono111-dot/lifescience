# Task card: `ls10-neun-power-analysis`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls10-neun-power-analysis`

- Inputs: `NeuN_quantification.csv` (218 bytes), two labeled groups with observed measurements. Provenance: BixBench capsule data; no decoy.
- Prompt: **Estimate the standardized mean difference (Cohen's d) between the two supplied groups and the required equal sample size per group for a two-sided independent t-test at alpha 0.05 and power 0.80. Write `output/power_result.json` with `group_labels,n_each,means,sds,pooled_sd,cohens_d,alpha,power,alternative,required_n_per_group`, `output/analysis.py`, and `output/report.md`. Round required n upward.**
- Deliverables: one JSON object with group-keyed or label-aligned arrays; report; rerunnable script. Sample SD convention and signed-d order must be stated.
- Hard gates: both groups mapped correctly; finite means/SD/pooled SD/effect size; two-sided alpha/power specification exact; sample size rounded upward.
- Deterministic 80: coverage/schema 10; means 8, SDs 8, pooled SD 6, absolute Cohen d 8 (`5e-3` tolerance), required n/group 10; specification/direction 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[power-analysis]`, `[effect-size]`, `[reproducible-code]`; expected to reduce SD convention, sidedness and rounding errors.
