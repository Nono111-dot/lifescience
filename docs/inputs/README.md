# Input index

Task inputs are read-only fixtures. Copy the contents of exactly one task directory into a fresh workspace's `inputs/` directory. Never edit the repository copy during a run.

| Task ID | Files | License/provenance | Notes |
| --- | --- | --- | --- |
| `life-l2-paired-expression` | `paired_expression.csv` | CC0-1.0 synthetic fixture created for this repository | Expression values are arbitrary normalized units; they are not patient data. |

## Adding an input set

Each `docs/inputs/<task-id>/` directory must include a README stating provenance, redistribution terms, schema, units, missing-value representation, and integrity information. Do not include secrets, personal data, controlled clinical data, or files whose license prohibits redistribution.

