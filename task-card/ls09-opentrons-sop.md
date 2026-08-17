# Task card: `ls09-opentrons-sop`

> Canonical individual task card materialized from `docs/ls06-ls10-task-cards-v2.md`. The Prompt is the only instruction pasted into an evaluated run; oracle-only answers and evaluation outputs are never exposed to the agent.

## `ls09-opentrons-sop`

- Inputs: `sop.md`, `instrument.csv`, `labware.csv`, `reagent_map.csv`, `sample_map.csv`, and `simulator_contract.json`. They pin robot/API, pipette, deck slots, labware, wells, source volumes, 24 samples, Opentrons package 7.1.0, Protocol API 2.16, invocation, capture policy, and failure behavior. Provenance and scientific basis are in `docs/research/ls09-local-extension-provenance.md`; no answer-bearing decoy.
- Prompt: **Translate the supplied SOP into an auditable Opentrons protocol plan. The transfer plan represents exactly eight net liquid-transfer stages per sample; do not list individual mix strokes or low-level aspirate/dispense movements as extra rows. Write `output/protocol.py`, `output/transfer_plan.csv` with `step,source,destination,volume_uL,pipette,tip_policy`, `output/simulation.txt`, and `output/report.md`. Respect labware, deck, pipette, volume and contamination constraints. Run the supplied pinned simulator; if it is unavailable or fails, record the exact error and mark the protocol not execution-ready rather than claiming success.**
- Deliverables: static Opentrons protocol; 192-row net-transfer plan; verbatim simulator record; report. All wells/volumes/pipettes/tip policies must be explicit.
- Hard gates: exact net-transfer contract and liquid balance; valid deck/labware/wells/pipette range and contamination-safe tip policy; static protocol contract; pinned simulation success.
- Deterministic 80: coverage/schema 10; transfer contract, balance, pipette and tip policy 40; protocol/simulation decision 15; report consistency 5; static protocol plus isolated pinned simulation 10.
- Ablation expectation: `[protocol-planning]`, `[liquid-handling]`, `[labware-validation]`, `[simulation]`; expected to reduce unsafe tips, invalid volumes, deck and false-success errors.
- Readiness closure: the reference protocol completed three real Opentrons 7.1.0 simulations and wrong/empty/legacy-tip controls fail; both C0 and T1 receive the same pre-provisioned simulator. The macOS-arm64 versus production Linux-x86_64 platform difference is retained as a disclosed campaign deviation.
