from __future__ import annotations
import csv, json, math
from pathlib import Path

# The public prompt says EP1-EP8 but the supplied files/options contain EP1-EP7,
# and CompBioBench does not publish its hidden answer or integration rule.
ACCEPTED = False

def check(workspace: Path):
    out=workspace/'output'; failures=[]; criteria={}
    try:
        with (out/'pair_evidence.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    except Exception: rows=[]
    ids=[str(r.get('pair_id','')) for r in rows]
    expected={f'EP{i}' for i in range(1,8)}
    coverage=set(ids)==expected and len(ids)==len(set(ids))==7
    finite=True
    for r in rows:
        try: finite &= all(math.isfinite(float(r[k])) for k in ('contact_evidence','perturbation_effect','combined_support','rank'))
        except Exception: finite=False
    try: call=json.loads((out/'least_supported.json').read_text(encoding='utf-8'))
    except Exception: call={}
    called=str(call.get('pair_id',call.get('least_supported','')))
    min_consistent=False
    if coverage and finite and called in expected:
        vals={r['pair_id']:float(r['combined_support']) for r in rows}; min_consistent=vals[called]==min(vals.values())
    core=(15 if coverage else 0)+(10 if finite and rows else 0)+(15 if min_consistent else 0)
    direction=10 if min_consistent else 0
    summary=0
    if not coverage: failures.append('EP_PAIR_SET_INVALID')
    if not finite: failures.append('EP_VALUES_INVALID')
    if not min_consistent: failures.append('EP_CALL_NOT_TABLE_MINIMUM')
    failures.extend(['EP8_NATIVE_PROMPT_INCONSISTENCY','EP_INTEGRATION_RULE_NOT_PINNED'])
    criteria.update(seven_supplied_pairs=coverage,finite_values=finite,call_matches_reported_minimum=min_consistent,
                    formal_blocker='EP8 omitted and no public hidden rule/gold')
    return {'core_science':core,'direction':direction,'summary':summary,'hardgate_pass':False,
            'failure_codes':failures,'criteria':criteria}
