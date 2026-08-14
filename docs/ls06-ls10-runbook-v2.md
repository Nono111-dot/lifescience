# LS06–LS10 evaluation runbook v2

Controlling source: Feishu evaluation workflow revision 138, especially §§1, 3.1, 4, 5 and 7. This runbook covers 10 tasks only: LS06, LS07, LS08, LS09 and LS10, two tasks each.

## Task-card completeness gate (§3.1)

No task may run until one page contains all of the following:

1. `ID`: globally unique, stable, directory-safe.
2. `Domain`: exactly `life_science`.
3. `Sub-domain`: one primary value from §3.2.
4. `Level / time`: L1 15–20, L2 30–45 or L3 60–90 minutes, based on workflow complexity.
5. `Anchor / related`: exactly one anchor and 2–5 related capability codes from D/P/T/A/X/V/R/I/O/G.
6. `来源思想`: borrowed workflow/rubric/verifier idea, not a copied question.
7. `Inputs`: role, key fields, provenance/license, approximate size and known decoy/stale files.
8. `Prompt`: one-paste target, input locations, scientific constraints and complete output contract; no gold steps or recommended library.
9. `Deliverables`: fixed paths, formats, schemas, units, missing-value policy and rerun requirement; at most 5–6 formal artifacts.
10. `Hard gates`: 2–4 silent scientific failures, never a required library/MCP or visual polish.
11. `DeterministicArtifactScore`: criteria, points, pass conditions, tolerances and Python/manual check method, total 80.
12. `JudgeScore`: Evidence, Method, Restraint and Readability, each 0/3/5.
13. `Ablation`: generic skill/MCP placeholders and the error class they are expected to reduce; no task ID, filename, gold value or answer.

## Experiment arms

- C0: Codex native, no added domain skill/MCP.
- T0: 端砚 bare.
- T1: T0 plus corresponding domain skill environment. The agent autonomously selects, installs and may combine entries from the approved 222 catalog; the operator provides no routing hint.
- T2: T1 plus corresponding approved local scientific MCP environment. MCPs expose generic typed operations, never a task-solving endpoint.

T0 and T1 must have access to the same scientific information available in original inputs. If an MCP uniquely owns required reference data, the result is availability comparison, not MCP uplift.

## Before every independent run

1. Verify the previous run has `reset_status=clean` or this is the first run on a freshly established baseline.
2. Create a new one-use workspace; copy only this task's inputs and create empty `output/`.
3. Create a new client conversation and attach only the new workspace.
4. Export installed/enabled domain capability inventory to `capability_before.json`; compute its SHA-256.
5. Confirm condition: C0/T0 have no added domain capability; T1/T2 expose only the approved catalog environment.
6. Record client/model exactly as shown; unknown values are `N/A`, never guessed.
7. Paste the Prompt once and start wall-clock timing.

## During the run

The operator handles only uniform file/command permission dialogs. No scientific help, error diagnosis, extra prompt, capability recommendation or installation hint is allowed. Capability discovery, installation, selection and invocation are agent behavior. Log capability name, catalog match, install/call time and result automatically where possible.

## Stop, freeze and score

1. Stop at completion or time limit and revoke client write access.
2. Record `completed`, `timeout`, `crash` or `operator_abort`, plus intervention facts.
3. Hash and freeze the workspace. A normal UI end with missing artifacts is harness failure.
4. Run the independent static oracle/manual checklist. Never import or execute untrusted submission code in the grader.
5. Clean-rerun generated scripts only in an isolated workspace copy/container.
6. Blind-judge report artifacts without harness/condition metadata.

## Mandatory capability reset after every run

This happens after evidence capture and before the next task **or next trial**.

1. Export `capability_after_run.json` before removal so the just-finished run remains auditable.
2. Uninstall or disable every skill installed during the run.
3. Remove/disable every MCP connection enabled during the run; terminate its task-scoped process/session.
4. Close the conversation, detach the frozen workspace and clear task-scoped capability routing/cache/state supported by the client.
5. Do not delete the approved catalog itself or account-wide credentials; restore the experiment baseline, not a factory reset.
6. Export `capability_after_reset.json` and compare its normalized inventory with `capability_baseline.json`.
7. Verify no prior task ID, workspace path, skill installation, MCP session or task-specific memory is visible to a fresh conversation.
8. Set `reset_status=clean` only when the inventory diff is empty and the smoke check passes.

If removal fails, stop. Record `reset_status=failed`, preserve the diff and do not run the next task. Use a fresh client profile/container only if that recovery method was predeclared for all comparable runs.

## Minimal per-run evidence

- workflow revision and task-card version/hash;
- task_id, harness, condition, client/model, trial and wall_min;
- run_status, hardgate_pass, deterministic_score, judge_score and intervention/notes;
- workspace/input/frozen-output hashes;
- capability baseline, before, installed/invoked, after-run and after-reset inventories;
- reset status/diff and next-run release decision.

## Current ten tasks

| Task | Primary sub-domain | Proposed level/time | Anchor / related |
|---|---|---|---|
| ls06-eno1-effect-size | proteomics_and_metabolomics | L2 / 35 min | X / D,A,V,O,G |
| ls06-eno1-significance-audit | proteomics_and_metabolomics | L2 / 30 min | A / D,X,V,I,O |
| ls07-combination-treatment-deg | transcriptomics | L3 / 75 min | X / D,P,T,A,G |
| ls07-combination-treatment-mechanism | systems_and_synthetic_biology | L3 / 90 min | I / T,A,X,V,G |
| ls08-multiome-column-match | single_cell_and_spatial | L3 / 75 min | X / D,P,A,V,G |
| ls08-enhancer-promoter-integration | epigenomics_and_regulation | L2 / 45 min | I / D,A,X,V,O |
| ls09-opentrons-sop | systems_and_synthetic_biology | L2 / 45 min | P / T,A,V,O,G |
| ls09-plate-dilution-recovery | systems_and_synthetic_biology | L2 / 40 min | R / D,P,A,X,V |
| ls10-neun-power-analysis | biomedical_and_clinical_bioinformatics | L2 / 40 min | X / D,A,V,I,G |
| ls10-treatment-response-model | biomedical_and_clinical_bioinformatics | L2 / 45 min | X / D,A,V,I,G |

Each row still requires the full task card; this table is routing and coverage metadata only.
