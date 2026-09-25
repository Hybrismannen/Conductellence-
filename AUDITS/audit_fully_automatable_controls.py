#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json

LAW=Path("CONTROL-CATALOGUE/law-bindings.json")
REG=Path("POLICY/control-registry.json")
ENGINE=Path("POLICY/engine.py")

def fail(m):
    print("FAIL:",m)
    raise SystemExit(1)

for p in (LAW,REG,ENGINE):
    if not p.exists(): fail(f"missing {p}")

b=json.loads(LAW.read_text())
r=json.loads(REG.read_text())
spec=importlib.util.spec_from_file_location("cdx_policy",ENGINE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
controls={c["control_id"]:c for c in r["controls"]}
full=[s for s in b["sections"] if s["auditability"]=="FULLY_AUTOMATABLE"]

if len(full)!=69: fail(f"expected 69 FULLY_AUTOMATABLE sections, got {len(full)}")

for s in full:
    if s.get("binding_state") not in {"IMPLEMENTED","VERIFIED"}:
        fail(f"{s['section_id']}: not implemented")
    if len(s.get("controls",[]))!=1:
        fail(f"{s['section_id']}: requires exactly one canonical runtime control")
    cid=s["controls"][0]
    if cid not in controls: fail(f"{s['section_id']}: missing control {cid}")
    c=controls[cid]
    vectors=c.get("test_vectors",[])
    if len(vectors)<2: fail(f"{cid}: allow/deny vectors missing")
    for v in vectors:
        out=m.evaluate(v["context"],[cid])
        if out["decision"]!=v["expected"]:
            fail(f"{cid}/{v['name']}: expected {v['expected']} got {out['decision']}")

print(f"PASS: {len(full)} FULLY_AUTOMATABLE §§ have executable controls")
print(f"PASS: {len(controls)} control objects passed deterministic allow/deny vectors")
