# AI4S Desktop UI Taskbook v0.1

## Purpose

This taskbook defines reproducible desktop UI tasks. Each task has redistributable, read-only inputs and an independent deterministic oracle. The deterministic oracle contributes 0–80 points; a blind visual judge contributes 0–20 points.

## Standard operating procedure

1. Create a one-use workspace.
2. Copy one task's input directory to `workspace/inputs/` without modifying the source copy.
3. Create an empty `workspace/output/` directory.
4. Open the workspace in the desktop client and paste the task prompt once.
5. Freeze the workspace when the run ends.
6. Run the matching oracle with `--workspace /path/to/workspace`.
7. Preserve the oracle JSON and the frozen workspace for review.

## Task card: `life-l2-paired-expression`

- **domain:** life_sciences
- **sub_domain:** transcriptomics / paired expression
- **level:** L2
- **input:** `docs/inputs/life-l2-paired-expression/`
- **oracle:** `docs/oracles/life-l2-paired-expression/oracle.py`

### Prompt

Build a desktop UI for reviewing paired gene-expression measurements. Read `inputs/paired_expression.csv`; do not fetch external data or modify the input file.

The UI must:

1. show the subject pairs and pre/post expression values;
2. display a paired plot in which each subject's pre and post points are visibly connected;
3. show the mean paired change and the number of complete pairs;
4. allow a user to export the required artifacts to `output/`;
5. clearly label expression units and the direction of change.

For each row compute `paired_change = post_expression - pre_expression`. Positive values are `up`, negative values are `down`, and zero is `unchanged`. Do not replace paired analysis with a comparison of unpaired group means.

### Deliverables

Write all deliverables under `workspace/output/`:

- `paired_expression_results.csv` with columns `subject_id`, `pre_expression`, `post_expression`, `paired_change`, and `direction`;
- `summary.json` with `task_id`, `pair_count`, `mean_paired_change`, `up_count`, `down_count`, and `unchanged_count`;
- `paired_expression.png`, a non-empty PNG export of the paired plot.

### Hard gates

- all three deliverables exist under `output/`;
- output rows match the input subjects exactly, without duplicates;
- numeric results are finite and agree with the paired calculations within `1e-6`;
- directions and summary counts are scientifically consistent with the row-level changes;
- the chart is a valid, non-empty PNG file;
- the evaluator can parse the CSV and JSON without external services.

### Deterministic rubric (80 points)

| Criterion | Points |
| --- | ---: |
| Required files and parseable formats | 10 |
| Subject identity and complete pairing | 15 |
| Pre/post values preserved | 10 |
| Paired changes correct | 20 |
| Direction labels correct | 10 |
| Summary statistics and counts correct | 10 |
| Non-empty PNG export | 5 |

### Blind visual rubric (20 points)

- paired relationships are immediately legible: 6;
- labels, units, and direction are clear: 5;
- hierarchy and spacing support rapid review: 4;
- table and plot agree visually: 3;
- export affordance and status feedback are clear: 2.

## Contribution checklist

- [ ] Task card contains `domain`, `sub_domain`, Prompt, deliverables, hard gates, and rubric.
- [ ] Inputs are redistributable and live under `docs/inputs/<task-id>/`.
- [ ] Oracle is independent, deterministic, and accepts `--workspace`.
- [ ] Oracle emits `deterministic_score`, `criteria`, `hardgate_pass`, and `failure_codes`.
- [ ] Tests cover a correct answer, empty output, and at least one format-correct but scientifically wrong answer.

