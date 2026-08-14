# `life-l2-paired-expression` input

`paired_expression.csv` is a synthetic CC0-1.0 fixture created for UI evaluation. It contains no human-subject or patient data.

## Schema

| Column | Type | Meaning |
| --- | --- | --- |
| `subject_id` | string | Stable synthetic pair identifier |
| `pre_expression` | float | Baseline normalized expression, arbitrary units |
| `post_expression` | float | Post-condition normalized expression, arbitrary units |

All rows are complete pairs. Missing values would be represented by an empty CSV field, although this fixture contains none. Preserve the row identities and values exactly.

## Integrity

- Row count excluding header: 6
- Expected mean paired change: `0.5`
- Redistribution: CC0-1.0

