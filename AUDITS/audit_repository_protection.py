#!/usr/bin/env python3
from pathlib import Path
import json

STATE=Path("GOVERNANCE/repository-protection-state.json")
VERIFY=Path("GOVERNANCE/repository-protection-verification.json")
TARGET=Path("GOVERNANCE/repository-protection-target.json")
SYSTEM=Path("GOVERNANCE/system-state.json")
PREFLIGHT=Path("GOVERNANCE/release-preflight-state.json")
ORDER=Path("GOVERNANCE/orders/CDX-RELEASE-1.0.0.json")
CODEOWNERS=Path(".github/CODEOWNERS")
GUARD=Path(".github/workflows/constitutional-mutation-guard.yml")
HUMAN_APPROVAL=Path(".github/workflows/human-sovereign-approval.yml")
MUTATION_POLICY=Path("GOVERNANCE/constitutional-mutation-policy.md")
CHANGE_POLICY=Path("GOVERNANCE/constitutional-change-policy.md")

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (STATE,VERIFY,TARGET,SYSTEM,PREFLIGHT,ORDER,CODEOWNERS,GUARD,HUMAN_APPROVAL,MUTATION_POLICY,CHANGE_POLICY):
    if not p.exists():
        fail(f"missing {p}")

state=json.loads(STATE.read_text())
verify=json.loads(VERIFY.read_text())
target=json.loads(TARGET.read_text())
system=json.loads(SYSTEM.read_text())
preflight=json.loads(PREFLIGHT.read_text())
order=json.loads(ORDER.read_text())

if state.get("schema")!="cdx.repository-protection-state/v1.1":
    fail("unexpected repository-protection state schema")
if verify.get("schema")!="cdx.repository-protection-verification/v1.0":
    fail("unexpected verification schema")
if target.get("target_id")!="CDX-REPO-PROTECT-TARGET-001":
    fail("unexpected target profile")

required_checks={"constitutional-audit","mutation-guard","human-sovereign-approval"}
declared={x.get("context") for x in target.get("required_status_checks",{}).get("checks",[])}
if not required_checks.issubset(declared):
    fail("target profile omitted required constitutional checks")
if target.get("pull_request",{}).get("required") is not True:
    fail("target profile does not require pull request")
approval=target.get("pull_request",{})
if approval.get("human_approval_mode")!="OWNER_COMMENT_STATUS":
    fail("target profile lacks owner-bound human approval mode")
if approval.get("human_approval_context")!="human-sovereign-approval":
    fail("target profile has wrong human approval status context")
if approval.get("human_approval_workflow")!=".github/workflows/human-sovereign-approval.yml":
    fail("target profile has wrong human approval workflow")
if target.get("history_integrity",{}).get("allow_force_pushes") is not False:
    fail("target profile permits force push")
if target.get("history_integrity",{}).get("allow_deletions") is not False:
    fail("target profile permits branch deletion")
if target.get("bypass",{}).get("allow_admin_bypass") is not False:
    fail("target profile permits admin bypass")

codeowners=CODEOWNERS.read_text()
required_owner_paths=[
    "/LAW/","/INTERPRETATION/","/GOVERNANCE/","/CONTROL-CATALOGUE/","/POLICY/",
    "/SPETL/","/SECURITY-TWIN/","/GLOBAL-AUTHORITY-CORPUS/","/LEGAL-REFERENCES/",
    "/LEGAL-RESOLVER/","/REGULATORY-DRIFT/","/EVIDENCE-AUTHORITY/","/REVIEW-CATALOGUE/",
    "/RED-TEAM/","/DISTRIBUTION/","/RUNTIME-INTEGRATION/","/ESTATE-REGISTRY/","/AUDITS/",
    "/.github/CODEOWNERS","/.github/workflows/"
]
missing_owner=[p for p in required_owner_paths if p not in codeowners]
if missing_owner:
    fail("CODEOWNERS coverage drift: "+", ".join(missing_owner))

guard=GUARD.read_text()
if "\\.github/CODEOWNERS$" not in guard or "\\.github/workflows/" not in guard:
    fail("constitutional mutation guard does not protect CODEOWNERS/workflow control paths")

human=HUMAN_APPROVAL.read_text()
for token in ("issue_comment:", "author_association == 'OWNER'", "/cdx-approve", "statuses: write", '"context":"human-sovereign-approval"'):
    if token not in human:
        fail("human-sovereign approval workflow missing required trust binding: "+token)

for policy_path in (MUTATION_POLICY,CHANGE_POLICY):
    policy=policy_path.read_text()
    if ".github/CODEOWNERS" not in policy:
        fail(f"{policy_path} does not protect CODEOWNERS")

verified=state.get("satisfies_enforcing_requirement") is True
criteria=verify.get("criteria",{})
all_required=all(criteria.get(k) is True for k in (
    "pull_request_required",
    "human_approval_required",
    "constitutional_audit_required",
    "mutation_guard_required",
    "force_push_disabled",
    "branch_deletion_disabled",
    "uncontrolled_bypass_absent",
))

if verified:
    if state.get("provisioning_state") not in {"VERIFIED_NATIVE_PROTECTION","VERIFIED_EQUIVALENT_PREMERGE"}:
        fail("protection satisfied without verified platform state")
    if verify.get("state")!="VERIFIED":
        fail("protection satisfied without VERIFIED platform record")
    if verify.get("source")!="GITHUB_PLATFORM_API":
        fail("verified protection lacks independent platform source")
    if verify.get("all_criteria_verified") is not True or not all_required:
        fail("verified protection lacks complete closure criteria")
    platform=verify.get("platform_evidence",{})
    if not (platform.get("branch_protected_flag") is True or platform.get("ruleset_id") or platform.get("protection_rule_id")):
        fail("verified protection lacks platform rule identity/evidence")
    if "CDX-BLOCK-REPO-PROTECTION-001" in system.get("core_release_blockers",[]):
        fail("verified protection blocker still present in canonical system state")
else:
    if verify.get("all_criteria_verified") is True or all_required:
        fail("verification record claims complete criteria while canonical protection remains unsatisfied")
    if "CDX-BLOCK-REPO-PROTECTION-001" not in system.get("core_release_blockers",[]):
        fail("repository-protection blocker removed before platform verification")
    pre={x.get("blocker_id") for x in preflight.get("blocking_core_conditions",[])}
    if "CDX-BLOCK-REPO-PROTECTION-001" not in pre:
        fail("release preflight lost repository-protection blocker")
    if "CDX-BLOCK-REPO-PROTECTION-001" not in set(order.get("blockers",[])):
        fail("release order lost repository-protection blocker")

print("PASS: WP05 target profile requires PR, owner-bound human approval, constitutional checks and non-destructive main")
print(f"INFO: repository protection verified={verified}")
print("PASS: blocker state cannot be promoted without complete platform verification evidence")
