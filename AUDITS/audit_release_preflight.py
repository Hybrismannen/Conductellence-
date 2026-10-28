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
expected={"CDX-BLOCK-REPO-PROTECTION-001","CDX-BLOCK-EVIDENCE-INDEPENDENCE-001"}
if blockers!=expected: fail(f"unexpected core release blocker set: {sorted(blockers)}")

if prot.get("satisfies_enforcing_requirement") is not False or prot.get("blocker_id") not in blockers:
    fail("repository protection blocker state inconsistent")
if pres.get("independent_preservation",{}).get("satisfies_enforcing_requirement") is not False:
    fail("evidence preservation incorrectly satisfies release gate")
if custody.get("satisfies_enforcing_requirement") is not False:
    fail("custody incorrectly satisfies release gate")

if state.get("release_state")!="PRE_RELEASE": fail("blocked preflight must remain PRE_RELEASE")
if state.get("enforcement_state")!="BOOTSTRAP": fail("blocked preflight must remain BOOTSTRAP")
if pre.get("decision")!="BLOCKED_EXTERNAL_GATES" or pre.get("release_authorized") is not False:
    fail("preflight must remain blocked while core blockers are open")
if order.get("state")!="PENDING_BLOCKER_CLOSURE" or order.get("decision") is not None:
    fail("release order must remain pending blocker closure")

print("PASS: all internal CDX 1.0 release-candidate conditions are coherent")
print("PASS: exact two core external blockers remain and release is fail-closed")
print("PASS: release_state PRE_RELEASE / enforcement_state BOOTSTRAP preserved")
print("INFO: final release decision is not yet requestable")
