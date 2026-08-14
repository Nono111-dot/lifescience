# LS09 local-extension provenance and scientific basis

These two tasks are **locally authored evaluation extensions**, not native tasks from BioAgentBench, BixBench, CompBioBench, ABC-Bench, or any other benchmark. Their purpose is to cover LS09 laboratory automation after the three selected public benchmarks were found not to contain equivalent, fully reproducible tasks. The fixture values and expected results are frozen in repository inputs and oracle-side `gold.json`; no hidden biological fact is inferred.

## `ls09-opentrons-sop`

- Opentrons' official Python Protocol API tutorial defines a protocol through an API version and a `run()` function, and demonstrates OT-2 serial-dilution liquid handling with the NEST reservoir, 96-well plate, and 300-uL tip rack: https://docs.opentrons.com/python-api/tutorial/
- Official instrument documentation states that configured volumes must fall within the pipette's supported volume range: https://docs.opentrons.com/python-api/reference/instruments/
- Official module documentation defines loading compatible labware on a Magnetic Module and using `engage()` / `disengage()`: https://sandbox.docs.opentrons.com/edge/python-api/modules/magnetic-module/
- Official labware-definition documentation defines `isMagneticModuleCompatible` and `magneticModuleEngageHeight`: https://sandbox.docs.opentrons.com/edge/ot-2/labware/definitions/

The fixture therefore pins robot, API level, pipette, deck slots, compatible deep-well plate, sample wells, reagent wells, starting volumes, dead volumes, and tips. The contamination-path audit requires six independent tip lifecycles per sample: lysis, beads, supernatant, wash 1, wash 2, and elution. Within a wash only, its fresh addition tip remains attached and may remove liquid from the same sample; it is never returned to reagent. This gives `24 × 6 = 144` tips, so two 96-tip racks are supplied. The earlier 72-tip interpretation was scientifically unsafe and is retained only as a deliberate failing test control. The oracle checks 24 samples, 192 transfer-plan rows, 144 tips, pipette range, peak/final volume, source consumption, and waste balance. It statically checks required protocol constructs because the repository does not ship the Opentrons simulator. A real formal run should additionally execute the frozen `protocol.py` with the pinned Opentrons simulator before judging `simulation.txt`.

### Trial-2 contract finding and blocked status

Codex C0 trial-2 produced 1,032 plan rows because it reasonably represented individual mix strokes and low-level movements; the earlier Prompt had not defined that the oracle's 192 rows meant only eight **net liquid-transfer stages** per sample. The corrected draft Prompt now defines this granularity explicitly. This is an evaluation-contract defect, not evidence that mix operations are scientifically wrong.

The same trial correctly recorded `ModuleNotFoundError: No module named 'opentrons'`, marked simulation `FAILED / NOT EXECUTION-READY`, and aborted. Requiring simulation success when neither harness has the pinned simulator is invalid. Accordingly, `ls09-opentrons-sop` is blocked and its checker is `ACCEPTED=False`. It may be unblocked only by one of two frozen designs: (1) install and pin the same Opentrons simulator version and invocation in both harnesses; or (2) have the evaluator prevalidate the frozen protocol contract and provide a signed/checksummed validation record as an input, while no longer asking the agent to claim a simulation it cannot execute. Trial-2 observations are frozen in `docs/oracles/ls09-opentrons-sop/regressions/codex-c0-trial-2.json`.

## `ls09-plate-dilution-recovery`

- The Opentrons official tutorial uses serial dilution as the canonical automated dilution workflow: https://docs.opentrons.com/python-api/tutorial/
- Dilution concentration is evaluated by conservation of solute, `C_source * V_transfer = C_final * V_final`; this is the standard mass-balance relation, instantiated entirely by frozen fixture values.
- Pipette feasibility is evaluated against the frozen P20 (2–20 uL) and P300 (20–300 uL) ranges supplied in `pipettes.csv`, consistent with the official rule that a volume must be within the configured instrument range.

The log explicitly records that the B2 tip-pickup error occurred before aspiration, so no liquid moved. The oracle accepts a controlled semantic rendering of this failure (for example, spaces versus underscores and “aspirate” versus “aspiration”) while still requiring the concepts tip pickup, failure, before, and aspiration. A1–A3 and B1 are complete; only B2 and B3 require recovery. For each B well, `25 uM * 2 uL / 100 uL = 0.5 uM`, with 98 uL diluent. The output contract identifies the P20 for the 2-uL intermediate transfer and the P300 for the distinct 98-uL diluent movement in separate fields; a legacy combined `pipette` value is deliberately rejected as ambiguous. The oracle also checks source inventory and prevents an infeasible direct-stock transfer from being silently substituted.
