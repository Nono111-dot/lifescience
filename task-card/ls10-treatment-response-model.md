# Task card: `ls10-treatment-response-model`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls10-treatment-response-model`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 806 bytes
- `inputs/data.xlsx` — 22,788 bytes

**Total:** 23,594 bytes (0.02 MiB).

- Prompt: **Fit a logistic regression for the binary treatment-response outcome using BMI, age and gender. Use complete cases, document outcome coding and gender reference level, and report the age log-odds coefficient and two-sided p-value. Write `output/model_coefficients.csv` with `term,estimate,std_error,z,p_value,odds_ratio`, `output/model_metadata.json`, `output/analysis.py`, and `output/report.md`.**
- Deliverables: unique coefficient rows; metadata with formula, outcome coding, reference level, complete-case count and implementation/version; report; rerunnable script.
- Hard gates: specified model only; binary outcome coding and gender reference documented; age term unique and finite; coefficient, odds ratio and significance interpretation mutually consistent.
- Deterministic 80: coverage/schema 10; age estimate, SE, two-sided p-value and odds ratio 10 each (`rel_tol=3e-3`, `abs_tol=5e-5`); age direction/decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[biostatistics]`, `[regression-diagnostics]`, `[categorical-coding]`, `[reproducible-code]`; expected to reduce outcome/reference-level and coefficient-interpretation errors.

## Release gate

A card enters the main result only if its reference submission passes 3/3 clean reruns, empty output and at least one format-correct scientific error fail 3/3, one domain reviewer and one grader reviewer accept it, and a timed calibration run can be frozen and rescored. On 2026-08-17, all ten cards have accepted static checkers; campaign-level reviewer and platform deviations remain governed by `formal-eval-release-status-2026-08-17.md`.
