# Formal-run preflight checklist

## Task acceptance

- [ ] Card version and Prompt hash frozen
- [ ] Input provenance/license and SHA-256 verified
- [ ] `docs/inputs/SHA256SUMS.tsv` covers every copied input file, including README/resource/environment manifests, with current byte size and hash
- [ ] No gold/oracle/judge notes in workspace
- [ ] Scientific reviewer approved target and expected behavior
- [ ] Reference output passes 3/3
- [ ] Empty output fails 3/3
- [ ] Format-correct scientific error fails 3/3
- [ ] Static oracle cannot execute submission code
- [ ] Isolated clean-rerun environment pinned (if required)
- [ ] Any required scientific simulator/reference environment is provisioned before timing, matches its exact lock, and passes the task-specific smoke check in every scheduled harness
- [ ] Independent-review sign-off is recorded, or the missing-review deviation is disclosed before delivery

## Harness/condition

- [ ] Fresh conversation and one-use workspace
- [ ] Client/model/build and hardware recorded
- [ ] Network policy frozen
- [ ] C0/T1 condition assigned from the frozen 50-row queue before opening the task
- [ ] C0 receives no added life-science Agent Skill; T1 receives only the task's predeclared rows from `docs/task-skill-plan-codex-t1-v1.tsv`
- [ ] All unselected life-science skills and all MCP/SCP capabilities are disabled
- [ ] Every selected skill matches `docs/capability-runtime-mapping-v1.tsv` by repository, commit, path and `SKILL.md` SHA-256
- [ ] Install, exposure, actual invocation, failure and post-run removal/reset evidence will be captured separately
- [ ] Permission policy and timer checked

## Previous-run reset gate

- [ ] Previous run's installed/invoked capability trace preserved
- [ ] All skills installed by the previous run uninstalled/disabled
- [ ] All MCPs enabled by the previous run removed/disabled and sessions terminated
- [ ] Previous conversation closed and workspace detached/frozen
- [ ] Post-reset normalized inventory equals the experiment baseline
- [ ] Fresh-conversation smoke check shows no previous task state
- [ ] `reset_status=clean`; otherwise the next run is blocked

## Freeze/score

- [ ] Write access closed at stop
- [ ] Status classified including timeout/crash/no-artifact/intervention
- [ ] Frozen workspace manifest and hash saved
- [ ] Oracle run against frozen copy
- [ ] Blind bundle removes harness metadata
- [ ] Judge form complete
- [ ] Raw and capped totals both retained
