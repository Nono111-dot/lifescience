from __future__ import annotations
import csv, json, math
from pathlib import Path

ACCEPTED = True

def _rows(path):
    try:
        with path.open(encoding="utf-8-sig", newline="") as h: return list(csv.DictReader(h))
    except Exception: return []

def check(workspace: Path):
    gold=json.loads((Path(__file__).parent/'gold.json').read_text())['rows']; rows=_rows(workspace/'output'/'ranked_guides.csv')
    by={r.get('guide_id',''):r for r in rows}; ids=len(rows)==len(by)==len(gold) and set(by)=={g['guide_id'] for g in gold}
    rank=[]; score=[]; risk=[]; decision=[]; rationale=[]
    for g in gold:
        r=by.get(g['guide_id'],{})
        try: rank.append(int(r.get('rank',''))==g['rank'])
        except Exception: rank.append(False)
        try: score.append(math.isclose(float(r.get('on_target_score','nan')),g['on_target_score'],abs_tol=1e-9))
        except Exception: score.append(False)
        risk.append(r.get('risk_class','').lower()==g['risk_class'])
        decision.append(r.get('decision','').lower()==g['decision'])
        rationale.append(bool(r.get('rationale','').strip()))
    core=(16 if all(rank) else 0)+(6 if all(score) else 0)+(10 if all(risk) else 0)+(8 if all(rationale) else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else ''
    summary='g02' in report and ('coding' in report or 'exon' in report) and ('trade' in report or 'risk' in report)
    failures=[]
    for ok,code in [(ids,'GUIDE_COVERAGE'),(all(rank),'GUIDE_ORDER'),(all(score),'ACTIVITY_TRACE'),(all(risk),'RISK_CLASS'),(all(rationale),'RATIONALE'),(all(decision),'DECISION'),(summary,'REPORT')]:
        if not ok: failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if all(decision) else 0,'summary':5 if summary else 0,
      'hardgate_pass':ids and all(rank) and all(score) and all(risk) and all(decision) and all(rationale),
      'failure_codes':failures,'criteria':{'all_guides_once':ids,'rank_rule_6_of_6':sum(rank),'activity_trace_6_of_6':sum(score),'risk_class_6_of_6':sum(risk),'decision_6_of_6':sum(decision),'rationale_6_of_6':sum(rationale),'report_top_choice_and_tradeoff':summary}}
