# BixBench evidence for LS06 and LS10

## Provenance boundary

Checked against `futurehouse/BixBench` `BixBench.jsonl`, benchmark version `1.5`, downloaded from the official Hugging Face repository on 2026-08-14. Dataset license is Apache-2.0 according to the dataset card. Official metadata contains question text, `ideal`, distractors, capsule UUID/data archive, paper, and `eval_mode`; it does **not** contain the implementation of the verifier, a per-field 80-point rubric, dependency versions, or a reference analysis script. Dataset: <https://huggingface.co/datasets/futurehouse/BixBench>; metadata file: <https://huggingface.co/datasets/futurehouse/BixBench/blob/main/BixBench.jsonl>.

The four local tasks combine multiple native questions and demand richer artifacts. The benchmark-native checks below are kept distinct from the proposed artifact checks. No benchmark-absent scientific value is treated as native gold.

## LS06-1 `ls06-eno1-effect-size`

- Capsule: `40cbef03-b5c3-4448-b00f-0ba2965dea9b`; archive `CapsuleFolder-40cbef03-b5c3-4448-b00f-0ba2965dea9b.zip`; cited dataset DOI `10.17632/dj4sb8h3c3.1`.
- `bix-37-q1`: native ideal `4.81-fold increase in tumor`; native `eval_mode=llm_verifier`.
- `bix-37-q4`: native ideal `2.27`; native `eval_mode=str_verifier`.
- Independently reproducible from the frozen workbook, sheet `Tumor vs Normal`, unique `gene=ENO1` row: Normal `72896133.2946858`, Tumor `350385456.451912`, Ratio/FC `4.81`, log2FC `2.27`.
- Native standard: answer equivalence for q1 and string value for q4. Benchmark does not natively require JSON schema, source fields, report, script, exact raw abundance values, or an 80-point allocation.
- Proposed extension used by the local oracle: raw Normal 10, raw Tumor 10, FC 10, log2FC 10; positive tumor direction 15; report agreement 5. These extensions are independently derivable from the supplied input, not claimed as BixBench-native.
- Status: **ready for oracle calibration**, subject to independent reviewer and 3/3 acceptance runs.

## LS06-2 `ls06-eno1-significance-audit`

- Same capsule and cited DOI as LS06-1.
- `bix-37-q3`: native ideal `0.226`; native `eval_mode=str_verifier`; distractors include raw p `0.031`.
- Independently reproducible from the unique ENO1 row: `p.value=0.031`, `adj.Pval=0.226`. At the task-card FDR threshold 0.05, ENO1 is not significant.
- Native standard checks only the adjusted p-value. FDR threshold, boolean decision, source traceability, JSON/report/script are local extensions. The 0.05 threshold is supplied by the local prompt rather than inferred from hidden gold.
- Proposed extension: adjusted p 40; threshold-calibrated non-significant decision 15; report agreement 5.
- Status: **ready for oracle calibration**, subject to independent reviewer and 3/3 acceptance runs.

## LS10-1 `ls10-neun-power-analysis`

- Capsule: `8c64b1fa-fdcc-41e2-be8d-2f0c8d5faaa1`; archive `CapsuleFolder-8c64b1fa-fdcc-41e2-be8d-2f0c8d5faaa1.zip`; papers listed by BixBench: <https://zenodo.org/records/8036465> and <https://www.science.org/doi/10.1126/sciadv.adf4950>.
- `bix-19-q1`: native ideal `337`; native `eval_mode=str_verifier`.
- `bix-19-q2`: native ideal range `(0.215,0.217)`; native `eval_mode=range_verifier`.
- Related `bix-19-q5`: native ideal text `337 samples`; `eval_mode=llm_verifier`.
- Independently reproducible from `NeuN_quantification.csv`: KD mean `214.5`, CTRL mean `210.625`, sample SDs `10.9414023651` and `22.8531804601`, pooled SD `17.9162236933`, KD-minus-CTRL Cohen d `0.2162844172`.
- The JSONL states two-sample t-test, power 0.80 and alpha 0.05, but does not publish the power solver/package/version or reference code. Thus 337 is retained as benchmark-native gold; exact solver equivalence is not asserted beyond that value.
- Proposed extension: means 8, SDs 8, pooled SD 6, d 8, n/group 10; supplied alpha/power/two-sided/ceiling decision 15; report agreement 5.
- Status: **ready for oracle calibration with limitation**: reproduce 337 against at least one pinned solver before final acceptance; document solver/version.

## LS10-2 `ls10-treatment-response-model`

- Capsule: `93f63fb8-b56c-4ad1-8d3b-d651e2107423`; archive `CapsuleFolder-93f63fb8-b56c-4ad1-8d3b-d651e2107423.zip`; BixBench paper field is empty.
- `bix-51-q3`: native ideal range `(0.0024,0.0026)` for age p-value; `eval_mode=range_verifier`.
- `bix-51-q4`: native ideal range `(-0.085,-0.075)` for age log-odds coefficient; `eval_mode=range_verifier`.
- Independently refit from the frozen workbook using 80 complete outcome rows, PR=1, predictors BMI + age + male indicator (female reference), standard unpenalized binomial-logit MLE: age estimate `-0.0795084690`, SE `0.0262977303`, two-sided Wald p `0.0024995441`, OR `0.9235701982`. The native q3/q4 ranges confirm the estimate and p-value.
- Benchmark does not specify software/version, convergence settings, complete-case statement, outcome coding, gender reference, SE, OR, CSV/JSON schema, report, or script. The local prompt supplies complete cases and coding documentation; female reference and the exact SE/OR are proposed extensions derived from the fit, not native benchmark gold.
- Proposed extension: estimate 10, SE 10, p 10, OR 10; negative/significant age direction 15; report agreement 5. Before main evaluation, independently reproduce with a pinned R `glm` or statsmodels release.
- Status: **ready for oracle calibration with limitation**: independent software reproduction and reviewer approval remain required.

## Missing items and go/no-go

| Task | Native gold | Input recomputation | Immediate status | Still required |
|---|---|---|---|---|
| LS06 effect | q1/q4 | complete | calibration-ready | 3/3 acceptance; second reviewer |
| LS06 significance | q3 | complete | calibration-ready | 3/3 acceptance; second reviewer |
| LS10 power | q1/q2/q5 | d complete; n native gold | conditional | pin/reproduce power solver; acceptance/review |
| LS10 logistic | q3/q4 | complete independent fit | conditional | reproduce in second pinned package; acceptance/review |

The BixBench repository provides no verifier source or submitted-analysis reference implementation for these rows. Therefore a claim that the local oracle is the original BixBench grader would be false; it is an auditable extension grounded in native gold and frozen input data.
