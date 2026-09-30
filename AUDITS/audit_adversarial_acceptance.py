#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json

SCENARIOS=Path("RED-TEAM/scenarios.json")
ENGINE=Path("POLICY/engine.py")

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (SCENARIOS,ENGINE):
    if not p.exists(): fail(f"missing {p}")

spec=importlib.util.spec_from_file_location("cdx_policy",ENGINE)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

doc=json.loads(SCENARIOS.read_text())
rows=doc.get("scenarios",[])
if len(rows)<15:
    fail(f"expected at least 15 critical scenarios, got {len(rows)}")

ids=[x["id"] for x in rows]
if len(ids)!=len(set(ids)):
    fail("duplicate adversarial scenario id")

for s in rows:
    out=m.evaluate(s["context"],s.get("control_ids"))
    if out["decision"]!=s["expected"]:
        fail(f"{s['id']} {s['title']}: expected {s['expected']} got {out}")
    if s["expected"] in {"DENY","SECURITY_STOP","CONSTITUTIONAL_STOP"} and out["decision"]=="ALLOW":
        fail(f"{s['id']}: prohibited fail-open")
    print(f"PASS CASE: {s['id']} -> {s['expected']}")

print(f"PASS: {len(rows)} critical adversarial scenarios")
print("PASS: composed and unknown-surface cases remain fail-closed")
