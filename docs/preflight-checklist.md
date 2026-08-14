# Formal-run preflight checklist

## Task acceptance

- [ ] Card version and Prompt hash frozen
- [ ] Input provenance/license and SHA-256 verified
- [ ] No gold/oracle/judge notes in workspace
- [ ] Scientific reviewer approved target and expected behavior
- [ ] Reference output passes 3/3
- [ ] Empty output fails 3/3
- [ ] Format-correct scientific error fails 3/3
- [ ] Static oracle cannot execute submission code
- [ ] Isolated clean-rerun environment pinned (if required)
- [ ] Second operator completes within 1.5× limit

## Harness/condition

- [ ] Fresh conversation and one-use workspace
- [ ] Client/model/build and hardware recorded
- [ ] Network policy frozen
- [ ] C0/T0/T1/T2 assigned before opening task
- [ ] Exact enabled capability copied from allowlist
- [ ] All other life-science skills/MCPs disabled
- [ ] Exact capability runtime smoke test passed
- [ ] Permission policy and timer checked

## Freeze/score

- [ ] Write access closed at stop
- [ ] Status classified including timeout/crash/no-artifact/intervention
- [ ] Frozen workspace manifest and hash saved
- [ ] Oracle run against frozen copy
- [ ] Blind bundle removes harness metadata
- [ ] Judge form complete
- [ ] Raw and capped totals both retained
