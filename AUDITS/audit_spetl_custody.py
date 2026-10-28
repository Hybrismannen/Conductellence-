#!/usr/bin/env python3
from pathlib import Path
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

if policy.get("custody_id")!="CDX-CUSTODY-001": fail("wrong long-lived custody id")
trust=policy.get("trust_model",{})
if trust.get("source_authentication")!="GITHUB_ACTIONS_OIDC": fail("Vercel sender auth is not GitHub OIDC")
if trust.get("storage_authentication")!="VERCEL_PROJECT_BLOB_BINDING": fail("Vercel storage binding semantics are inaccurate")
if trust.get("runtime_has_storage_admin_credential") is not False: fail("runtime may not hold storage admin credentials")
if trust.get("runtime_has_delete_credential") is not False: fail("runtime may not hold deletion credentials")
writes=policy.get("write_semantics",{})
if writes.get("append_only_service") is not True or writes.get("allow_overwrite") is not False:
    fail("long-lived custody service is not append-only/non-overwriting")
if writes.get("delete_endpoint_exposed") is not False: fail("delete endpoint must not be exposed")
if policy.get("retention_and_rights",{}).get("deletion_mode")!="GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION":
    fail("retention/deletion governance missing")

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
    "IMMUTABLE_ACTIONS_ARTIFACT_DIGEST","GITHUB_WORKFLOW_RUN_PROVENANCE"
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

service_files=[
    ROOT/"SPETL/custody-service/api/v1/evidence.mjs",
    ROOT/"SPETL/custody-service/api/v1/verify.mjs",
    ROOT/"SPETL/custody-service/api/health.mjs",
    ROOT/"SPETL/custody-service/lib/auth.mjs",
    ROOT/"SPETL/custody-service/lib/validate.mjs",
    ROOT/"SPETL/custody-service/package.json"
]
for p in service_files:
    if not p.exists(): fail(f"missing custody service file {p}")
service_text="\n".join(p.read_text(encoding="utf-8") for p in service_files)
if "allowOverwrite: false" not in service_text: fail("Vercel service does not visibly fail closed on overwrite")
if any(token in service_text for token in [" del(", "deleteBlob", "allowOverwrite: true"]):
    fail("custody implementation exposes destructive/overwrite semantics")

result=subprocess.run(["node","--test","SPETL/custody-service/test/validation.test.mjs"],capture_output=True,text=True)
if result.returncode!=0:
    print(result.stdout)
    print(result.stderr,file=sys.stderr)
    fail("custody service contract tests failed")

with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    bundle=td/"evidence-bundle.json"
    cmd=[
        sys.executable,"AUDITS/generate_spetl_reference_bundle.py",
        "--output",str(bundle),
        "--source-commit","1"*40,
        "--workflow-run-id","101",
        "--workflow-run-attempt","1"
    ]
    result=subprocess.run(cmd,capture_output=True,text=True)
    if result.returncode!=0:
        print(result.stdout); print(result.stderr,file=sys.stderr)
        fail("reference evidence generator failed")

    package=td/"custody-package"
    cmd=[
        sys.executable,"SPETL/custody/gha_custody.py","receive",
        str(bundle),str(package),
        "--expected-source-commit","1"*40,
        "--expected-producer-run-id","101",
        "--custody-run-id","202",
        "--custody-run-attempt","1"
    ]
    result=subprocess.run(cmd,capture_output=True,text=True)
    if result.returncode!=0:
        print(result.stdout); print(result.stderr,file=sys.stderr)
        fail("reference custody receive interface failed")

    report=td/"verification-report.json"
    cmd=[
        sys.executable,"SPETL/custody/gha_custody.py","verify",
        str(package),
        "--expected-custody-run-id","202",
        "--report",str(report),
        "--verifier-run-id","303",
        "--verifier-run-attempt","1"
    ]
    result=subprocess.run(cmd,capture_output=True,text=True)
    if result.returncode!=0 or not report.exists():
        print(result.stdout); print(result.stderr,file=sys.stderr)
        fail("reference custody read/verify interface failed")

    wrong=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","verify",str(package),
        "--expected-custody-run-id","999","--report",str(td/"bad-report.json"),
        "--verifier-run-id","304","--verifier-run-attempt","1"
    ],capture_output=True,text=True)
    if wrong.returncode==0:
        fail("wrong custody-run provenance was accepted")

    (package/"evidence-bundle.json").unlink()
    lost=subprocess.run([
        sys.executable,"SPETL/custody/gha_custody.py","verify",str(package),
        "--expected-custody-run-id","202","--report",str(td/"lost-report.json"),
        "--verifier-run-id","305","--verifier-run-attempt","1"
    ],capture_output=True,text=True)
    if lost.returncode==0 or "EVIDENCE_LOSS" not in lost.stdout:
        fail("withheld/lost custody evidence was not detected")

ind=preserve.get("independent_preservation",{})
reference=deploy.get("profiles",{}).get("github_actions_reference",{})
required_tests={
    "allow","deny","policy_unavailable","denied_write","invalid_event","tamper",
    "withheld_or_loss","different_identity","forged_authority","write_read_verify_provenance"
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
print("PASS: canonical SPETL reference custody is separate-workflow, fail-closed and credential-separated")
print("PASS: reference write/read/verify and loss/provenance negative interfaces")
print("PASS: long-lived Vercel custody service contract remains append-only and credential-separated")
print("INFO: custody deployment state =",deploy.get("state"))
