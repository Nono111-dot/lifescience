from __future__ import annotations
import csv,json,re
from pathlib import Path
ACCEPTED=True
def _bool(x):
    v=str(x).strip().lower()
    return True if v in {'true','1','yes'} else False if v in {'false','0','no'} else None
def check(workspace:Path):
    try:
        with (workspace/'output'/'construct_audit.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    except Exception:rows=[]
    gold=json.loads((Path(__file__).parent/'gold.json').read_text())['rows'];by={r.get('construct_id',''):r for r in rows};ids=len(rows)==len(by)==3 and set(by)=={g['construct_id'] for g in gold}
    fields={k:[] for k in ['frame_ok','start_ok','stop_ok','tag_ok']};statuses=[];issues=[]
    for g in gold:
        r=by.get(g['construct_id'],{})
        for k in fields:fields[k].append(_bool(r.get(k)) is g[k])
        statuses.append(r.get('overall_status','').lower()==g['overall_status'])
        got={x for x in re.split(r'[;,|\s]+',r.get('issues','').upper()) if x};issues.append(set(g['issues'])<=got)
    core=sum(10 for k in fields if all(fields[k]));direction=15 if all(statuses) and all(issues) else 0
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else ''
    summary=all(x in report for x in ['c01','c02','c03']) and ('no' in report or 'none' in report) and ('pass' in report or 'usable' in report)
    failures=[]
    if not ids:failures.append('CONSTRUCT_COVERAGE_MISMATCH')
    for k,v in fields.items():
        if not all(v):failures.append(k.upper()+'_MISMATCH')
    if not all(statuses):failures.append('OVERALL_STATUS_MISMATCH')
    if not all(issues):failures.append('ISSUE_LABEL_MISMATCH')
    if not summary:failures.append('REPORT_MISMATCH')
    return {'core_science':core,'direction':direction,'summary':5 if summary else 0,'hardgate_pass':ids and core==40 and direction==15,'failure_codes':failures,'criteria':{'all_constructs_once':ids,**{k+'_3_of_3':sum(v) for k,v in fields.items()},'overall_status_3_of_3':sum(statuses),'issues_3_of_3':sum(issues),'report_no_usable_construct':summary}}
