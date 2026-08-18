# Task card: `ls08-enhancer-promoter-integration`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls08-enhancer-promoter-integration`

### Inputs (authoritative packaged inventory)
- `inputs/INTEGRATION_RULE.md` — 1,011 bytes
- `inputs/README.md` — 1,131 bytes
- `inputs/ep.interactions.q1.expr.csv` — 3,792 bytes
- `inputs/ep.interactions.q1.hic.csv` — 6,388 bytes

**Total:** 12,322 bytes (0.01 MiB).

- Prompt: **Integrate the supplied Hi-C and CRISPR-expression evidence for all candidate enhancer-promoter pairs and identify the least supported causal pair. Write `output/pair_evidence.csv` with `pair_id,contact_evidence,perturbation_effect,combined_support,rank`, `output/least_supported.json`, `output/analysis.py`, and `output/report.md`. Treat physical contact and perturbation evidence as distinct.**
- Deliverables: every candidate pair exactly once, unique ranks, one least-supported call, report and rerunnable script; units/scales and tie policy stated.
- Hard gates: modalities joined by the true pair key; all candidates covered once; least-supported call equals minimum combined support under the frozen rule; contact is not described as perturbational proof.
- Deterministic 80: coverage/schema 10; modality values, combined score and ranking 40; least-supported decision 15; report consistency 5; static/rerunnable script 10.
- Ablation expectation: `[regulatory-integration]`, `[causal-evidence-audit]`, `[tabular-analysis]`, `[reproducible-code]`; expected to reduce bad joins, scale mixing and causal overclaim.
- Readiness closure: background distance regression, robust residual z-score, guide aggregation, physical-evidence threshold and ranking/tie rule are frozen and independently recomputed by the checker.
