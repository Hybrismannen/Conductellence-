#!/usr/bin/env python3
"""AUD-CDX-RUNTIME-DISTRIBUTION-001 — WP06 contract/package consistency."""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(".")
ENGINE=ROOT/"POLICY/engine.py"
DIST=ROOT/"DISTRIBUTION/conductellence-runtime.py"
POLICY=ROOT/"POLICY/control-registry.json"
DIST_POLICY=ROOT/"DISTRIBUTION/conductellence-policy.json"
SPETL=ROOT/"SPETL/spetl.py"
CONTRACT=ROOT/"RUNTIME-INTEGRATION/CDX-RUNTIME-001.json"
PACKAGE=ROOT/"DISTRIBUTION/releases/1.0.0-rc1/manifest.json"
BUILDER=ROOT/"DISTRIBUTION/build_release_package.py"

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (ENGINE,DIST,POLICY,DIST_POLICY,SPETL,CONTRACT,PACKAGE,BUILDER):
    if not p.exists(): fail(f"missing {p}")

if POLICY.read_bytes()!=DIST_POLICY.read_bytes():
    fail("distribution policy differs from canonical policy registry")

engine_text=ENGINE.read_text(encoding="utf-8")
if "SPETL/ledger.py" in engine_text:
    fail("policy engine still references removed legacy SPETL/ledger.py")
if 'SPETL=Path("SPETL/spetl.py")' not in engine_text:
    fail("policy engine is not pinned to canonical SPETL v1.1 module")

contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
if contract.get("contract_id")!="CDX-RUNTIME-001" or contract.get("contract_version")!="1.0.0":
    fail("runtime contract identity/version invalid")
if contract.get("status")!="FROZEN_RELEASE_CANDIDATE":
    fail("runtime contract is not frozen release candidate")
if contract.get("repository_binding",{}).get("anchor_path")!=".cdx/anchor.json":
    fail("runtime contract does not require canonical anchor")
if contract.get("repository_binding",{}).get("legacy_security_manifest_satisfies_canonical_binding") is not False:
    fail("legacy manifest incorrectly satisfies canonical runtime binding")
if contract.get("evidence",{}).get("event_schema")!="cdx.spetl.event/1.1":
    fail("runtime contract not aligned to SPETL v1.1")

package=json.loads(PACKAGE.read_text(encoding="utf-8"))
if package.get("package_id")!="CDX-DIST-1.0.0-RC1":
    fail("unexpected distribution candidate package id")
if package.get("status")!="RELEASE_CANDIDATE_NOT_RELEASED" or package.get("release_authorized") is not False:
    fail("WP06 package must remain an unreleased candidate")
if package.get("runtime_contract_id")!="CDX-RUNTIME-001" or package.get("evidence_schema_version")!="1.1":
    fail("package identity does not match runtime/evidence contract")
if sorted(package.get("release_gate",{}).get("required_core_blockers_closed",[]))!=sorted([
    "CDX-BLOCK-REPO-PROTECTION-001","CDX-BLOCK-EVIDENCE-INDEPENDENCE-001"
]):
    fail("package release gate does not preserve both core blockers")

proc=subprocess.run([sys.executable,str(BUILDER),"--verify-only"],text=True,capture_output=True)
if proc.returncode!=0:
    print(proc.stdout);print(proc.stderr,file=sys.stderr);fail("distribution package blob verification failed")

# Canonical engine must emit a v1.1 event.
spec=importlib.util.spec_from_file_location("engine",ENGINE)
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
sp_spec=importlib.util.spec_from_file_location("spetl",SPETL)
spetl=importlib.util.module_from_spec(sp_spec);sp_spec.loader.exec_module(spetl)

ctx={
    "surface":"AUTHORITY",
    "actor_id":"CDX-AUDIT-ACTOR",
    "subject_ref":"SUBJECT:PSEUDONYMOUS-001",
    "action":"TEST_EFFECT",
    "resource_id":"RESOURCE:FIXTURE",
    "authority_ref":"HUM-1",
    "mandate_ref":"M-1",
    "correlation_id":"CORR-WP06-1",
    "causation_id":"ROOT",
    "run_id":"RUN-WP06-1",
    "trace_ref":"TRACE-WP06-1",
    "reviewer_ref":None,
    "attempted_effect":{"surface":"AUTHORITY","operation":"TEST_EFFECT","target_ref":"RESOURCE:FIXTURE"},
    "data_minimization":{"personal_data_present":False,"redacted_fields":[],"rationale":"Synthetic WP06 audit fixture."},
    "evidence_refs":[]
}
result=engine.evaluate(ctx)
with tempfile.TemporaryDirectory() as td:
    ledger=Path(td)/"canonical.jsonl"
    event=engine.emit_spetl(ledger,ctx,result)
    if event.get("schema_version")!="1.1": fail("canonical engine emitted non-v1.1 SPETL")
    ok,count,error=spetl.verify(ledger)
    if not ok or count!=1: fail("canonical engine SPETL failed verification: "+str(error))

# Portable distribution must execute with only its declared package artifacts.
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    (td/".security").mkdir()
    (td/".cdx").mkdir()
    shutil.copy2(DIST_POLICY,td/".security/conductellence-policy.json")
    shutil.copy2(SPETL,td/".security/conductellence-spetl.py")

    anchor=json.loads((ROOT/"DISTRIBUTION/cdx-anchor.template.json").read_text(encoding="utf-8"))
    anchor["governed_surface"]["identity"]="AUDIT/CONSUMER"
    anchor["governed_surface"]["repository"]="AUDIT/CONSUMER"
    anchor["governed_surface"]["system_id"]="AUDIT-SYS"
    anchor["policy_pin"]={"ref_type":"POLICY_DIGEST","ref":"sha256:placeholder","digest":None}
    # Fill exact digest using the portable runtime helper after import in subprocess context.
    (td/".cdx/anchor.json").write_text(json.dumps(anchor,indent=2)+"\n",encoding="utf-8")

    context=td/"context.json"
    context.write_text(json.dumps(ctx),encoding="utf-8")
    ledger=td/"events.jsonl"
    runtime_abs=str(DIST.resolve())

    # Self-test all 69 controls.
    proc=subprocess.run([sys.executable,runtime_abs,"--selftest"],cwd=td,text=True,capture_output=True)
    if proc.returncode!=0 or "PASS: 69-control" not in proc.stdout:
        print(proc.stdout);print(proc.stderr,file=sys.stderr);fail("portable runtime selftest failed")

    # Compute portable policy digest and update anchor.
    digest="sha256:"+__import__("hashlib").sha256((td/".security/conductellence-policy.json").read_bytes()).hexdigest()
    anchor["policy_pin"]={"ref_type":"POLICY_DIGEST","ref":digest,"digest":digest}
    (td/".cdx/anchor.json").write_text(json.dumps(anchor,indent=2)+"\n",encoding="utf-8")
    proc=subprocess.run([sys.executable,runtime_abs,"--binding-check"],cwd=td,text=True,capture_output=True)
    if proc.returncode!=0: print(proc.stdout);print(proc.stderr,file=sys.stderr);fail("canonical anchor binding check failed")

    # Allow path emits v1.1 decision evidence.
    proc=subprocess.run([sys.executable,runtime_abs,"--context",str(context),"--ledger",str(ledger)],cwd=td,text=True,capture_output=True)
    if proc.returncode!=0: print(proc.stdout);print(proc.stderr,file=sys.stderr);fail("portable allow decision failed")
    data=json.loads(proc.stdout)
    if data.get("decision")!="ALLOW": fail("portable allow path not ALLOW")
    ok,count,error=spetl.verify(ledger)
    if not ok or count!=1: fail("portable allow evidence invalid: "+str(error))

    # Policy unavailable path must SECURITY_STOP and still emit evidence.
    (td/".security/conductellence-policy.json").unlink()
    unavailable=td/"unavailable.jsonl"
    proc=subprocess.run([sys.executable,runtime_abs,"--context",str(context),"--ledger",str(unavailable)],cwd=td,text=True,capture_output=True)
    if proc.returncode!=0: print(proc.stdout);print(proc.stderr,file=sys.stderr);fail("portable policy-unavailable path failed")
    data=json.loads(proc.stdout)
    if data.get("decision")!="SECURITY_STOP": fail("policy unavailable did not SECURITY_STOP")
    ok,count,error=spetl.verify(unavailable)
    if not ok or count!=1: fail("policy-unavailable evidence invalid: "+str(error))
    row=json.loads(unavailable.read_text(encoding="utf-8").splitlines()[0])
    if row.get("policy_digest")!="UNAVAILABLE" or row.get("effect_status")!="BLOCKED":
        fail("policy-unavailable evidence does not prove blocked effect")

print("PASS: canonical and portable runtime emit SPETL v1.1")
print("PASS: distribution policy exactly matches canonical policy")
print("PASS: canonical .cdx anchor required; legacy manifest is not canonical binding")
print("PASS: portable runtime allow and policy-unavailable paths are fail-closed/evidenced")

print("PASS: CDX-DIST-1.0.0-RC1 artifact blob set is pinned and reproducible")
