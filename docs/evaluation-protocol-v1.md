# 端砚 × Codex life-science evaluation protocol v1

## Evaluation scope

The current experiment covers **LS06–LS10 only: 10 tasks, two tasks per LS group**. LS01–LS05 assets remain candidate-development material and are not scheduled in this evaluation. The controlling workflow is Feishu revision 138; every task card must contain all §3.1 fields before it can enter a run.

## What is being compared

The primary harness comparison is **Codex C0 vs 端砚 T0** on the same frozen task card, input bytes, time limit, machine class, network policy and trial count. Capability uplift is measured separately inside 端砚: **T0 vs T1**, and only where justified, **T1 vs T2**. Do not report C0-vs-T1 as a pure harness effect.

| Condition | Harness | Allowed capability |
|---|---|---|
| C0 | Codex | Native client only; no added life-science skill/MCP |
| T0 | 端砚 | Bare client; no added life-science skill/MCP |
| T1 | 端砚 | Agent autonomously discovers, installs and invokes every skill needed for the task; every installed/invoked skill must match the Feishu revision-717 222-row life-science catalog and the target-client runtime inventory |
| T2 | 端砚 | T1 plus autonomous use of all necessary catalog-listed scientific MCP/API capabilities; every installed/invoked connector must also have a target-client runtime match |

T1/T2 deliberately do **not** cap the number of capabilities. Capability selection is part of the agent behavior being evaluated: the agent should infer what it needs, install it without operator scientific guidance, call it when useful, and stop when sufficient. Any installed, attempted, automatically routed or invoked domain capability outside the exact 222-item catalog is a protocol violation. General filesystem, shell and client-native editing are harness functions, not scientific capability packages; record them but do not treat them as T1/T2. Catalog membership does not prove runtime availability: record canonical package ID, exact display name/version, install/call timestamps, outcome and a preflight smoke-test result. `capability-whitelist-v1.tsv` is only a 22-row previously smoke-tested subset and is not the catalog authority.

## Preflight gates

No main run starts until all are true:

- task state is `ready`, not `needs_oracle`, `blocked_input`, `blocked_reference` or `calibration_only`;
- input hashes match `docs/inputs/SHA256SUMS.tsv`, provenance/license is recorded, and no gold/oracle is inside the run workspace;
- prompt and deliverable contract have passed scientific review and leak review;
- oracle is static and deterministic, does not import/execute the submission, emits criterion scores/failure codes, and has correct/empty/wrong tests passing 3/3;
- any clean-rerun grader uses a separate sandbox/container with pinned dependencies and no access to hidden gold beyond the grader;
- exact client/model/build, OS, CPU/RAM, network policy, capability inventory, time source and screen-recording policy are frozen;
- operator has practiced permissions handling and signs the no-scientific-help rule;
- blind judges are assigned without seeing harness/condition metadata.

## Per-run SOP

1. Copy `docs/inputs/<task-id>/` to a new one-use `workspace/inputs/`; create empty `workspace/output/`.
2. Verify hashes and capture workspace ID. Open it in a fresh client conversation; confirm the assigned condition and disable every non-allowed domain package.
3. Paste the task-card Prompt exactly once and start a monotonic timer.
4. The operator may only answer uniform file/command permission dialogs according to the predeclared permission policy. No scientific hints, corrections, extra steps or prompt restatement.
5. Stop at completion or the card time limit. Revoke/close client write access, capture end time and classify `success`, `timeout`, `crash`, `harness_no_artifact`, `operator_invalid`, or `other_failure`.
6. Hash and freeze the whole workspace. Run the static Python oracle/checklist against the frozen copy, then any isolated clean rerun. Send only designated nondeterministic artifacts to blind judges.
7. Store raw run record, oracle JSON, judge forms, screenshots/logs and frozen-artifact manifest. Never repair outputs before scoring.
8. Before any next task or trial, perform the capability reset in `ls06-ls10-runbook-v2.md`: preserve the just-finished capability trace, uninstall/disable every skill and MCP added by the run, close the conversation, detach the workspace, clear task-scoped capability state, and compare the post-reset inventory with the experiment baseline. A mismatch blocks the next run.

If an operator gives scientific help, mark `operator_invalid` and exclude the run from the primary result while retaining it in the audit log. A normally ending UI with no required artifact is `harness_no_artifact`, not missing data. Failure to restore the capability baseline is `environment_contaminated`; do not start the next run until resolved.

## Experimental design

- Minimum calibration: 3 representative ready tasks × C0/T0 × 1 trial. Calibration is excluded from headline results.
- Main result: the 10 accepted LS06–LS10 cards. Randomize task order within harness; counterbalance harness order; use fresh workspaces, conversations and capability baselines.
- Following workflow §5.2, start with `k=1`: C0 vs T2 on all 10 tasks, and add T0/T1 on predeclared representative L2 tasks. Only hard-gate flips or conclusion-critical runs are repeated twice. For T1/T2, expose the experiment-approved subset of the 222 catalog rather than preselecting a package; the agent autonomously chooses and may install/call multiple relevant capabilities. T2 is used only when local scientific MCP policy is frozen.
- Preserve every failed run. Do not rerun selectively; predeclare retry rules for infrastructure outages.
- Stratify reporting by P0/P1, task, level and capability tag. The calibration-only protein-shape card must not enter the primary scientific aggregate unless replaced by an ecologically valid LS05 card.

Publish the exact run denominator and any predeclared repeats. Do not silently expand to three trials for every arm or task; the default is the lightweight workload in §5.2.

## Scoring and result presentation

- DeterministicArtifactScore: 0–80. Missing core artifact gives 0 deterministic points.
- JudgeScore: four blind dimensions—Evidence, Method, Restraint, Readability—each 0/3/5, total 0–20.
- StrictSuccess: every hard gate passes and raw total ≥80. If any hard gate fails, displayed total is capped at 49, while raw component scores remain in the audit record.
- Primary metrics: StrictSuccess rate with bootstrap 95% CI; paired C0–T0 difference; median wall time among all and successful runs; timeout/crash/no-artifact/operator-invalid rates.
- Secondary metrics: deterministic and judge distributions, failure-code profile, T1 uplift over T0, T2 uplift over T1, and per-task trial variance.
- Present a task-level table, condition-level summary, failure taxonomy and 2–3 representative blinded artifacts. Never collapse invalid runs into failures or drop harness failures.

Required deliverables to the user:

1. frozen task cards and input provenance/hash manifest;
2. exact capability/condition manifest;
3. immutable run records and frozen workspace hashes;
4. oracle JSON and blind-judge forms;
5. aggregate report with denominators, uncertainty, exclusions and limitations;
6. issue log covering crashes, timeouts, permission interventions and deviations.

## Current go/no-go

**No-go for the 25-task main run.** Inputs are downloaded, but 24/25 independent oracles are absent; several references are not pinned; three custom fixtures are scientifically incomplete/inconsistent; and actual 端砚 account/client/capability availability has not been observed. It is valid to prepare workspaces now, but any execution before these gates close is calibration evidence only.
