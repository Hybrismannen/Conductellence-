#!/usr/bin/env python3
"""AUD-CDX-RELEASE-PREFLIGHT-001 — fail-closed release preflight."""
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(".")
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

state=load("GOVERNANCE/system-state.json")
pre=load("GOVERNANCE/release-preflight-state.json")
order=load("GOVERNANCE/orders/CDX-RELEASE-1.0.0.json")
prot=load("GOVERNANCE/repository-protection-state.json")
pres=load("SPETL/evidence-preservation-state.json")
custody=load("SPETL/custody/deployment-state.json")
boundary=load("GOVERNANCE/release-boundary-v1.json")
adoption=load("GOVERNANCE/constitutional-adoption-state.json")
package=load("DISTRIBUTION/releases/1.0.0-rc1/manifest.json")
runtime=load("RUNTIME-INTEGRATION/CDX-RUNTIME-001.json")

if state.get("constitutional_state")!="ADOPTED": fail("constitutional state not ADOPTED")
if adoption.get("current_constitutional_state")!="ADOPTED": fail("adoption record not ADOPTED")
if boundary.get("state")!="FROZEN_FOR_CLOSURE" or boundary.get("active_exceptions"): fail("release boundary not clean/frozen")
if runtime.get("contract_id")!="CDX-RUNTIME-001" or runtime.get("contract_version")!="1.0.0": fail("runtime contract not 1.0.0")
if package.get("package_id")!="CDX-DIST-1.0.0-RC1": fail("release candidate package missing")
if package.get("status")!="RELEASE_CANDIDATE_NOT_RELEASED" or package.get("release_authorized") is not False:
    fail("candidate package has been prematurely released")

builder=subprocess.run([sys.executable,"DISTRIBUTION/build_release_package.py","--verify-only"],capture_output=True,text=True)
if builder.returncode!=0:
    print(builder.stdout);print(builder.stderr,file=sys.stderr);fail("release candidate artifact verification failed")

blockers=set(state.get("core_release_blockers",[]))
repo_ok=prot.get("satisfies_enforcing_requirement") is True
pres_ok=pres.get("independent_preservation",{}).get("satisfies_enforcing_requirement") is True
custody_ok=custody.get("satisfies_enforcing_requirement") is True
if pres_ok != custody_ok:
    fail("evidence preservation and custody verification states diverge")

expected=set()
if not repo_ok:
    expected.add("CDX-BLOCK-REPO-PROTECTION-001")
if not (pres_ok and custody_ok):
    expected.add("CDX-BLOCK-EVIDENCE-INDEPENDENCE-001")
if blockers!=expected:
    fail(f"core release blocker set does not match live gate state: blockers={sorted(blockers)} expected={sorted(expected)}")

pre_blockers={x.get("blocker_id") for x in pre.get("blocking_core_conditions",[])}
if pre_blockers!=blockers:
    fail(f"release preflight blocker register diverges: {sorted(pre_blockers)} != {sorted(blockers)}")
if set(order.get("blockers",[]))!=blockers:
    fail("pending release order blocker set diverges from canonical state")

if state.get("release_state")!="PRE_RELEASE": fail("preflight must remain PRE_RELEASE before human release decision")
if state.get("enforcement_state")!="BOOTSTRAP": fail("preflight must remain BOOTSTRAP before later enforcement gates")

if blockers:
    if pre.get("decision")!="BLOCKED_EXTERNAL_GATES" or pre.get("release_authorized") is not False:
        fail("preflight must remain blocked while core blockers are open")
    if order.get("state")!="PENDING_BLOCKER_CLOSURE" or order.get("decision") is not None:
        fail("release order must remain pending blocker closure")
else:
    if pre.get("decision")!="READY_FOR_HUMAN_RELEASE_DECISION" or pre.get("release_authorized") is not False:
        fail("zero-blocker preflight must hand off to explicit human release decision")
    if order.get("state")=="READY_FOR_DECISION":
        if order.get("decision") is not None:
            fail("undecided release order has a decision")
    elif order.get("state")=="DECISION_RECORDED_PENDING_PUBLICATION":
        att=load("GOVERNANCE/orders/CDX-RELEASE-1.0.0-SOVEREIGN-ATTESTATION-2026-10-29.json")
        if (order.get("decision")!="RELEASE_1_0_0"
            or order.get("decision_by")!="Hybrismannen"
            or order.get("decision_approval_pr")!=45
            or order.get("decision_attestation_ref")!="GOVERNANCE/orders/CDX-RELEASE-1.0.0-SOVEREIGN-ATTESTATION-2026-10-29.json"
            or att.get("decision")!=order.get("decision")
            or att.get("decision_approval_pr")!=45
            or att.get("recorded_in_canonical_order") is not True
            or att.get("publication_authorized") is not False):
            fail("recorded sovereign decision lacks matching approved attestation")
        if (order.get("release_authorized") is not False
            or order.get("publication_authorized") is not False
            or order.get("publication_state")!="NOT_AUTHORIZED"):
            fail("recorded release decision improperly authorizes publication")
    else:
        fail("unexpected zero-blocker release order state")

print("PASS: all internal CDX 1.0 release-candidate conditions are coherent")
print(f"PASS: live core blocker set derived from verified gate state: {sorted(blockers)}")
print("PASS: release_state PRE_RELEASE / enforcement_state BOOTSTRAP preserved")
print("INFO: human release decision recorded separately from publication authority; publication remains prohibited")
