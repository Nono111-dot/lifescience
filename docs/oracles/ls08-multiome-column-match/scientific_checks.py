from __future__ import annotations
import csv, math
from pathlib import Path

# Public CompBioBench does not publish the hidden permutation, and the workspace
# does not contain the genome annotation required for an independent gene-activity mapping.
ACCEPTED = False

def check(workspace: Path):
    out=workspace/'output'; failures=[]; criteria={}
    try:
        with (out/'column_mapping.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    except Exception: rows=[]
    rna=[str(r.get('rna_population','')) for r in rows]; atac=[str(r.get('atac_column','')) for r in rows]
    coverage=len(rows)==8 and len(set(rna))==8 and len(set(atac))==8
    finite=True
    for r in rows:
        try: finite &= math.isfinite(float(r.get('match_score'))) and math.isfinite(float(r.get('runner_up_score')))
        except Exception: finite=False
    core=(20 if coverage else 0)+(10 if finite and rows else 0)
    direction=5 if coverage else 0
    report=(out/'report.md').read_text(encoding='utf-8',errors='replace') if (out/'report.md').is_file() else ''
    summary=0
    failures += ([] if coverage else ['MULTIOME_NOT_BIJECTION'])
    failures += ([] if finite else ['MULTIOME_SCORES_INVALID'])
    failures.append('MULTIOME_HIDDEN_PERMUTATION_NOT_DERIVED')
    criteria.update(bijection_structure=coverage,finite_scores=finite,
                    formal_blocker='No public native permutation; required annotation/reference is not pinned')
    return {'core_science':core,'direction':direction,'summary':summary,'hardgate_pass':False,
            'failure_codes':failures,'criteria':criteria}
