from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    gold=json.loads((Path(__file__).parent/'gold.json').read_text())
    try:
        with (workspace/'output'/'composition.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    except Exception:rows=[]
    aliases={'1':'sample1','2':'sample2','sample 1':'sample1','sample 2':'sample2','sample1':'sample1','sample2':'sample2'};by={};valid=True
    for r in rows:
        s=aliases.get(r.get('sample','').strip().lower());ct=r.get('cell_type','')
        if not s or (s,ct) in by:valid=False
        by[(s,ct)]=r
    expected={(s,ct) for s,d in gold['counts'].items() for ct in d};coverage=valid and set(by)==expected
    count_ok=[];fraction_ok=[];sums={s:0 for s in gold['counts']}
    for s,d in gold['counts'].items():
        total=gold['sample_totals'][s]
        for ct,n in d.items():
            r=by.get((s,ct),{})
            try:count_ok.append(int(float(r.get('n_cells','nan')))==n)
            except Exception:count_ok.append(False)
            try:f=float(r.get('fraction','nan'));fraction_ok.append(math.isclose(f,n/total,abs_tol=1e-6));sums[s]+=f
            except Exception:fraction_ok.append(False)
    sums_ok=all(math.isclose(x,1,abs_tol=1e-6) for x in sums.values())
    try:call=json.loads((workspace/'output'/'depleted_call.json').read_text())
    except Exception:call={}
    called=str(call.get('cell_type',call.get('depleted_cell_type','')));sample=str(call.get('depleted_in',call.get('sample',''))).lower();call_ok=called=='horizontal cell';direction=sample in {'sample2','sample 2','2'}
    core=(16 if all(count_ok) else 0)+(14 if all(fraction_ok) else 0)+(5 if sums_ok else 0)+(5 if call_ok else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else ''
    summary='horizontal' in report and ('sample 2' in report or 'sample2' in report) and ('lhx1' in report or 'onecut' in report or 'marker' in report)
    failures=[]
    for ok,code in [(coverage,'COMPOSITION_COVERAGE'),(all(count_ok),'CELL_COUNTS'),(all(fraction_ok),'FRACTIONS'),(sums_ok,'FRACTION_SUM'),(call_ok,'DEPLETED_TYPE'),(direction,'DEPLETION_DIRECTION'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if call_ok and direction else 0,'summary':5 if summary else 0,'hardgate_pass':coverage and core==40 and call_ok and direction,'failure_codes':failures,'criteria':{'32_rows_exact':coverage,'counts_correct':sum(count_ok),'counts_total':len(count_ok),'fractions_correct':sum(fraction_ok),'fractions_total':len(fraction_ok),'fractions_sum_one':sums_ok,'horizontal_cell_call':call_ok,'sample2_direction':direction,'report_marker_evidence':summary}}
