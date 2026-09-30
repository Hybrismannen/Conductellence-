#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,tempfile,os

EST=Path("ESTATE-REGISTRY/systems.json")
CTRL=Path("POLICY/control-registry.json")
BUILDER=Path("SECURITY-TWIN/build_twin.py")

for p in (EST,CTRL,BUILDER):
    if not p.exists(): raise SystemExit("FAIL missing "+str(p))

estate=json.loads(EST.read_text())
controls=json.loads(CTRL.read_text())
if not estate.get("systems"): raise SystemExit("FAIL empty estate")
if len(controls.get("controls",[]))!=69: raise SystemExit("FAIL control count")

spec=importlib.util.spec_from_file_location("twin_builder",BUILDER)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=m.build()
systems=[n for n in d["nodes"] if n["type"]=="SYSTEM"]
control_nodes=[n for n in d["nodes"] if n["type"]=="CONTROL"]
if len(systems)!=len(estate["systems"])-1: raise SystemExit("FAIL system projection")
if len(control_nodes)!=69: raise SystemExit("FAIL control projection")
print(f"PASS: Security Twin projects {len(systems)} governed systems and {len(control_nodes)} controls")
