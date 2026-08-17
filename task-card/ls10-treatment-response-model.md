# Task card: `ls10-treatment-response-model`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls10-treatment-response-model`

- Inputs: `data.xlsx` (22,788 bytes), sheet `Sheet1`; columns include `Efficacy`, `Age`, `Gender`, `BMI` and other non-model covariates. The target model uses only the named outcome/predictors; other columns are distractors. Provenance: BixBench capsule data.
- Prompt: **Fit a logistic regression for the binary treatment-response outcome using BMI, age and gender. Use complete cases, document outcome coding and gender reference level, and report the age log-odds coefficient and two-sided p-value. Write `output/model_coefficients.csv` with `term,estimate,std_error,z,p_value,odds_ratio`, `output/model_metadata.json`, `output/analysis.py`, and `output/report.md`.**
- Deliverables: unique coefficient rows; metadata with formula, outcome coding, reference level, complete-case count and implementation/version; report; rerunnable script.
- Hard gates: specified model only; binary outcome coding and gender reference documented; age term unique and finite; coefficient, odds ratio and significance interpretation mutually consistent.
- Deterministic 80: coverage/schema 10; age estimate, SE, two-sided p-value and odds ratio 10 each (`rel_tol=3e-3`, `abs_tol=5e-5`); age direction/decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[regression-diagnostics]`, `[categorical-coding]`, `[reproducible-code]`; expected to reduce outcome/reference-level and coefficient-interpretation errors.

## Release gate

A card enters the main result only if its reference submission passes 3/3 clean reruns, empty output and at least one format-correct scientific error fail 3/3, one domain reviewer and one grader reviewer accept it, and a timed calibration run can be frozen and rescored. On 2026-08-17, all ten cards have accepted static checkers; campaign-level reviewer and platform deviations remain governed by `formal-eval-release-status-2026-08-17.md`.
