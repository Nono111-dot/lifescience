from __future__ import annotations
import csv,json,math
from collections import defaultdict
from pathlib import Path
ACCEPTED=True
def _rows(p):
    try:
        with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
    except Exception:return []
def check(workspace:Path):
    source=workspace/'inputs'/'single_cell_dynamics_question.csv'
    if not source.is_file():source=Path(__file__).parents[2]/'inputs'/'ls03-genome-coordinates'/'single_cell_dynamics_question.csv'
    groups=defaultdict(list)
    with source.open(newline='') as h:
        for r in csv.DictReader(h):
            d=math.sqrt(sum((float(r['enh_'+a])-float(r['prom_'+a]))**2 for a in 'xyz'));groups[r['cell_id']].append((int(r['time']),d,int(r['transcription'])))
    expected={}
    for cid,v in groups.items():
        v.sort();expected[cid]=(len(v),sum(x[1] for x in v)/len(v),sum(x[1]<=260 for x in v)/len(v),sum(x[2] for x in v)/len(v))
    rows=_rows(workspace/'output'/'cell_metrics.csv');by={r.get('cell_id',''):r for r in rows};coverage=len(rows)==len(by)==600 and set(by)==set(expected);metrics=[]
    for cid,e in expected.items():
        r=by.get(cid,{})
        try:metrics.append(int(float(r.get('n_timepoints')))==e[0] and math.isclose(float(r.get('mean_distance_nm')),e[1],abs_tol=1e-6) and math.isclose(float(r.get('contact_fraction')),e[2],abs_tol=1e-9) and math.isclose(float(r.get('transcription_fraction')),e[3],abs_tol=1e-9))
        except Exception:metrics.append(False)
    lrows=_rows(workspace/'output'/'lag_analysis.csv');lb={int(float(r.get('lag'))):r for r in lrows if r.get('lag','')};lagcov=len(lrows)==len(lb)==41 and set(lb)==set(range(-20,21));peak=False;nobs=False
    if lagcov:
        try:
            vals={k:float(r['association']) for k,r in lb.items()};peak=max(vals,key=lambda k:abs(vals[k]))==-1 and math.isclose(vals[-1],0.07784324772318195,abs_tol=1e-6);nobs=int(float(lb[-1]['n_observations']))==149400 and all(int(float(lb[k]['n_observations']))==600*(250-abs(k)) for k in lb)
        except Exception:pass
    core=(20 if all(metrics) else 0)+(10 if lagcov else 0)+(6 if peak else 0)+(4 if nobs else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';association=('lag -1' in report or 'lag = -1' in report or '-1 lag' in report) and ('0.077' in report or '0.078' in report);restraint=('cannot' in report or 'does not' in report or 'not establish' in report) and ('caus' in report)
    failures=[]
    for ok,code in [(coverage,'CELL_COVERAGE'),(all(metrics),'CELL_METRICS'),(lagcov,'LAG_COVERAGE'),(peak,'PEAK_LAG'),(nobs,'LAG_N'),(association,'REPORT_ASSOCIATION'),(restraint,'CAUSAL_RESTRAINT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if association and restraint else 0,'summary':5 if association and restraint else 0,'hardgate_pass':coverage and all(metrics) and lagcov and peak and nobs and restraint,'failure_codes':failures,'criteria':{'600_cells_exact':coverage,'cell_metrics_600_of_600':sum(metrics),'lags_minus20_to_plus20':lagcov,'peak_abs_lag_minus1':peak,'lag_observation_counts':nobs,'report_peak':association,'no_causal_overclaim':restraint}}
