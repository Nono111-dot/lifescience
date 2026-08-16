# 25-task C0/T1 formal evaluation protocol v2

Status: **preflight only; no formal run is released until every gate below is closed**.

This protocol is the campaign-specific supplement requested for all 25 repository tasks. It narrows the experiment to one matched trial per task in two conditions, `C0` and `T1` (50 runs total). It does not retroactively convert a blocked or calibration result into formal evidence. Where this supplement is silent, `evaluation-protocol-v1.md` and the controlling evaluation guide apply.

## Comparison and interpretation

| Condition | Client | Scientific capability policy |
|---|---|---|
| `C0` | Codex | Native client only. No added life-science skill, MCP/SCP or task-specific scientific package. |
| `T1` | Codex | Same Codex client/model/build as C0, with task-appropriate **Agent Skills** selected from the approved `life_science_agent_skills.xlsx` catalogue and installed from its fixed GitHub commit/path. MCP/SCP entries are excluded from this campaign. |

The primary contrast is a matched Codex capability ablation. Client, model/build, machine class, prompt, inputs and network policy are identical; only the predeclared task-specific Agent Skill installation differs. Subject to successful reset and order control, the paired difference may be reported as Codex skill uplift.

## Frozen scope

- 25 stable task IDs from `docs/input-problem-inventory-v1.tsv`.
- One trial in each condition: 25 `C0` + 25 `T1` = 50 independent runs.
- Randomization seed: `20260816`; the immutable execution order is stored in the local campaign `audit/run_matrix.tsv`.
- Run outputs, screenshots, logs, frozen workspaces, grader output and judge forms remain local and are not committed to GitHub.
- GitHub contains task definitions, input/provenance manifests, accepted static graders, environment contracts and release status only.

## Fail-closed release gates

A task-condition pair may be marked `formal_released` only when all of the following are true:

1. The task card contains all 13 fields required by §3.1 and its prompt hash is frozen.
2. Every input byte is present, its SHA-256 matches `docs/inputs/SHA256SUMS.tsv`, and provenance/license are recorded.
3. No gold, expected answer, reference submission or oracle-only fixture is copied into the agent workspace.
4. A static deterministic grader is independently accepted: correct/empty/wrong controls pass in three clean repetitions, and submission code is not imported or executed by the grader.
5. Any clean rerun occurs in an isolated, pinned environment and is recorded separately from static grading.
6. Prompt/deliverable, scientific validity and answer-leak review are signed off by reviewers independent of the run operator.
7. The exact Codex client/model/build, machine class, network policy, time source and permission policy are frozen identically across C0 and T1.
8. Every predeclared T1 skill has a fixed GitHub repository, commit, directory path and expected `SKILL.md` SHA-256; selected entries pass install/load/uninstall smoke tests before their first formal use.
9. The post-reset inventory equals the campaign baseline and a fresh conversation exposes no prior task state.
10. Blind judges are assigned and cannot see client, condition, installed skills, deterministic score or gold data.

Unreleased attempts may be retained as `calibration` or `preflight_diagnostic`, but never entered in the formal denominator or score table.

## Environment reset before every run

1. Confirm the previous run has a clean reset attestation; otherwise stop.
2. Close the prior conversation and detach its workspace.
3. Remove every skill installed by the prior run and clear task-scoped routing/cache/state supported by the client.
4. Export the normalized capability inventory and compare it byte-for-byte with the campaign baseline.
5. Create a new one-use workspace; copy only the current task's public inputs and create an empty `output/`.
6. Recompute the input manifest and record client/model/build, machine, network and wall-clock source.
7. For `C0`, verify zero added domain capabilities. For `T1`, install only the task's predeclared catalogue rows into the isolated Codex profile, then start a fresh Codex task so the installed skills are loaded.

The run cannot start if the inventory differs, any old task ID/path is visible, or a prior capability remains enabled.

## T1 selection and installation record

The Excel workbook's `真实说明书索引` sheet is the selection and source authority. Skill choice is made before seeing a run's outputs or gold data, based only on the frozen task card and catalogue metadata, and is recorded in the task-to-skill plan. For every attempted, installed, loaded or invoked skill, record:

- workbook item ID and exact display name;
- Codex install name, GitHub repository, fixed commit and directory path;
- expected and installed `SKILL.md` SHA-256 plus catalogue-match result;
- discovery, install, invoke and uninstall timestamps;
- result/failure code and evidence-log path;
- post-reset inventory diff.

The run operator must not change the predeclared selection after seeing outputs, provide scientific hints or substitute an unlisted package. If the fixed source cannot be installed or loaded, record `capability_unavailable`; do not improvise another repository or branch.

The 146 Agent Skill rows are normalized in `docs/capability-runtime-mapping-v1.tsv`. All fixed `SKILL.md` sources and hashes have been verified, but 122 explicitly require MCP/SCP or an API key and are not eligible for strict skill-only T1. The task plan may select only the remaining direct candidates; installation success is not the same as a successful Codex load/invoke/reset.

## Run, freeze and score

1. Paste the frozen Prompt exactly once and start the monotonic timer.
2. Only uniform predeclared permission handling is allowed; record every intervention.
3. Stop at completion or the card limit; classify status without repairing artifacts.
4. Revoke write access, hash the entire workspace and copy it to the immutable local `frozen/` area.
5. Run the accepted static oracle, then any isolated clean-rerun check.
6. Score `DeterministicArtifactScore` from the repository's authoritative 80-point task rubric.
7. Blind-score Evidence, Method, Restraint and Readability at 0/3/5 each (20 points).
8. `StrictSuccess=true` only when every hard gate passes and raw total is at least 80. A hard-gate failure caps the displayed total at 49 while preserving raw component scores.
9. Complete reset and inventory comparison before releasing the next row of the queue.

## Evidence scoring precision

Blind Evidence is scored from visible report citations and traceability only:

- `0`: no task-specific evidence; fabricated/untraceable support; or the report contradicts required machine-readable artifacts.
- `3`: at least one traceable task-specific input/result supports the main claim, but coverage, linkage or uncertainty is incomplete.
- `5`: every main claim is linked to the relevant input/result artifact, the report identifies the decisive measurements or rows, and limitations/uncertainty are tied to the evidence without unsupported extrapolation.

Judges record claim count, supported-claim count, evidence locations and a short rationale. Evidence points cannot repair a deterministic hard-gate failure.

## Required local and Feishu records

The local campaign stores immutable per-run workspaces, hashes, status, capability traces, oracle JSON, judge forms and deviations. Feishu receives native tables for:

1. task-level and condition-level score statistics with denominators and exclusions;
2. the complete 50-row evaluation log, including unreleased/invalid attempts;
3. capability installation/reset evidence and issue/deviation summaries.

No row receives a score until execution evidence exists. Missing prerequisites remain explicit blockers, not zero scores.
