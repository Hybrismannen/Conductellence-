#!/usr/bin/env python3
from pathlib import Path
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile

ROOT=Path(".")
POLICY=ROOT/"SPETL/custody/custody-policy.json"
PROFILE=ROOT/"SPETL/custody/github-actions-reference-profile.json"
DEPLOY=ROOT/"SPETL/custody/deployment-state.json"
PRESERVE=ROOT/"SPETL/evidence-preservation-state.json"
SYSTEM=ROOT/"GOVERNANCE/system-state.json"
APPROVAL=ROOT/"GOVERNANCE/orders/CDX-EVIDENCE-CUSTODY-APPROVAL-001.json"

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (POLICY,PROFILE,DEPLOY,PRESERVE,SYSTEM,APPROVAL):
    if not p.exists(): fail(f"missing {p}")

policy=json.loads(POLICY.read_text(encoding="utf-8"))
profile=json.loads(PROFILE.read_text(encoding="utf-8"))
deploy=json.loads(DEPLOY.read_text(encoding="utf-8"))
preserve=json.loads(PRESERVE.read_text(encoding="utf-8"))
system=json.loads(SYSTEM.read_text(encoding="utf-8"))
approval=json.loads(APPROVAL.read_text(encoding="utf-8"))

if approval.get("authority")!="HUMAN_SOVEREIGN_AUTHORITY":
    fail("custody principal lacks human approval")
if approval.get("reference_profile",{}).get("custody_id")!="CDX-CUSTODY-GHA-001":
    fail("reference custody profile not approved")

# Existing long-lived Vercel target remains valid but may stay externally blocked.
if policy.get("custody_id")!="CDX-CUSTODY-001": fail("wrong long-lived custody id")
trust=policy.get("trust_model",{})
if trust.get("source_authentication")!="GITHUB_ACTIONS_OIDC":
    fail("long-lived custody sender authentication drift")
if trust.get("runtime_has_storage_admin_credential") is not False:
    fail("runtime may not hold storage admin credentials")
if trust.get("runtime_has_delete_credential") is not False:
    fail("runtime may not hold deletion credentials")
writes=policy.get("write_semantics",{})
if writes.get("append_only_service") is not True or writes.get("allow_overwrite") is not False:
    fail("long-lived custody service is not append-only/non-overwriting")
if writes.get("delete_endpoint_exposed") is not False:
    fail("delete endpoint must not be exposed")
if policy.get("retention_and_rights",{}).get("deletion_mode")!="GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION":
    fail("retention/deletion governance missing")

service_files=[
    ROOT/"SPETL/custody-service/api/v1/evidence.mjs",
    ROOT/"SPETL/custody-service/api/v1/verify.mjs",
    ROOT/"SPETL/custody-service/api/health.mjs",
    ROOT/"SPETL/custody-service/lib/auth.mjs",
    ROOT/"SPETL/custody-service/lib/validate.mjs",
    ROOT/"SPETL/custody-service/package.json",
]
for p in service_files:
    if not p.exists(): fail(f"missing custody service file {p}")
service_text="\n".join(p.read_text(encoding="utf-8") for p in service_files)
if "allowOverwrite: false" not in service_text:
    fail("long-lived service does not visibly fail closed on overwrite")
if any(token in service_text for token in [" del(", "deleteBlob", "allowOverwrite: true"]):
    fail("custody implementation exposes destructive/overwrite semantics")

node=subprocess.run(["node","--test","SPETL/custody-service/test/validation.test.mjs"],capture_output=True,text=True)
if node.returncode!=0:
    print(node.stdout); print(node.stderr,file=sys.stderr)
    fail("custody service contract tests failed")

# Independent reference custody trust separation.
if profile.get("custody_id")!="CDX-CUSTODY-GHA-001":
    fail("wrong reference custody id")
sep=profile.get("trust_separation",{})
if sep.get("separate_workflow_run_required") is not True:
    fail("reference custody is not separated into workflow runs")
if sep.get("producer_has_custodian_credentials") is not False:
    fail("producer may not have custodian credentials")
if sep.get("custodian_executes_producer_code") is not False:
    fail("custodian may not execute producer-supplied code")
if sep.get("repository_write_permission") is not False:
    fail("custody reference workflows may not write repository contents")
if profile.get("retention",{}).get("days")!=90:
    fail("reference custody retention mismatch")
required_chain={
    "SPETL_EVENT_HASH_CHAIN","CUSTODY_BUNDLE_SHA256","CUSTODY_RECEIPT_SHA256",
    "IMMUTABLE_ACTIONS_ARTIFACT_DIGEST","GITHUB_WORKFLOW_RUN_PROVENANCE",
}
if not required_chain.issubset(set(profile.get("integrity_chain",[]))):
    fail("reference integrity chain incomplete")

workflow_paths=[
    ROOT/".github/workflows/spetl-evidence-producer.yml",
    ROOT/".github/workflows/spetl-independent-custodian.yml",
    ROOT/".github/workflows/spetl-custody-verifier.yml",
]
for p in workflow_paths:
    if not p.exists(): fail(f"missing custody workflow {p}")
producer_text=workflow_paths[0].read_text(encoding="utf-8")
custodian_text=workflow_paths[1].read_text(encoding="utf-8")
verifier_text=workflow_paths[2].read_text(encoding="utf-8")
if "contents: write" in producer_text+custodian_text+verifier_text:
    fail("custody workflow unexpectedly has repository write permission")
if "workflow_run:" not in custodian_text or 'workflows: ["SPETL Evidence Producer"]' not in custodian_text:
    fail("custodian is not a separate workflow_run consumer")
if "workflow_run:" not in verifier_text or 'workflows: ["SPETL Independent Custodian"]' not in verifier_text:
    fail("verifier is not a separate workflow_run consumer")
if "ref: main" not in custodian_text or "ref: main" not in verifier_text:
    fail("custodian/verifier do not pin trusted main code")
if producer_text.count("retention-days: 90")!=1 or custodian_text.count("retention-days: 90")!=1 or verifier_text.count("retention-days: 90")!=1:
    fail("reference artifacts do not carry explicit 90-day retention")

# Local contract proof for the same interfaces that execute cross-workflow.
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    bundle=td/"evidence-bundle.json"
    p=subprocess.run([
        sys.executable,"AUDITS/generate_spetl_reference_bundle.py",
        "--output",str(bundle),
        "--source-commit","1"*40,
        "--workflow-run-id","101",
        "--workflow-run-attempt","1",
    ],capture_output=True,text=True)
    if p.returncode!=0:
        print(p.stdout); print(p.stderr,file=sys.stderr)
        fail("reference evidence generator failed")

    package=td/"custody-package"
    p=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","receive",
        str(bundle),str(package),
        "--expected-source-commit","1"*40,
        "--expected-producer-run-id","101",
        "--custody-run-id","202",
        "--custody-run-attempt","1",
    ],capture_output=True,text=True)
    if p.returncode!=0:
        print(p.stdout); print(p.stderr,file=sys.stderr)
        fail("reference custody receive interface failed")

    report=td/"verification-report.json"
    p=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","verify",str(package),
        "--expected-custody-run-id","202",
        "--report",str(report),
        "--verifier-run-id","303",
        "--verifier-run-attempt","1",
    ],capture_output=True,text=True)
    if p.returncode!=0 or not report.exists():
        print(p.stdout); print(p.stderr,file=sys.stderr)
        fail("reference custody read/verify interface failed")

    wrong=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","verify",str(package),
        "--expected-custody-run-id","999",
        "--report",str(td/"wrong.json"),
        "--verifier-run-id","304",
        "--verifier-run-attempt","1",
    ],capture_output=True,text=True)
    if wrong.returncode==0:
        fail("wrong custody-run provenance was accepted")

    # The independent custodian must reject a DENY that claims an effect was permitted,
    # even if an attacker recomputes the local hash chain and outer bundle hash.
    sp_spec=importlib.util.spec_from_file_location("spetl_wp04",ROOT/"SPETL/spetl.py")
    spetl=importlib.util.module_from_spec(sp_spec); sp_spec.loader.exec_module(spetl)
    original=json.loads(bundle.read_text(encoding="utf-8"))
    contradictory=copy.deepcopy(original)
    contradictory["events"][1]["effect_status"]="PERMITTED"
    previous=None
    for event in contradictory["events"]:
        event["previous_hash"]=previous
        event["event_hash"]=spetl.sha256_obj({k:v for k,v in event.items() if k!="event_hash"})
        previous=event["event_hash"]
    contradictory["bundle_hash"]=spetl.sha256_obj({k:v for k,v in contradictory.items() if k!="bundle_hash"})
    denied_bundle=td/"denied-write.json"
    denied_bundle.write_text(json.dumps(contradictory),encoding="utf-8")
    denied=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","receive",
        str(denied_bundle),str(td/"denied-package"),
        "--expected-source-commit","1"*40,
        "--expected-producer-run-id","101",
        "--custody-run-id","203",
        "--custody-run-attempt","1",
    ],capture_output=True,text=True)
    if denied.returncode==0 or "restrictive decision cannot report PERMITTED effect" not in denied.stdout:
        fail("contradictory denied-write evidence was accepted")

    # Reference custody is minimized: direct personal-data payloads are refused.
    personal=copy.deepcopy(original)
    personal["events"][0]["data_minimization"]["personal_data_present"]=True
    previous=None
    for event in personal["events"]:
        event["previous_hash"]=previous
        event["event_hash"]=spetl.sha256_obj({k:v for k,v in event.items() if k!="event_hash"})
        previous=event["event_hash"]
    personal["bundle_hash"]=spetl.sha256_obj({k:v for k,v in personal.items() if k!="bundle_hash"})
    personal_bundle=td/"personal-data.json"
    personal_bundle.write_text(json.dumps(personal),encoding="utf-8")
    personal_result=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","receive",
        str(personal_bundle),str(td/"personal-package"),
        "--expected-source-commit","1"*40,
        "--expected-producer-run-id","101",
        "--custody-run-id","204",
        "--custody-run-attempt","1",
    ],capture_output=True,text=True)
    if personal_result.returncode==0 or "direct personal data is prohibited" not in personal_result.stdout:
        fail("reference custody accepted direct personal-data evidence")

    (package/"evidence-bundle.json").unlink()
    lost=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","verify",str(package),
        "--expected-custody-run-id","202",
        "--report",str(td/"lost.json"),
        "--verifier-run-id","305",
        "--verifier-run-attempt","1",
    ],capture_output=True,text=True)
    if lost.returncode==0 or "EVIDENCE_LOSS" not in lost.stdout:
        fail("withheld/lost custody evidence was not detected")

ind=preserve.get("independent_preservation",{})
reference=deploy.get("profiles",{}).get("github_actions_reference",{})
required_tests={
    "allow","deny","policy_unavailable","denied_write","invalid_event","tamper",
    "withheld_or_loss","different_identity","forged_authority","write_read_verify_provenance",
}
if deploy.get("state")=="VERIFIED_REFERENCE_CUSTODY":
    observed=deploy.get("external_verification",{}).get("tests",{})
    if deploy.get("external_verification",{}).get("approved_profile")!="CDX-CUSTODY-GHA-001":
        fail("verified state does not identify approved reference custody profile")
    if not required_tests.issubset({k for k,v in observed.items() if v=="PASS"}):
        fail("verified custody state lacks complete observed test matrix")
    if reference.get("state")!="VERIFIED" or reference.get("satisfies_enforcing_requirement") is not True:
        fail("verified deployment is not reflected in reference profile")
    if ind.get("state")!="VERIFIED" or ind.get("satisfies_enforcing_requirement") is not True:
        fail("verified deployment not reflected in evidence-preservation state")
    if "CDX-BLOCK-EVIDENCE-INDEPENDENCE-001" in system.get("core_release_blockers",[]):
        fail("verified evidence-independence blocker still present in system state")
else:
    if ind.get("satisfies_enforcing_requirement") is True:
        fail("unobserved custody cannot satisfy enforcing requirement")
    if "CDX-BLOCK-EVIDENCE-INDEPENDENCE-001" not in system.get("core_release_blockers",[]):
        fail("evidence-independence blocker removed before observed verification")

print("PASS: independent custody principals are explicitly human-approved")
print("PASS: reference custody is separate-workflow, read-only and credential-separated")
print("PASS: reference custody local write/read/verify and provenance/loss negatives")
print("PASS: long-lived custody service remains append-only and credential-separated")
print("INFO: custody deployment state =",deploy.get("state"))
