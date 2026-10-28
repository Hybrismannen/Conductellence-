#!/usr/bin/env python3
"""AUD-CDX-CONSTITUTIONAL-ADOPTION-001."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def fail(message):
    print("FAIL:", message)
    raise SystemExit(1)

def git_blob_sha(path):
    data=(ROOT/path).read_bytes()
    header=f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header+data).hexdigest()

candidate=load("GOVERNANCE/constitutional-adoption-candidate.json")
order=load("GOVERNANCE/orders/CDX-CONST-ADOPT-001.json")
state=load("GOVERNANCE/system-state.json")
boundary=load("GOVERNANCE/release-boundary-v1.json")
bindings=load("CONTROL-CATALOGUE/law-bindings.json")
phase_b=load("GOVERNANCE/household/records/CDX-HH-B-ACCEPT-001.json")
phase_c=load("GOVERNANCE/household/records/CDX-HH-C-ACCEPT-001.json")
phase_d=load("GOVERNANCE/household/records/CDX-HH-D-ACCEPT-001.json")
law=(ROOT/"LAW/CONDUCTELLENCE-ACT.md").read_text(encoding="utf-8")
core=(ROOT/"GOVERNANCE/household/records/CDX-CORE-CLOSEOUT-001.md").read_text(encoding="utf-8")

if candidate.get("candidate_id")!="CDX-CONST-CAND-001":
    fail("wrong constitutional candidate id")
if candidate.get("decision_order_id")!="CDX-CONST-ADOPT-001":
    fail("candidate/order linkage mismatch")
if order.get("order_id")!="CDX-CONST-ADOPT-001" or order.get("candidate_id")!=candidate.get("candidate_id"):
    fail("wrong or mismatched constitutional decision order")
if order.get("authority_required")!="HUMAN_SOVEREIGN_AUTHORITY":
    fail("constitutional decision not reserved to human sovereign authority")
if boundary.get("boundary_id")!="CDX-RC01-BOUNDARY-001" or boundary.get("state")!="FROZEN_FOR_CLOSURE":
    fail("RC-01 boundary unavailable or not frozen")
if boundary.get("active_exceptions"):
    fail("constitutional adoption cannot proceed with active boundary exception")

expected_ids=boundary.get("frozen_semantic_grammars",{}).get("law_section_ids",[])
observed_ids=[item.get("section_id") for item in bindings.get("sections",[])]
if observed_ids!=expected_ids or len(observed_ids)!=131:
    fail("constitutional section identity differs from RC-01 frozen set")

for name, record in [("B",phase_b),("C",phase_c),("D",phase_d)]:
    if record.get("director_state")!="ACCEPTED" or record.get("acceptance_state")!="PASS":
        fail(f"Legal Integrity phase {name} is not Director ACCEPTED/PASS")
if "Core state:" not in core or "REMEDIATED" not in core:
    fail("core remediation closeout is not recorded as REMEDIATED")

decision=order.get("decision")
order_state=order.get("state")
candidate_state=candidate.get("state")

if decision is None:
    if order_state!="PENDING_HUMAN_DECISION":
        fail("null decision must remain PENDING_HUMAN_DECISION")
    if candidate_state!="READY_FOR_HUMAN_DECISION":
        fail("pending candidate must be READY_FOR_HUMAN_DECISION")
    if state.get("constitutional_state")!="FOUNDATIONAL_DRAFT":
        fail("pending adoption cannot promote constitutional state")
    if "**Version:** 0.1.0-bootstrap" not in law or "**Status:** FOUNDATIONAL DRAFT" not in law:
        fail("pending candidate law header changed")
    expected_blob=candidate.get("source_snapshot",{}).get("law_blob_sha")
    if git_blob_sha("LAW/CONDUCTELLENCE-ACT.md")!=expected_blob:
        fail("pending constitutional law content differs from locked candidate blob")
    print("PASS: constitutional adoption candidate is ready and human decision remains pending.")
elif decision=="APPROVED":
    if order_state!="RESOLVED":
        fail("approved decision order must be RESOLVED")
    if not order.get("decision_by") or not order.get("decision_at"):
        fail("approved order requires human attribution and date")
    if candidate_state!="ADOPTED" or state.get("constitutional_state")!="ADOPTED":
        fail("approved order is not reflected as ADOPTED")
    if "**Version:** 1.0.0" not in law or "**Status:** ADOPTED" not in law:
        fail("adopted Act header is inconsistent")
    if state.get("release_state")!="PRE_RELEASE" or state.get("enforcement_state")!="BOOTSTRAP":
        fail("constitutional adoption improperly promoted release or enforcement")
    print("PASS: explicit constitutional adoption decision is consistently enacted.")
elif decision in {"RETURN_FOR_AMENDMENT","REJECTED"}:
    if order_state!="RESOLVED":
        fail("resolved non-approval decision must have RESOLVED order")
    if state.get("constitutional_state")!="FOUNDATIONAL_DRAFT":
        fail("non-approved candidate cannot promote constitutional state")
    print("PASS: constitutional candidate resolved without adoption.")
else:
    fail("unrecognized constitutional decision")

print("PASS: RC-01 topology and prior legal/core acceptance evidence remain intact.")
print("PASS: constitutional, release, enforcement and estate states remain separated.")
