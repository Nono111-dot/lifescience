from __future__ import annotations
import json,struct
from pathlib import Path
ACCEPTED=True
def check(workspace:Path):
    try:d=json.loads((workspace/'output'/'shape_call.json').read_text())
    except Exception:d={}
    call=str(d.get('shape',d.get('letter',''))).strip().upper()=='T';atom=str(d.get('atom_selection','')).upper() in {'CA','C-ALPHA','ALPHA CARBON'}
    try:n_ok=int(d.get('n_atoms',d.get('n_ca_atoms')))==2388
    except Exception:n_ok=False
    method=bool(d.get('method')) and bool(d.get('projection'));evidence=str(d.get('evidence',d.get('interpretation',''))).lower();geometry=('crossbar' in evidence or 'horizontal' in evidence) and ('stem' in evidence or 'vertical' in evidence)
    p=workspace/'output'/'shape_view.png';png=False
    try:
        b=p.read_bytes();w,h=struct.unpack('>II',b[16:24]);png=b[:8]==b'\x89PNG\r\n\x1a\n' and w>=300 and h>=300 and len(b)>=5000
    except Exception:pass
    core=(20 if call else 0)+(6 if atom else 0)+(4 if n_ok else 0)+(5 if method else 0)+(5 if png else 0);decision=call and geometry
    failures=[]
    for ok,code in [(call,'SHAPE_CALL'),(atom,'ATOM_SELECTION'),(n_ok,'ATOM_COUNT'),(method,'PROJECTION_METADATA'),(png,'PNG_VIEW'),(geometry,'GEOMETRY_EVIDENCE')]:
        if not ok:failures.append(code+'_MISMATCH')
    return {'core_science':core,'direction':15 if decision else 0,'summary':5 if geometry else 0,'hardgate_pass':core==40 and decision,'failure_codes':failures,'criteria':{'letter_T':call,'CA_selection':atom,'2388_CA_atoms':n_ok,'projection_declared':method,'render_at_least_300px_and_5KB':png,'crossbar_and_stem_evidence':geometry}}
