#!/usr/bin/env python3
"""Validate CDX estate registry axes after WP10/WP12 without false runtime promotion.

This audit validates central reconciliation against persisted WP10 anchor evidence and
WP12 Pius reference-binding evidence. It does not itself perform remote GitHub verification.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

state = load("GOVERNANCE/system-state.json")
anchors = load("ESTATE-REGISTRY/cdx-anchors.json")
systems = load("ESTATE-REGISTRY/systems.json")
registry_v2 = load("ESTATE-REGISTRY/registry-v2.json")
wp10_evidence = load("ESTATE-REGISTRY/wp10-anchor-verification-evidence.json")
wp12_evidence = load("ESTATE-REGISTRY/wp12-pius-verification-evidence.json")
pius_profile = load("RUNTIME-INTEGRATION/consumers/CDX-PIUS-CONSUMER-001.json")
issues = []

def check(condition, message):
    if not condition:
        issues.append(message)

entries = {x["repository"]: x for x in anchors.get("entries", [])}
pending = {x["repository"]: x for x in anchors.get("pending_admissions", [])}
sys_entries = {x["repository"]: x for x in systems.get("systems", [])}

check(state.get("release_state") == "RELEASED", "CDX release must remain RELEASED")
check(state.get("enforcement_state") == "BOOTSTRAP", "WP10 may not promote estate enforcement")
check(state.get("estate_integration_state") in {"PENDING_RUNTIME_BINDINGS","BINDINGS_IN_PROGRESS"},
      "estate integration state exceeds current WP11 boundary")
check("CDX-BLOCK-ESTATE-RUNTIME-001" in state.get("estate_enforcement_blockers", []), "estate runtime blocker must remain open")

records = registry_v2.get("records", [])
current = [x for x in records if x.get("record_kind") == "CURRENT_REPOSITORY"]
governed = [x for x in current if x.get("applicability") == "GOVERNED_APPLICABLE"]
check(len(records) == 31 and len(current) == 30, "Registry v2 topology drift")
check(len(governed) == 28, "WP10 governed consumer count must remain 28")

for rec in governed:
    repo = rec.get("canonical_repository")
    check(rec.get("anchor_state") == "CDX_BOUND", f"{repo}: Registry v2 anchor not CDX_BOUND")
    check(rec.get("anchor_verification_state") == "PASS", f"{repo}: Registry v2 verification not PASS")
    check(rec.get("wp10_status") == "COMPLETE_VERIFIED_RECONCILED", f"{repo}: WP10 reconciliation missing")
    e = entries.get(repo, {})
    check(bool(e), f"{repo}: missing anchor registry entry")
    check(e.get("anchor_state") == "CDX_BOUND", f"{repo}: anchor registry not CDX_BOUND")
    check(e.get("anchor_verification_state") == "PASS", f"{repo}: anchor registry verification not PASS")
    check(e.get("binding_mode") == "PINNED_RELEASE", f"{repo}: binding mode drift")
    check(e.get("cdx_ref") == "1.0.0", f"{repo}: release pin drift")

bo = next((x for x in current if x.get("repository_identifier") == "Hybrismannen/Barnombudet"), {})
check(bo.get("applicability") == "EXCLUDED_BY_DECISION", "Barnombudet exclusion drift")
check(bo.get("anchor_requirement") == "NOT_REQUIRED_EXCLUDED", "Barnombudet must not gain CDX dependency")

legacy = entries.get("Hybrismannen/form-flode", {})
check(legacy.get("record_state") == "HISTORICAL_ALIAS", "historical form-flode alias provenance lost")
check(legacy.get("anchor_state") == "UNBOUND", "historical alias cannot claim canonical binding")

ffos = entries.get("Motherpher/FFOS", {})
ffos_sys = sys_entries.get("Motherpher/FFOS", {})
check(ffos.get("anchor_state") == "CDX_BOUND", "FFOS anchor not verified")
check(ffos.get("anchor_verification_state") == "PASS", "FFOS anchor verification not PASS")
check(ffos.get("runtime_integration_state") == "BOUND_PENDING_RUNTIME_INTEGRATION", "FFOS runtime was improperly promoted")
check(ffos_sys.get("runtime_integration_state") == "BOUND_PENDING_RUNTIME_INTEGRATION", "FFOS systems runtime was improperly promoted")
ffos_consumer_state = state.get("consumer_bindings", {}).get("Motherpher/FFOS")
check(ffos_consumer_state in {"NOT_STARTED","IMPLEMENTATION_STAGED_VERIFICATION_BLOCKED"},
      "FFOS consumer binding state exceeds current WP11 evidence")
if state.get("estate_integration_state") == "BINDINGS_IN_PROGRESS":
    wp11 = state.get("wp11_ffos_runtime_binding", {})
    check(wp11.get("state") == "IMPLEMENTATION_STAGED_VERIFICATION_BLOCKED",
          "BINDINGS_IN_PROGRESS requires explicit WP11 staged/blocker evidence")
    check(wp11.get("production_deployment_state") == "NOT_DEPLOYED",
          "WP11 staged state must not claim production deployment")
    check("CDX-BLOCK-WP11-FFOS-EXECUTION-001" in state.get("estate_enforcement_blockers", []),
          "WP11 external execution blocker missing")
ffos_binding = state.get("repository_anchor_bindings", {}).get("Motherpher/FFOS", {})
check(ffos_binding.get("state") == "CDX_BOUND" and ffos_binding.get("verification") == "PASS", "central FFOS anchor axis not reconciled")

pius = entries.get("Hybrismannen/pius-universe", {})
check(pius.get("anchor_state") == "CDX_BOUND", "Pius anchor not verified")
check(pius.get("anchor_verification_state") == "PASS", "Pius anchor verification not PASS")
check(pius.get("runtime_integration_state") == "VERIFIED_REFERENCE_RUNTIME",
      "WP12 must reconcile Pius only to VERIFIED_REFERENCE_RUNTIME")
check(pius.get("estate_admission_state") == "REFERENCE_CONSUMER_VERIFIED_WP12",
      "Pius WP12 reference-consumer admission state missing")
check(pius.get("consequential_enforcement_verified") is False,
      "Pius reference verification must not claim consequential enforcement")
pius_sys = sys_entries.get("Hybrismannen/pius-universe", {})
check(pius_sys.get("runtime_integration_state") == "VERIFIED_REFERENCE_RUNTIME",
      "Pius systems registry not reconciled to reference-runtime state")
check(pius_sys.get("consequential_enforcement_verified") is False,
      "Pius systems registry falsely claims consequential enforcement")

wp12 = state.get("wp12_pius_verification", {})
check(wp12.get("state") == "COMPLETE_PIUS_REFERENCE_BINDING_VERIFIED",
      "system-state WP12 closure missing")
check(wp12.get("reference_runtime_state") == "VERIFIED_REFERENCE_RUNTIME_REPOSITORY_CI_ONLY",
      "WP12 reference-runtime scope drift")
check(wp12.get("consequential_enforcement_verified") is False,
      "WP12 may not promote consequential enforcement")
check(wp12.get("production_effect_authorization") is False,
      "WP12 may not authorize production effects")

check(wp12_evidence.get("programme") == "CDX-WP12", "WP12 evidence identity mismatch")
check(wp12_evidence.get("result", {}).get("reference_binding_verification") == "PASS",
      "WP12 evidence does not verify Pius reference binding")
check(wp12_evidence.get("result", {}).get("consequential_runtime_verification") == "NOT_VERIFIED_NOT_IMPLEMENTED",
      "WP12 evidence improperly advances Pius consequential runtime")
check(pius_profile.get("status") == "ADMITTED_REFERENCE_CONSUMER_PROFILE",
      "Pius reference consumer profile not admitted")
check(pius_profile.get("production_effect_authorization") is False,
      "Pius consumer profile may not grant production-effect authority")

wp10 = state.get("wp10_anchor_verification", {})
check(wp10.get("state") == "COMPLETE_ANCHORS_VERIFIED_RECONCILED", "system-state WP10 closure missing")
check(wp10.get("governed_consumers_verified") == 28, "system-state WP10 verified count mismatch")
check(wp10.get("local_reconciliation_prs_merged") == 28, "system-state WP10 merge count mismatch")
check(wp10.get("default_branch_readbacks_passed") == 28, "system-state WP10 readback count mismatch")

summary = wp10_evidence.get("verification_summary", {})
recon = wp10_evidence.get("reconciliation", {})
check(summary.get("governed_consumers_verified") == 28 and summary.get("failures") == 0, "WP10 evidence verification summary invalid")
check(recon.get("state") == "COMPLETE", "WP10 evidence reconciliation incomplete")
check(recon.get("local_anchor_prs_merged") == 28, "WP10 evidence local merge count mismatch")
check(recon.get("default_branch_readbacks_passed") == 28, "WP10 evidence readback count mismatch")

if issues:
    for item in issues:
        print("FAIL:", item)
    raise SystemExit(1)

print("PASS: WP10 anchor verification and reconciliation are internally consistent.")
print("PASS: 28/28 governed consumers are CDX_BOUND / PASS on the anchor axis.")
print("PASS: FFOS runtime verification, FFC admission and estate enforcement remain unadvanced.")
print("PASS: Pius is independently verified only at repository-CI reference-runtime scope; consequential enforcement remains false.")
print(f"PASS: estate integration state={state.get('estate_integration_state')} within current rollout boundary.")
