#!/usr/bin/env python3
"""Audit the CDX constitutional-closure/adoption state.

Audit ID: AUD-CDX-CONSTITUTIONAL-ADOPTION-001
This audit validates constitutional maturity without implying release or enforcement.
"""
from pathlib import Path
import json
import re

def fail(message):
    print("FAIL:", message)
    raise SystemExit(1)

required={
    "law":Path("LAW/CONDUCTELLENCE-ACT.md"),
    "system":Path("GOVERNANCE/system-state.json"),
    "adoption":Path("GOVERNANCE/constitutional-adoption-state.json"),
    "authorization":Path("GOVERNANCE/orders/CDX-CONSTITUTIONAL-AUTHORIZATION-001.json"),
    "boundary":Path("GOVERNANCE/release-boundary-v1.json"),
    "wp01":Path("PROGRAMME/WP01-reconciliation-register.json"),
    "bindings":Path("CONTROL-CATALOGUE/law-bindings.json"),
    "reviews":Path("REVIEW-CATALOGUE/bindings.json"),
    "protection":Path("GOVERNANCE/repository-protection-state.json"),
    "preservation":Path("SPETL/evidence-preservation-state.json"),
}
for name,path in required.items():
    if not path.exists():
        fail(f"missing {name}: {path}")

law=required["law"].read_text(encoding="utf-8")
system=json.loads(required["system"].read_text(encoding="utf-8"))
adoption=json.loads(required["adoption"].read_text(encoding="utf-8"))
authorization=json.loads(required["authorization"].read_text(encoding="utf-8"))
boundary=json.loads(required["boundary"].read_text(encoding="utf-8"))
wp01=json.loads(required["wp01"].read_text(encoding="utf-8"))
bindings=json.loads(required["bindings"].read_text(encoding="utf-8"))
reviews=json.loads(required["reviews"].read_text(encoding="utf-8"))
protection=json.loads(required["protection"].read_text(encoding="utf-8"))
preservation=json.loads(required["preservation"].read_text(encoding="utf-8"))

if adoption.get("adoption_id")!="CDX-CONST-ADOPT-001":
    fail("wrong adoption record")
if adoption.get("law_id")!="CDX-LAW-001" or adoption.get("system_id")!="CDX-SYS-001":
    fail("adoption record identity mismatch")
if authorization.get("authorization_id")!="CDX-CONST-AUTH-001":
    fail("wrong constitutional authorization")
if authorization.get("authority")!="HUMAN_SOVEREIGN_AUTHORITY":
    fail("constitutional transition lacks human sovereign authority")
if authorization.get("final_adoption_authorized_if_conditions_pass") is not True:
    fail("WP03 final adoption was not conditionally authorized")
if authorization.get("authorized_transition_path")!=[
    "FOUNDATIONAL_DRAFT","CONSTITUTIONAL_CANDIDATE","STABLE_CANDIDATE","ADOPTED"
]:
    fail("constitutional transition path drift")

if boundary.get("state")!="FROZEN_FOR_CLOSURE":
    fail("constitutional closure attempted outside frozen RC-01 boundary")
if boundary.get("active_exceptions"):
    fail("constitutional closure has active boundary exception; review required")

if wp01.get("constitutional_conflicts_found")!=0:
    fail("WP01 records unresolved constitutional conflict")

markers=re.findall(r'<!-- cdx:section id="([^"]+)" auditability="([^"]+)" -->',law)
principles=re.findall(r'^## Principle [IVX]+ — ',law,flags=re.MULTILINE)
if len(principles)!=7 or len(markers)!=131:
    fail(f"constitutional topology drift: principles={len(principles)} sections={len(markers)}")

entries=bindings.get("sections",[])
full=[x for x in entries if x.get("auditability")=="FULLY_AUTOMATABLE"]
nonfull=[x for x in entries if x.get("auditability")!="FULLY_AUTOMATABLE"]
if len(entries)!=131 or len(full)!=69 or len(nonfull)!=62:
    fail("law-binding topology does not match frozen 131/69/62 baseline")
if len(reviews.get("bindings",[]))!=62:
    fail("review-governance coverage is not 62/62")

state=adoption.get("current_constitutional_state")
valid={"CONSTITUTIONAL_CANDIDATE","STABLE_CANDIDATE","ADOPTED"}
if state not in valid:
    fail(f"invalid WP03 constitutional state: {state}")
if system.get("constitutional_state")!=state:
    fail("system constitutional state and adoption record diverge")

header={
    "CONSTITUTIONAL_CANDIDATE":"**Status:** CONSTITUTIONAL CANDIDATE",
    "STABLE_CANDIDATE":"**Status:** STABLE CANDIDATE",
    "ADOPTED":"**Status:** ADOPTED",
}[state]
if header not in law[:1200]:
    fail(f"Act header does not match {state}")

if state in {"STABLE_CANDIDATE","ADOPTED"}:
    stable=adoption.get("stable_candidate_basis",{})
    if stable.get("candidate_merge_commit")!="4e238ef93a944cbaa9cf082f39587d8bd02750b8":
        fail("stable/adopted state lacks verified constitutional-candidate merge provenance")
    if stable.get("candidate_gates")!="PASS" or stable.get("scope_change") is not False:
        fail("stable/adopted state lacks clean candidate gate evidence")

if state=="ADOPTED":
    if "**Version:** 1.0.0" not in law[:1200]:
        fail("adopted Act must be constitutional version 1.0.0")
    order=Path("GOVERNANCE/orders/CDX-CONSTITUTIONAL-ADOPTION-001.json")
    if not order.exists():
        fail("adopted state lacks final human adoption order")
    o=json.loads(order.read_text(encoding="utf-8"))
    if o.get("decision")!="ADOPT" or o.get("authority")!="HUMAN_SOVEREIGN_AUTHORITY":
        fail("final adoption order is not valid")
    if o.get("constitutional_version")!="1.0.0":
        fail("final adoption order version mismatch")
    if o.get("effective_condition")!="MERGE_OF_FINAL_ADOPTION_PR_WITH_ALL_REQUIRED_GATES_PASSING":
        fail("final adoption order has unexpected effective condition")
    stable=o.get("evidence",{}).get("candidate_to_stable",{})
    if stable.get("merge_commit")!="9dc5591a0be3cf7b331a658e130dccc0ce373c3d" or stable.get("gates")!="PASS":
        fail("final adoption order lacks stable-candidate gate provenance")
    if adoption.get("final_adoption",{}).get("order_ref")!="GOVERNANCE/orders/CDX-CONSTITUTIONAL-ADOPTION-001.json":
        fail("adoption state does not bind the final adoption order")
else:
    if "**Version:** 0.1.0-bootstrap" not in law[:1200]:
        fail("pre-adoption candidate must retain bootstrap law version")

expected_other={
    "core_runtime_state":"VERIFIED_REFERENCE_RUNTIME",
    "enforcement_state":"BOOTSTRAP",
}
for key,val in expected_other.items():
    if system.get(key)!=val:
        fail(f"constitutional transition improperly changed {key}: {system.get(key)}")

estate_state=system.get("estate_integration_state")
if estate_state not in {"PENDING_RUNTIME_BINDINGS","BINDINGS_IN_PROGRESS"}:
    fail(f"estate integration axis exceeds current governed rollout boundary: {estate_state}")
if estate_state=="BINDINGS_IN_PROGRESS":
    wp11=system.get("wp11_ffos_runtime_binding",{})
    if wp11.get("state")!="IMPLEMENTATION_STAGED_VERIFICATION_BLOCKED":
        fail("BINDINGS_IN_PROGRESS lacks explicit WP11 staged/blocker evidence")
    if wp11.get("production_deployment_state")!="NOT_DEPLOYED":
        fail("WP11 staged state cannot claim production deployment")
    if system.get("consumer_bindings",{}).get("Motherpher/FFOS")!="IMPLEMENTATION_STAGED_VERIFICATION_BLOCKED":
        fail("FFOS consumer binding state does not match WP11 staged state")

release_state=system.get("release_state")
if release_state not in {"PRE_RELEASE","RELEASED"}:
    fail(f"unexpected release state on independent release axis: {release_state}")
if release_state=="RELEASED":
    evidence_path=Path("GOVERNANCE/release/CDX-1.0-PUBLICATION-EVIDENCE-2026-10-29.json")
    order_path=Path("GOVERNANCE/orders/CDX-RELEASE-1.0.0.json")
    if not evidence_path.exists() or not order_path.exists():
        fail("RELEASED state lacks independent publication evidence/order")
    publication=json.loads(evidence_path.read_text(encoding="utf-8"))
    release_order=json.loads(order_path.read_text(encoding="utf-8"))
    if (publication.get("publication_verified") is not True
        or publication.get("release_published") is not True
        or publication.get("tag",{}).get("name")!="1.0.0"
        or release_order.get("state")!="PUBLISHED"
        or release_order.get("publication_state")!="PUBLISHED_VERIFIED"):
        fail("RELEASED state is not supported by verified publication evidence")

core_blockers=set(system.get("core_release_blockers",[]))
estate_blockers=set(system.get("estate_enforcement_blockers",[]))

repo_protected=protection.get("satisfies_enforcing_requirement") is True
evidence_verified=preservation.get("independent_preservation",{}).get("satisfies_enforcing_requirement") is True

expected_core=set()
if not repo_protected:
    expected_core.add("CDX-BLOCK-REPO-PROTECTION-001")
if not evidence_verified:
    expected_core.add("CDX-BLOCK-EVIDENCE-INDEPENDENCE-001")
if core_blockers!=expected_core:
    fail(f"constitutional state sees blocker drift unrelated to verified gate state: {sorted(core_blockers)} != {sorted(expected_core)}")

if system.get("estate_integration_state")!="VERIFIED_RUNTIME_BOUND":
    if "CDX-BLOCK-ESTATE-RUNTIME-001" not in estate_blockers:
        fail("estate-runtime blocker removed before verified estate runtime binding")

print(f"PASS: constitutional state={state}")
print("PASS: explicit HUMAN_SOVEREIGN_AUTHORITY authorization present")
print("PASS: frozen constitutional topology remains 7/131/69/62")
print("PASS: no WP01 constitutional conflict")
print(f"PASS: release axis independently evidenced at {release_state}; enforcement/integration remain separate")
print("PASS: independent blocker state tracks verified external gate state")
