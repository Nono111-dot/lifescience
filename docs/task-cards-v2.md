# Life-science evaluation task cards v2 — 25-task index

This is the campaign entry point for the 25 frozen task IDs. It combines:

- `docs/task-cards/ls01-ls05-v2.md` — 15 normalized §3.1 cards;
- `docs/ls06-ls10-task-cards-v2.md` — 10 detailed §3.1 cards.

The paste-once Prompt inside each card is the only task instruction given to an evaluated agent. Gold data, expected outputs, oracle internals, reviewer notes and scoring results remain outside the run workspace.

## Controlling contracts

- Readiness/blockers: `docs/input-problem-inventory-v1.tsv`.
- Input bytes: `docs/inputs/SHA256SUMS.tsv` and per-directory provenance notes.
- Deterministic score: `docs/deterministic-rubrics-v2.tsv` (10/40/15/5/10 = 80).
- C0/T1 campaign: `docs/evaluation-protocol-c0-t1-v2.md`.
- Release decision: `docs/formal-eval-release-status-2026-08-16.md`.

Structural completeness is not scientific acceptance. A card remains blocked until its declared reference, oracle, acceptance controls, reviewers, target-client runtime and environment-reset gates are all closed.

## Current denominator

The requested queue contains 25 tasks and 50 planned runs. All 69 agent-visible input files pass the corrected byte manifest, but only 7/25 scientific oracles are accepted and no T1 runtime package has completed target-client smoke testing. The formal denominator is therefore currently zero. Attempts made before release must be labelled calibration or diagnostic and excluded from headline scores.
