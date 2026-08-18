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
- Release decision: `docs/formal-eval-release-status-2026-08-17.md`.

Structural completeness and scientific acceptance are audited separately. Current release status, deviations and capability-use limitations are authoritative in `docs/formal-eval-release-status-2026-08-17.md`.

## Current denominator

The frozen queue contains 25 tasks and 50 Codex runs. The canonical input manifest covers the 25 task directories, all 25 scientific oracles are accepted, and all 18 selected Agent Skills have pinned source/hash plus install and clean-reset evidence. Six exposed skills were not opened by the evaluated agent; this limitation is recorded in the release status and must not be reported as skill use.
