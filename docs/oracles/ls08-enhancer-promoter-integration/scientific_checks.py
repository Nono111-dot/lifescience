from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    g=json.loads((Path(__file__).parent/'gold.json').read_text())
    try:
        with (workspace/'output'/'pair_evidence.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
    except Exception:rows=[]
    by={r.get('pair_id',''):r for r in rows};coverage=len(rows)==len(by)==7 and set(by)=={f'EP{i}' for i in range(1,8)};contact=[];effect=[];support=[];rank=[]
    for x in g['rows']:
        r=by.get(x['pair_id'],{})
        for out,key,tol in [(contact,'contact_evidence',.02),(effect,'perturbation_effect',.02),(support,'combined_support',.03)]:
            try:out.append(math.isclose(float(r.get(key)),x[key],abs_tol=tol))
            except Exception:out.append(False)
        try:rank.append(int(float(r.get('rank')))==x['rank'])
        except Exception:rank.append(False)
    try:call=json.loads((workspace/'output'/'least_supported.json').read_text())
    except Exception:call={}
    called=str(call.get('pair_id',call.get('least_supported','')));call_ok=called=='EP3';core=(10 if all(contact) else 0)+(10 if all(effect) else 0)+(10 if all(support) else 0)+(10 if all(rank) else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';summary='ep3' in report and ('contact' in report or 'hi-c' in report) and ('perturb' in report or 'expression' in report) and ('ep8' in report or 'seven' in report or '7' in report)
    failures=[]
    for ok,code in [(coverage,'PAIR_COVERAGE'),(all(contact),'CONTACT_Z'),(all(effect),'PERTURBATION_EFFECT'),(all(support),'COMBINED_SUPPORT'),(all(rank),'ELIGIBLE_RANK'),(call_ok,'LEAST_SUPPORTED_CALL'),(summary,'REPORT')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if call_ok else 0,'summary':5 if summary else 0,'hardgate_pass':coverage and core==40 and call_ok,'failure_codes':failures,'criteria':{'EP1_to_EP7_once':coverage,'contact_7_of_7':sum(contact),'effect_7_of_7':sum(effect),'support_7_of_7':sum(support),'rank_7_of_7':sum(rank),'EP3_call':call_ok,'report_two_modalities_and_missing_EP8':summary}}
