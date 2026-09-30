#!/usr/bin/env python3
from pathlib import Path
import json

STATE=Path("SPETL/evidence-preservation-state.json")
RUNTIME=Path("SPETL/spetl.py")
ENFORCEMENT=Path("GOVERNANCE/enforcement-state.json")

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (STATE,RUNTIME,ENFORCEMENT):
    if not p.exists(): fail(f"missing {p}")

state=json.loads(STATE.read_text())
enforcement=json.loads(ENFORCEMENT.read_text())

if state.get("schema")!="cdx.spetl.evidence-preservation-state/v1.0":
    fail("unexpected preservation-state schema")
if state.get("system_id")!="CDX-SYS-002":
    fail("wrong SPETL system id")
if state.get("reference_runtime",{}).get("state")!="OPERATIONAL":
    fail("SPETL reference runtime not operational")
if state.get("reference_runtime",{}).get("implementation")!="SPETL/spetl.py":
    fail("canonical SPETL implementation mismatch")

ind=state.get("independent_preservation",{})
verified=ind.get("satisfies_enforcing_requirement") is True
if verified:
    if ind.get("state")!="VERIFIED":
        fail("independent preservation claims satisfaction without VERIFIED state")
    if not ind.get("verification_evidence"):
        fail("VERIFIED independent preservation lacks verification evidence")
else:
    if ind.get("blocker_id")!="CDX-BLOCK-EVIDENCE-INDEPENDENCE-001":
        fail("open independent-preservation state lacks canonical blocker id")
    if enforcement.get("mode")=="ENFORCING":
        fail("ENFORCING declared without independent evidence preservation")

print("PASS: SPETL reference-runtime evidence semantics are operational")
print(f"INFO: independent evidence preservation verified={verified}")
print("PASS: independent evidence state cannot silently satisfy ENFORCING")
