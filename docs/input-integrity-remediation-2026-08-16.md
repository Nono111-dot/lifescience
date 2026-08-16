# 25-task input integrity remediation — 2026-08-16

All agent-visible files under `docs/inputs/` were materialized from commit `ec1a6802ad23b4186b3b18da56cfa3c795922680` and independently hashed. Final result: **69/69 present; 69/69 SHA-256 match**.

## Corrected cross-platform manifest defect

Six manifest rows described Windows CRLF worktree bytes, while the canonical Git blobs use LF. The byte deltas exactly equalled the line counts, and replacing each LF with CRLF reproduced every old manifest hash. No scientific value or record changed.

Corrected rows:

- `life-l2-paired-expression/paired_expression.csv` and `README.md`;
- `ls07-combination-treatment-deg/counts_raw_unfiltered.csv` and `sample_layout.csv`;
- `ls07-combination-treatment-mechanism/counts_raw_unfiltered.csv` and `sample_layout.csv`.

`docs/inputs/SHA256SUMS.tsv` now records the canonical LF blob size/hash. Repository `.gitattributes` sets `docs/inputs/** -text` so Git does not silently transform line endings on checkout.

The audit also found two agent-visible LS05 rule files that were tracked but absent from the manifest: `ls05-low-confidence-pocket/SCORING_RULE.md` and `ls05-structure-model-ranking/SCORING_RULE.md`. Both canonical blob hashes are now included, closing manifest coverage at 69/69.

## Boundary

Byte integrity does not resolve scientific reference or oracle acceptance. Tasks marked `needs_reference_and_oracle`, `blocked_oracle_acceptance`, `blocked_environment_acceptance` or `calibration_only` remain blocked exactly as recorded in `docs/input-problem-inventory-v1.tsv`.
