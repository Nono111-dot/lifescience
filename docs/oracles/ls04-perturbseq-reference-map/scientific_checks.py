from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    gold=json.loads((Path(__file__).parent/'gold.json').read_text())['rows']
    try:
        with (workspace/'output'/'guide_mapping.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    except Exception:rows=[]
    by={r.get('target_gene','').upper():r for r in rows};coverage=len(rows)==len(by)==3 and set(by)=={'PABPC1','NUDT21','LEO1'} and len({r.get('query_guide_id') for r in rows})==3
    ids=[];scores=[];runners=[];conf=[]
    for g in gold:
        r=by.get(g['target_gene'],{});ids.append(r.get('query_guide_id')==g['query_guide_id'])
        try:scores.append(math.isclose(float(r.get('score')),g['score'],abs_tol=0.015))
        except Exception:scores.append(False)
        try:runners.append(math.isclose(float(r.get('runner_up_score')),g['runner_up_score'],abs_tol=0.02))
        except Exception:runners.append(False)
        conf.append(r.get('confidence','').lower()==g['confidence'])
    core=(24 if all(ids) else 0)+(8 if all(scores) else 0)+(8 if all(runners) else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else ''
    summary=all(x in report for x in ['pabpc1','guide18','nudt21','guide13','leo1','guide14']) and ('ambigu' in report or 'low confidence' in report)
    failures=[]
    for ok,code in [(coverage,'TARGET_COVERAGE'),(all(ids),'GUIDE_IDENTITY'),(all(scores),'MATCH_SCORE'),(all(runners),'RUNNER_UP'),(all(conf),'CONFIDENCE'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if all(conf) else 0,'summary':5 if summary else 0,'hardgate_pass':coverage and all(ids) and all(scores) and all(runners) and all(conf),'failure_codes':failures,'criteria':{'three_unique_targets_and_guides':coverage,'mapping_3_of_3':sum(ids),'scores_3_of_3':sum(scores),'runner_ups_3_of_3':sum(runners),'confidence_3_of_3':sum(conf),'report_all_mappings_and_ambiguity':summary}}
