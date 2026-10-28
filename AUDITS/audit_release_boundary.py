#!/usr/bin/env python3
"""CDX 1.0 release-boundary audit.

Audit ID: AUD-CDX-RELEASE-BOUNDARY-001
Purpose: detect architectural scope creep during RC-01 closure without
blocking remediation inside the existing Conductellence domains.
"""
from pathlib import Path
import json
import re

def fail(message):
    print("FAIL:", message)
    raise SystemExit(1)

BOUNDARY=Path("GOVERNANCE/release-boundary-v1.json")
LAW=Path("LAW/CONDUCTELLENCE-ACT.md")
BINDINGS=Path("CONTROL-CATALOGUE/law-bindings.json")

for p in (BOUNDARY, LAW, BINDINGS):
    if not p.exists():
        fail(f"missing required boundary input: {p}")

b=json.loads(BOUNDARY.read_text(encoding="utf-8"))
law=LAW.read_text(encoding="utf-8")
bindings=json.loads(BINDINGS.read_text(encoding="utf-8"))

if b.get("boundary_id")!="CDX-RC01-BOUNDARY-001":
    fail("wrong boundary identity")
if b.get("target_release")!="CDX 1.0":
    fail("wrong target release")
if b.get("state")!="FROZEN_FOR_CLOSURE":
    fail("CDX 1.0 boundary is not frozen")

ids=b.get("canonical_identities",{})
expected_ids={
    "system":"CDX-SYS-001",
    "law":"CDX-LAW-001",
    "runtime_contract":"CDX-RUNTIME-001",
    "estate_anchor_standard":"CDX-GOV-ANCHOR-001",
    "scientific_evidence_authority":"CDX-EVID-001",
    "short_name":"CDX",
    "name_derivation":"Code of Conduct + Excellence",
}
if ids!=expected_ids:
    fail("canonical identity set changed from RC-01 baseline")

topology=b.get("frozen_constitutional_topology",{})
section_markers=re.findall(r'<!-- cdx:section id="([^"]+)" auditability="([^"]+)" -->',law)
principles=re.findall(r'^## Principle [IVX]+ — ',law,flags=re.MULTILINE)
if topology.get("law_sections")!=131:
    fail(f"boundary law section baseline changed: {topology.get('law_sections')} != 131")
if len(section_markers)!=131:
    fail(f"law section count changed: {len(section_markers)} != 131")
if len(principles)!=7 or topology.get("foundational_principles")!=7:
    fail(f"Foundational Principle topology changed: observed={len(principles)}")

entries=bindings.get("sections",[])
full=[x for x in entries if x.get("auditability")=="FULLY_AUTOMATABLE"]
review=[x for x in entries if x.get("auditability")!="FULLY_AUTOMATABLE"]
if len(full)!=69 or topology.get("fully_automatable_sections")!=69:
    fail(f"FULLY_AUTOMATABLE topology changed: {len(full)}")
if len(review)!=62 or topology.get("review_governed_sections")!=62:
    fail(f"review-governed topology changed: {len(review)}")

required_closure={"CDX-WP03","CDX-WP04","CDX-WP05","CDX-WP06","CDX-WP07"}
observed_closure={x.get("wp") for x in b.get("closure_obligations",[])}
if observed_closure!=required_closure:
    fail(f"closure WP set drift: {sorted(observed_closure)}")

required_deferred={"CDX-WP08","CDX-WP09","CDX-WP10","CDX-WP11","CDX-WP12","CDX-WP13","CDX-WP14"}
observed_deferred={x.get("wp") for x in b.get("explicitly_not_core_1_0_execution",[])}
if observed_deferred!=required_deferred:
    fail(f"deferred estate WP set drift: {sorted(observed_deferred)}")

allowed=set(b.get("in_scope_core_domains",[]))
actual={p.name for p in Path(".").iterdir() if p.is_dir() and p.name!=".git"}
unexpected=sorted(actual-allowed)
if unexpected:
    fail("new top-level domain(s) outside frozen CDX 1.0 boundary: "+", ".join(unexpected))

if b.get("active_exceptions"):
    for exc in b["active_exceptions"]:
        if not isinstance(exc,dict) or not exc.get("exception_id") or exc.get("human_decision")!="APPROVED":
            fail("active boundary exception lacks explicit human approval")

print("PASS: CDX 1.0 core boundary is FROZEN_FOR_CLOSURE")
print(f"PASS: constitutional topology 7 principles / {len(section_markers)} §§ / {len(full)} automatable / {len(review)} review-governed")
print("PASS: canonical identity set unchanged")
print("PASS: no unexpected top-level first-class domain detected")
print("PASS: WP03-WP07 closure and WP08-WP14 estate execution remain separated")
