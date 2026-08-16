# Formal C0/T1 release status — 2026-08-16

Requested campaign: 25 tasks × (`C0`, `T1`) × 1 trial = 50 runs.

Current status: **NO-GO / preflight preparation**.

## Verified snapshot

- Scope/queue: 25 unique tasks, 50 paired rows, exactly one `C0` and one `T1` row per task.
- Inputs: 69/69 agent-visible files materialized and SHA-256 verified after correcting six manifest rows that had recorded Windows CRLF bytes rather than the repository's canonical LF blobs and adding two omitted LS05 `SCORING_RULE.md` rows. `.gitattributes` now prevents line-ending conversion under `docs/inputs/**`.
- Accepted scientific oracles: 7/25. LS05 model ranking/pocket, LS06 effect/significance, LS09 dilution recovery and both LS10 tasks pass their existing regression/acceptance controls. The remaining 18 are fail-closed.
- T1 catalogue: 146/146 Agent Skill rows normalized; 0/146 have verified 端砚 runtime mapping or install/invoke/uninstall smoke evidence.

## Blocking gates

- Several pinned scientific references remain absent or unaccepted even though all currently tracked input bytes now pass the repository manifest; see `input-problem-inventory-v1.tsv`.
- Most tasks do not yet have independently accepted static oracles and positive/empty/wrong controls passing 3/3.
- `ls05-protein-shape` is calibration-only and cannot enter the primary aggregate without an approved replacement or explicit protocol deviation.
- The supplied 222-row capability workbook is a discovery catalogue, but Agent Skill rows do not provide canonical 端砚 package IDs, versions or install sources.
- Exact 端砚 client/model/build access and capability inventory have not yet been captured.
- Independent scientific/leak reviewers and blind judges are not yet assigned in repository evidence.

## Work that is allowed before release

- materialize and hash all tracked inputs;
- repair or replace scientifically defective fixtures with provenance and reviewer sign-off;
- complete §3.1 task cards;
- implement static fail-closed graders and acceptance controls;
- map workbook entries to target-client runtime packages and run install/invoke/uninstall smoke tests;
- create local workspaces, run queue and empty audit tables.

## Work that is not yet a formal result

Any model attempt before the applicable gates close is labelled `preflight_diagnostic` or `calibration`. It is excluded from formal denominators, paired comparisons and headline scores.

## Capability mapping evidence

`docs/capability-runtime-mapping-v1.tsv` contains the 146 Agent Skill catalogue rows allowed for T1. All runtime IDs, versions, install sources and install/invoke/uninstall smoke states remain unresolved pending an actual 端砚 export. The 76 MCP rows are intentionally excluded because this campaign is T1, not T2.
