#!/usr/bin/env python3
from pathlib import Path
import json

def fail(m):
    print("FAIL:",m); raise SystemExit(1)

P=Path("ESTATE-REGISTRY/systems.json")
if not P.exists(): fail("missing estate registry")
d=json.loads(P.read_text())
systems=d.get("systems",[])
if not systems: fail("empty estate registry")
ids=[x.get("system_id") for x in systems]
repos=[x.get("repository") for x in systems]
if len(ids)!=len(set(ids)): fail("duplicate system_id")
if len(repos)!=len(set(repos)): fail("duplicate repository")
root=[x for x in systems if x.get("system_id")=="CDX-SYS-001"]
if len(root)!=1: fail("Conductellence root missing or duplicated")
for s in systems:
    if not s.get("repository"): fail(f"{s.get('system_id')}: repository missing")
    if s["system_id"]!="CDX-SYS-001":
        if s.get("authority_ref")!="CDX-SYS-001": fail(f"{s['system_id']}: wrong authority_ref")
        if s.get("binding_manifest")!=".security/conductellence.json": fail(f"{s['system_id']}: binding manifest missing")
        if s.get("runtime_integration_state") not in {"NOT_VERIFIED","VERIFIED_REFERENCE_RUNTIME","VERIFIED_PRODUCTION_RUNTIME"}:
            fail(f"{s['system_id']}: invalid runtime integration state {s.get('runtime_integration_state')}")
print(f"PASS: Estate Registry contains {len(systems)} unique governed repository records")
print("PASS: repository binding is kept distinct from runtime integration verification")
