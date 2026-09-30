#!/usr/bin/env python3
"""Conductellence law/control/review binding coverage audit."""

from pathlib import Path
import json,re

LAW=Path("LAW/CONDUCTELLENCE-ACT.md")
REGISTRY=Path("CONTROL-CATALOGUE/law-bindings.json")
STATE=Path("GOVERNANCE/enforcement-state.json")
REVIEW_BINDINGS=Path("REVIEW-CATALOGUE/bindings.json")

def die(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for path in (LAW,REGISTRY,STATE,REVIEW_BINDINGS):
    if not path.exists(): die(f"missing required file: {path}")

law=LAW.read_text(encoding="utf-8")
markers=re.findall(r'<!-- cdx:section id="([^"]+)" auditability="([^"]+)" -->',law)
law_ids={sid for sid,_ in markers}
auditability={sid:state for sid,state in markers}

registry=json.loads(REGISTRY.read_text())
state=json.loads(STATE.read_text())
review=json.loads(REVIEW_BINDINGS.read_text())
entries=registry.get("sections",[])
reg_ids={e["section_id"] for e in entries}
review_ids={e["section_id"] for e in review.get("bindings",[])}

missing=sorted(law_ids-reg_ids)
orphaned=sorted(reg_ids-law_ids)
if missing: die(f"{len(missing)} law §§ missing from binding registry: {missing[:10]}")
if orphaned: die(f"{len(orphaned)} orphaned binding entries: {orphaned[:10]}")

operational=[]
defects=[]
for e in entries:
    sid=e["section_id"]
    cls=auditability[sid]
    audits=e.get("audits",[])
    if cls=="FULLY_AUTOMATABLE":
        if not e.get("controls") or not audits:
            defects.append((sid,"missing executable control/audit"))
            continue
        if e.get("binding_state") not in {"IMPLEMENTED","VERIFIED"}:
            defects.append((sid,f"invalid machine binding state {e.get('binding_state')}"))
            continue
    else:
        reviews=e.get("review_procedures",[])
        if not reviews or not audits:
            defects.append((sid,"missing review procedure/audit"))
            continue
        if sid not in review_ids:
            defects.append((sid,"review procedure not present in review-binding registry"))
            continue
        if e.get("binding_state") not in {"REVIEW_BOUND","VERIFIED_REVIEW"}:
            defects.append((sid,f"invalid review binding state {e.get('binding_state')}"))
            continue
    operational.append(sid)

if defects:
    for sid,why in defects[:50]:
        print(f"DEFECT: {sid}: {why}")
    die(f"{len(defects)} provisions lack an operational machine/review path")

print(f"INFO: law §§={len(law_ids)} operationally_bound={len(operational)}")
print(f"INFO: machine_bound={sum(1 for e in entries if auditability[e['section_id']]=='FULLY_AUTOMATABLE')}")
print(f"INFO: review_bound={sum(1 for e in entries if auditability[e['section_id']]!='FULLY_AUTOMATABLE')}")
print(f"INFO: enforcement mode={state.get('mode')}")
print("PASS: every law § has an operational control or review-governance path")
