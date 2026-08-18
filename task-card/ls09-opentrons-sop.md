# Task card: `ls09-opentrons-sop`

> Canonical participant-facing card generated from `docs/ls06-ls10-task-cards-v2.md`. The packaged-input inventory below is generated from the frozen task directory. Only the Prompt is pasted into a run; evaluator-only answers and outputs are never exposed.

## `ls09-opentrons-sop`

### Inputs (authoritative packaged inventory)
- `inputs/README.md` — 1,699 bytes
- `inputs/instrument.csv` — 123 bytes
- `inputs/labware.csv` — 329 bytes
- `inputs/reagent_map.csv` — 200 bytes
- `inputs/sample_map.csv` — 274 bytes
- `inputs/simulator_contract.json` — 1,108 bytes
- `inputs/sop.md` — 1,481 bytes

**Total:** 5,214 bytes (0.00 MiB).

### Prompt

> Read every file under `inputs/`. Translate the frozen 24-sample magnetic-bead cleanup SOP into an auditable OT-2 Opentrons protocol. Use no external data and do not alter inputs. Write `output/protocol.py`, `output/transfer_plan.csv` with exactly the columns `step,source,destination,volume_uL,pipette,tip_policy`, `output/simulation.txt`, and `output/report.md`. `transfer_plan.csv` is a net liquid-transfer stage table, not a command log: write exactly one row per SOP net-transfer stage per sample (`lysis`, `beads`, `supernatant`, `wash1_add`, `wash1_remove`, `wash2_add`, `wash2_remove`, `elution`), for 8 × 24 = 192 rows. Do not add one row per mix stroke, aspirate command, dispense command, delay, magnet action, or tip action; represent those operations in `protocol.py` and summarize them in `report.md`. Identify each row as `<stage>:<well>` and use the frozen role/well identifiers. Respect the declared deck, Magnetic Module compatibility, API level, pipette range, well capacity, reagent dead volumes, liquid balance, and tip policy. Run the evaluator-pinned simulator using the supplied invocation and record its unedited outcome in `simulation.txt`; if that simulator or invocation is unavailable, record the failure and abort rather than claiming success.
- Deliverables: static Opentrons protocol; 192-row net-transfer plan; verbatim simulator record; report. All wells/volumes/pipettes/tip policies must be explicit.
- Hard gates: exact net-transfer contract and liquid balance; valid deck/labware/wells/pipette range and contamination-safe tip policy; static protocol contract; pinned simulation success.
- Deterministic 80: coverage/schema 10; transfer contract, balance, pipette and tip policy 40; protocol/simulation decision 15; report consistency 5; static protocol plus isolated pinned simulation 10.
- Ablation expectation: `[protocol-planning]`, `[liquid-handling]`, `[labware-validation]`, `[simulation]`; expected to reduce unsafe tips, invalid volumes, deck and false-success errors.
- Readiness closure: the reference protocol completed three real Opentrons 7.1.0 simulations and wrong/empty/legacy-tip controls fail; both C0 and T1 receive the same pre-provisioned simulator. The macOS-arm64 versus production Linux-x86_64 platform difference is retained as a disclosed campaign deviation.
