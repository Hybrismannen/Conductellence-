#!/usr/bin/env python3
"""Conductellence Household clearance audit for Legal Integrity Phases B-D.

Audit ID: AUD-CDX-CLR-LEGAL-BD-001
Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import json

ORDER=Path("GOVERNANCE/orders/CDX-CLR-LEGAL-BD-001.md")
MANIFEST=Path("GOVERNANCE/household/legal-integrity-bd-manifest.json")
RECORD_ROOT=Path("GOVERNANCE/household/records")

PASS_STATES={"PASS","REPAIRED_PASS"}
ALLOWED={
  "B":{"DISPATCHED","IN_PROGRESS","COMPLETE_PENDING_DIRECTOR_ACCEPTANCE","PASS","REPAIRED_PASS"},
  "C":{"CLEARED_PENDING_B","DISPATCHED","IN_PROGRESS","COMPLETE_PENDING_DIRECTOR_ACCEPTANCE","PASS","REPAIRED_PASS"},
  "D":{"CLEARED_PENDING_C","DISPATCHED","IN_PROGRESS","COMPLETE_PENDING_DIRECTOR_ACCEPTANCE","PASS","REPAIRED_PASS"},
}

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (ORDER,MANIFEST):
    if not p.exists(): fail(f"missing required clearance object: {p}")

order=ORDER.read_text(encoding="utf-8")
manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))

if manifest.get("authority_ref")!="CDX-CLR-LEGAL-BD-001":
    fail("manifest authority_ref does not match clearance order")
if "AUTHORITY_REF=CDX-CLR-LEGAL-BD-001" not in order:
    fail("canonical compact audit citation missing")
if "Director acceptance is valid only for committed state under audit" not in order:
    fail("committed-state acceptance rule missing")

phases=manifest.get("phases",[])
if [p.get("phase") for p in phases]!=["B","C","D"]:
    fail("phase sequence must be exactly B -> C -> D")
states={p["phase"]:p.get("state") for p in phases}
for ph,state in states.items():
    if state not in ALLOWED[ph]:
        fail(f"invalid Phase {ph} state: {state}")

if phases[1].get("dependency")!="B:PASS": fail("Phase C must depend on B:PASS")
if phases[2].get("dependency")!="C:PASS": fail("Phase D must depend on C:PASS")

c_started=states["C"] not in {"CLEARED_PENDING_B"}
d_started=states["D"] not in {"CLEARED_PENDING_C"}
if c_started and states["B"] not in PASS_STATES:
    fail("Phase C progressed before Phase B accepted")
if d_started and states["C"] not in PASS_STATES:
    fail("Phase D progressed before Phase C accepted")

hard=set(manifest.get("hard_stops",[]))
required_hard={
 "SECURITY_STOP","CONSTITUTIONAL_STOP","LEGAL_REVIEW_REQUIRED",
 "DISPUTED_SEMANTIC_EQUIVALENCE","DISPUTED_APPLICABILITY",
 "CONSTITUTIONAL_AMENDMENT_REQUIRED","PRIMARY_SOURCE_CONFLICT"
}
if required_hard-hard:
    fail(f"clearance manifest missing hard stops: {sorted(required_hard-hard)}")

statement=manifest.get("audit_reference_statement","")
if "CDX-CLR-LEGAL-BD-001" not in statement or "does not pre-authorize PASS" not in statement:
    fail("audit_reference_statement is incomplete")

records=[]
if RECORD_ROOT.exists():
    for path in sorted(RECORD_ROOT.glob("*.json")):
        rec=json.loads(path.read_text(encoding="utf-8"))
        if rec.get("programme_id")!="CDX-PROG-LEGAL-BD-001": continue
        if rec.get("authority_ref")!="CDX-CLR-LEGAL-BD-001":
            fail(f"{path}: wrong/missing authority_ref")
        phase=rec.get("phase")
        if phase not in {"B","C","D"}: fail(f"{path}: invalid phase")
        state=rec.get("acceptance_state")
        if state in PASS_STATES:
            if not rec.get("committed_sha"): fail(f"{path}: PASS lacks committed_sha")
            if rec.get("hard_stops"): fail(f"{path}: PASS with unresolved hard_stops")
            if rec.get("unresolved_legal_review"): fail(f"{path}: PASS with unresolved legal review")
            for field in ("janitor_scan_ref","ci_run_ref","accepted_at"):
                if not rec.get(field): fail(f"{path}: PASS lacks {field}")
        records.append(rec)

for ph,state in states.items():
    if state in PASS_STATES:
        matches=[r for r in records if r.get("phase")==ph and r.get("acceptance_state") in PASS_STATES]
        if not matches: fail(f"Phase {ph} manifest says {state} without acceptance record")
        if not any(r.get("acceptance_state")==state or state=="PASS" for r in matches):
            fail(f"Phase {ph} acceptance records do not support manifest state {state}")

programme_state=manifest.get("programme_state")
if programme_state=="CLOSED" and any(states[p] not in PASS_STATES for p in ("B","C","D")):
    fail("programme cannot be CLOSED before B, C and D all PASS")

print("PASS: CDX-CLR-LEGAL-BD-001 is structurally valid")
print(f"PASS: lifecycle states B={states['B']} C={states['C']} D={states['D']}")
print("PASS: B -> C -> D dependency and hard-stop semantics are preserved")
print("PASS: every accepted phase is backed by committed Household acceptance evidence")
