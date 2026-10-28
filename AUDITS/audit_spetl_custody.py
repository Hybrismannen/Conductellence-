#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(".")
POLICY=ROOT/"SPETL/custody/custody-policy.json"
DEPLOY=ROOT/"SPETL/custody/deployment-state.json"
PRESERVE=ROOT/"SPETL/evidence-preservation-state.json"
SYSTEM=ROOT/"GOVERNANCE/system-state.json"

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (POLICY,DEPLOY,PRESERVE,SYSTEM):
    if not p.exists(): fail(f"missing {p}")

policy=json.loads(POLICY.read_text(encoding="utf-8"))
deploy=json.loads(DEPLOY.read_text(encoding="utf-8"))
preserve=json.loads(PRESERVE.read_text(encoding="utf-8"))
system=json.loads(SYSTEM.read_text(encoding="utf-8"))

if policy.get("custody_id")!="CDX-CUSTODY-001": fail("wrong custody id")
trust=policy.get("trust_model",{})
if trust.get("source_authentication")!="GITHUB_ACTIONS_OIDC": fail("sender auth is not short-lived GitHub OIDC")
if trust.get("storage_authentication")!="VERCEL_OIDC": fail("storage auth is not Vercel OIDC")
if trust.get("runtime_has_storage_admin_credential") is not False: fail("runtime may not hold storage admin credentials")
if trust.get("runtime_has_delete_credential") is not False: fail("runtime may not hold deletion credentials")
writes=policy.get("write_semantics",{})
if writes.get("append_only_service") is not True or writes.get("allow_overwrite") is not False:
    fail("custody service is not append-only/non-overwriting")
if writes.get("delete_endpoint_exposed") is not False: fail("delete endpoint must not be exposed")
if policy.get("retention_and_rights",{}).get("deletion_mode")!="GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION":
    fail("retention/deletion governance missing")

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
if "allowOverwrite: false" not in service_text: fail("service does not visibly fail closed on overwrite")
if any(token in service_text for token in [" del(", "deleteBlob", "allowOverwrite: true"]):
    fail("custody implementation exposes destructive/overwrite semantics")

result=subprocess.run(["node","--test","SPETL/custody-service/test/validation.test.mjs"],capture_output=True,text=True)
if result.returncode!=0:
    print(result.stdout)
    print(result.stderr,file=sys.stderr)
    fail("custody service contract tests failed")

ind=preserve.get("independent_preservation",{})
if deploy.get("state")=="VERIFIED_EXTERNAL":
    required_tests={"allow","deny","policy_unavailable","denied_write","invalid_event","tamper","withheld_or_loss","different_identity","forged_authority"}
    observed=deploy.get("external_verification",{}).get("tests",{})
    if not required_tests.issubset({k for k,v in observed.items() if v=="PASS"}):
        fail("external custody state claims VERIFIED without all tests")
    if ind.get("state")!="VERIFIED" or ind.get("satisfies_enforcing_requirement") is not True:
        fail("verified deployment not reflected in preservation state")
else:
    if ind.get("satisfies_enforcing_requirement") is True:
        fail("unverified custody cannot satisfy enforcing requirement")
    if "CDX-BLOCK-EVIDENCE-INDEPENDENCE-001" not in system.get("core_release_blockers",[]):
        fail("evidence-independence blocker removed before external verification")

print("PASS: independent custody contract is fail-closed and credential-separated")
print("PASS: custody service local validation/identity negative tests")
print("INFO: custody deployment state =",deploy.get("state"))
