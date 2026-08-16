from __future__ import annotations
import csv,json,math
from pathlib import Path
ACCEPTED=True
def _rows(p):
    try:
        with p.open(encoding='utf-8-sig',newline='') as h:return list(csv.DictReader(h))
    except Exception:return []
def check(workspace:Path):
    g=json.loads((Path(__file__).parent/'gold.json').read_text());rows=_rows(workspace/'output'/'column_mapping.csv');by={r.get('rna_population',''):r for r in rows};coverage=len(rows)==len(by)==8 and set(by)==set(g['rna_columns']) and len({r.get('atac_column') for r in rows})==8
    amap={str(x['rna_population']):str(x['atac_column']) for x in g['assignment']};assignment=[];scores=[];runners=[];S=g['score_matrix']
    for rna in g['rna_columns']:
        r=by.get(rna,{});at=amap[rna];assignment.append(r.get('atac_column')==at)
        try:scores.append(math.isclose(float(r.get('match_score')),S[int(rna)][int(at)],abs_tol=.015))
        except Exception:scores.append(False)
        try:runners.append(math.isclose(float(r.get('runner_up_score')),sorted(S[int(rna)])[-2],abs_tol=.02))
        except Exception:runners.append(False)
    matrix=_rows(workspace/'output'/'score_matrix.csv');matrix_ok=len(matrix) in {8,64} and bool(matrix);core=(24 if all(assignment) else 0)+(8 if all(scores) else 0)+(4 if all(runners) else 0)+(4 if matrix_ok else 0)
    report=(workspace/'output'/'report.md').read_text(errors='replace').lower() if (workspace/'output'/'report.md').is_file() else '';method_ok='ensembl' in report and ('tss' in report or 'transcription start' in report) and ('hungarian' in report or 'one-to-one' in report)
    failures=[]
    for ok,code in [(coverage,'BIJECTION'),(all(assignment),'ASSIGNMENT'),(all(scores),'MATCH_SCORE'),(all(runners),'RUNNER_UP'),(matrix_ok,'SCORE_MATRIX'),(method_ok,'REPORT_METHOD')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if all(assignment) and coverage else 0,'summary':5 if method_ok else 0,'hardgate_pass':coverage and all(assignment) and all(scores) and all(runners) and matrix_ok,'failure_codes':failures,'criteria':{'eight_by_eight_bijection':coverage,'assignment_8_of_8':sum(assignment),'match_scores_8_of_8':sum(scores),'runner_ups_8_of_8':sum(runners),'score_matrix_shape':matrix_ok,'report_pinned_method':method_ok}}
