# LS05 benchmark-informed local extensions

## Status and provenance boundary

`ls05-structure-model-ranking` and `ls05-low-confidence-pocket` are local evaluation
extensions. They are **not** claimed as BioAgentBench, BixBench, CompBioBench, or
BioDesignBench items. Their small input tables are synthetic fixtures; all numeric gold
values are deterministic transformations or lookups from those committed tables.

This construction is used because the reviewed public benchmark sets do not provide two
additional, unused LS05 items with public prompts, inputs and graders. It preserves the LS05
sub-domain while keeping provenance explicit.

## Scientific basis

### Structure-model ranking

- Zhang Y, Skolnick J. *Scoring function for automated assessment of protein structure
  template quality*. Proteins. 2004;57:702-710. DOI
  [10.1002/prot.20264](https://doi.org/10.1002/prot.20264). TM-score is a global,
  length-normalized model/reference similarity score.
- Mariani V et al. *lDDT: a local superposition-free score for comparing protein structures
  and models using distance difference tests*. Bioinformatics. 2013;29:2722-2728. DOI
  [10.1093/bioinformatics/btt473](https://doi.org/10.1093/bioinformatics/btt473). lDDT
  supplies complementary local-quality evidence.

The frozen rule is lexicographic rather than an invented weighted composite. It first
requires complete chain mapping, then uses TM-score and lDDT as primary global/local
evidence; RMSD, aligned coverage and critical-region error are secondary diagnostics.

### Low-confidence pocket

- [AlphaFold Protein Structure Database FAQ](https://alphafold.ebi.ac.uk/faq) defines
  pLDDT as local confidence, advises that regions below 50 should not be interpreted, and
  explains that high PAE means relative placement is uncertain.
- Jumper J et al. *Highly accurate protein structure prediction with AlphaFold*. Nature.
  2021;596:583-589. DOI
  [10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2).
- Terwilliger TC et al. *AlphaFold predictions are valuable hypotheses and accelerate but
  do not replace experimental structure determination*. Nature Methods. 2024;21:110-116.
  DOI [10.1038/s41592-023-02087-4](https://doi.org/10.1038/s41592-023-02087-4).

Accordingly, the oracle rewards calibrated deferral when every nominated pocket interval
has pLDDT below 50 and high PAE. It never converts predicted ΔΔG or activity labels into
experimental facts.

## Reproducibility contract

- Frozen rules live beside the inputs in each `SCORING_RULE.md`.
- Gold artifacts live only under `docs/oracles/<task-id>/gold.json`; they are not copied to
  a run workspace.
- `scientific_checks.py` reads frozen submission artifacts but never imports the submitted
  `analysis.py`.
- Each checker has reference, empty-output and deliberately wrong-answer acceptance tests.
- Deterministic score remains 80 points: coverage 10, core science 40, direction 15,
  summary 5, script 10. The separate blind judge supplies the remaining 20 points.

## Known limits

These fixtures test evidence handling and calibrated structural interpretation, not atomistic
structure calculation, pocket detection, docking, experimental binding, or mutation-effect
prediction. A later public benchmark with released prompt, coordinates, gold and grader
should replace them rather than being silently merged with them.

