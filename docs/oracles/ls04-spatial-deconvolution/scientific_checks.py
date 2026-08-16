from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    gold=json.loads((Path(__file__).parent/'gold.json').read_text());valid=set(gold['weights'])
    try:
        with (workspace/'output'/'spot_710_composition.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    except Exception:rows=[]
    by={r.get('cell_type',''):r for r in rows};coverage=len(rows)==len(by) and bool(rows) and set(by)<=valid;vals={};finite=True
    for ct,r in by.items():
        try:vals[ct]=float(r.get('weight'));finite &= math.isfinite(vals[ct]) and vals[ct]>=0
        except Exception:finite=False
    norm=finite and math.isclose(sum(vals.values()),1,abs_tol=.01);supported={ct for ct,w in vals.items() if w>=.05};types=supported==set(gold['supported_types_at_0.05']);weights=all(abs(vals.get(ct,0)-w)<=.035 for ct,w in gold['weights'].items());evidence=all(bool(r.get('evidence','').strip()) for r in rows)
    core=(16 if types else 0)+(18 if weights else 0)+(6 if norm else 0);mixture=types and len(supported)==3
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else ''
    summary=all(x in report for x in ['b_cell','endothelial','macrophage']) and ('mixture' in report or 'mixed' in report)
    failures=[]
    for ok,code in [(coverage,'LABEL_COVERAGE'),(finite,'FINITE_NONNEGATIVE'),(norm,'WEIGHT_SUM'),(types,'SUPPORTED_TYPES'),(weights,'WEIGHT_VALUES'),(evidence,'EVIDENCE'),(mixture,'MIXTURE_DECISION'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if mixture else 0,'summary':5 if summary else 0,'hardgate_pass':coverage and finite and norm and types and weights and evidence,'failure_codes':failures,'criteria':{'valid_unique_labels':coverage,'finite_nonnegative':finite,'weights_sum_one':norm,'supported_types_exact':types,'six_weight_vector_with_0.035_tolerance':weights,'evidence_each_row':evidence,'three_type_mixture':mixture,'report_consistent':summary}}
