#!/usr/bin/env python3
"""Validate CDX estate registry axes through WP14 without false runtime promotion.

This audit validates central reconciliation against persisted anchor, admission and
estate-propagation evidence. It does not itself perform remote GitHub verification.
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
wp13_evidence = load("ESTATE-REGISTRY/wp13-ffc-admission-evidence.json")
wp14_evidence = load("ESTATE-REGISTRY/wp14-estate-propagation-closure-evidence.json")
wp15_ledger = load("PROGRAMME/CDX-1.0-WORK-PACKAGE-LEDGER.json")
residual = load("GOVERNANCE/CDX-1.0-RESIDUAL-OBLIGATIONS.json")
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
check(state.get("wp14_estate_propagation_closure", {}).get("state") == "COMPLETE_ESTATE_GOVERNANCE_PROPAGATION",
      "WP14 central closure missing")
check(state.get("programme_closure", {}).get("state") == "FINAL_ACCEPTED_WITH_RESIDUAL_DOWNSTREAM_OBLIGATIONS",
      "CDX final programme acceptance state missing")
check(state.get("wp15_final_programme_acceptance", {}).get("state") == "COMPLETE_FINAL_PROGRAMME_ACCEPTANCE",
      "WP15 final acceptance state missing")
check(state.get("enforcement_state") == "BOOTSTRAP", "WP14 may not promote enforcement")
check(state.get("estate_integration_state") == "BINDINGS_IN_PROGRESS", "WP14 may not promote estate integration")
check(len(pending) == 0, "WP14 requires zero pending admissions")

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

ffc = entries.get("Motherpher/form-flode", {})
ffc_sys = sys_entries.get("Motherpher/form-flode", {})
check("Motherpher/form-flode" not in pending, "FFC must leave pending admissions after WP13")
check(ffc.get("system_id") == "FFC", "FFC canonical system identity missing")
check(ffc.get("repository_id") == "1379622813", "FFC repository identity mismatch")
check(ffc.get("estate_admission_state") == "FORMALLY_ADMITTED_WP13", "FFC formal admission state missing")
check(ffc.get("runtime_integration_state") == "NOT_VERIFIED", "FFC runtime must remain NOT_VERIFIED")
check(ffc_sys.get("system_id") == "FFC", "canonical FFC systems entry missing")
check(wp13_evidence.get("result", {}).get("formal_admission") == "PASS", "WP13 evidence not PASS")


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
    check(wp11.get("production_deployment_state") in {"NOT_DEPLOYED","NOT_DEPLOYED_CURRENT_IMPLEMENTATION","NOT_REQUIRED_FOR_RUNTIME_VERIFICATION"},
          "WP11 staged state must not claim production deployment")
    check(wp11.get("implementation_pr") == 35,
          "WP11 current implementation must resolve to FFOS PR #35")
    check(wp11.get("proposed_runtime_state") == "RUNTIME_GUARDED_UNVERIFIED",
          "WP11 blocked implementation may not claim verified runtime")
    check({x.get("id") for x in wp11.get("blockers", [])} == {"FFOS-GHA-RUNNER-001"},
          "WP11 current external blocker set is incomplete")
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

wp14_result = wp14_evidence.get("result", {})
wp14_prop = wp14_evidence.get("propagation_result", {})
check(wp14_evidence.get("programme") == "CDX-WP14", "WP14 evidence identity mismatch")
check(wp14_result.get("governance_propagation_closure") == "PASS", "WP14 closure evidence not PASS")
check(wp14_prop.get("governed_repositories_expected") == 28, "WP14 evidence governed count mismatch")
check(wp14_prop.get("governed_repositories_cdxb_bound_pass") == 28, "WP14 evidence bound/PASS count mismatch")
check(wp14_prop.get("pending_admissions") == 0, "WP14 evidence pending admission count mismatch")
check(wp14_evidence.get("runtime_boundary", {}).get("consequential_verified_runtime_count") == 0,
      "WP14 evidence falsely claims verified consequential runtime")
check(wp14_result.get("verified_runtime_bound_claim") is False, "WP14 may not claim VERIFIED_RUNTIME_BOUND")
check(wp14_result.get("enforcing_claim") is False, "WP14 may not claim ENFORCING")

wp15_summary = wp15_ledger.get("completion_summary", {})
check(wp15_ledger.get("final_work_package") == "WP15", "WP15 ledger final work-package mismatch")
check(wp15_summary.get("total_work_packages") == 16, "WP15 ledger total mismatch")
check(wp15_summary.get("complete") == 15, "WP15 ledger complete-count mismatch")
check(wp15_summary.get("transferred_residual_obligation") == 1,
      "WP15 ledger must preserve exactly one transferred residual work package")
wp11_row = next((x for x in wp15_ledger.get("work_packages", []) if x.get("work_package") == "WP11"), {})
check(wp11_row.get("state") == "TRANSFERRED_RESIDUAL_OBLIGATION",
      "WP11 must remain transferred residual obligation, not falsely complete")
check(residual.get("programme_state") == "FINAL_ACCEPTED_WITH_RESIDUAL_DOWNSTREAM_OBLIGATIONS",
      "residual-obligation register programme state mismatch")
open_residual = {x.get("id"): x for x in residual.get("obligations", [])}
check(open_residual.get("CDX-RESIDUAL-RUNTIME-001", {}).get("state") == "OPEN",
      "estate runtime residual obligation must remain open")
check(open_residual.get("CDX-RESIDUAL-WP11-FFOS-001", {}).get("state") in {"OPEN","OPEN_IMPLEMENTATION_STAGED_VERIFICATION_BLOCKED"},
      "WP11 FFOS residual obligation must remain open")
check(open_residual.get("CDX-RESIDUAL-WP11-FFOS-001", {}).get("current_implementation", {}).get("pr") == 35,
      "WP11 residual must point to current FFOS PR #35")
check(state.get("estate_integration_state") == "BINDINGS_IN_PROGRESS",
      "WP15 must not promote estate integration")
check(state.get("enforcement_state") == "BOOTSTRAP",
      "WP15 must not promote enforcement")

if issues:
    for item in issues:
        print("FAIL:", item)
    raise SystemExit(1)

print("PASS: WP10 anchor verification and reconciliation are internally consistent.")
print("PASS: 28/28 governed consumers are CDX_BOUND / PASS on the anchor axis.")
print("PASS: FFC formal admission is complete; FFOS runtime verification and estate enforcement remain unadvanced.")
print("PASS: Pius is independently verified only at repository-CI reference-runtime scope; consequential enforcement remains false.")
print("PASS: WP14 estate-governance propagation is complete with 28/28 governed repositories CDX_BOUND / PASS and zero pending admissions.")
print("PASS: WP15 final-accepts the central programme while preserving WP11 and estate runtime as residual obligations.")
print(f"PASS: estate integration state={state.get('estate_integration_state')} and enforcement={state.get('enforcement_state')} remain correctly bounded.")
