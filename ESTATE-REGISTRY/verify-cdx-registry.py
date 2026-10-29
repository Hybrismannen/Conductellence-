#!/usr/bin/env python3
"""Validate CDX registry axes consistently without claiming runtime enforcement.

Does not perform remote verification. CI success means only internal consistency.
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
issues = []

def assert_check(condition, message):
    if not condition:
        issues.append(message)

entries = {x["repository"]: x for x in anchors.get("entries", [])}
pending = {x["repository"]: x for x in anchors.get("pending_admissions", [])}
sys_entries = {x["repository"]: x for x in systems.get("systems", [])}
ffos = entries.get("Motherpher/FFOS", {})
ffos_sys = sys_entries.get("Motherpher/FFOS", {})
assert_check(bool(ffos), "FFOS missing in anchor estate registry")
assert_check(bool(ffos_sys), "FFOS missing in systems estate registry")
assert_check(ffos.get("anchor_state") == "ANCHOR_DECLARED",
             "FFOS WP09 anchor must remain ANCHOR_DECLARED pending WP10")
assert_check(ffos_sys.get("security_state") == "ANCHOR_DECLARED",
             "FFOS systems registry must match WP09 anchor declaration state")
assert_check(ffos.get("runtime_integration_state") == "BOUND_PENDING_RUNTIME_INTEGRATION",
             "FFOS source runtime integration unexpectedly promoted")
assert_check(ffos_sys.get("runtime_integration_state") == "BOUND_PENDING_RUNTIME_INTEGRATION",
             "FFOS runtime entry unexpectedly promoted")
assert_check(state.get("consumer_binding_scope") == "RUNTIME_INTEGRATION_ONLY",
             "Central consumer runtime state field is ambiguous")
assert_check(state.get("consumer_bindings", {}).get("Motherpher/FFOS") == "NOT_STARTED",
             "No production runtime evidence was supplied to advance the CDX central state")
binding = state.get("repository_anchor_bindings", {}).get("Motherpher/FFOS", {})
assert_check(binding.get("state") == "ANCHOR_DECLARED",
             "Central repository axis does not match FFOS WP09 declaration")
assert_check(binding.get("verification") == "NOT_VERIFIED",
             "FFOS central anchor binding must remain NOT_VERIFIED pending WP10")
assert_check(binding.get("binding_mode") == "PINNED_RELEASE",
             "FFOS central anchor binding must use PINNED_RELEASE after WP09")
assert_check(binding.get("state_source_pin") == "1.0.0",
             "FFOS central anchor binding must pin CDX release 1.0.0")
release_state=state.get("release_state")
if release_state=="PRE_RELEASE":
    pass
elif release_state=="RELEASED":
    publication_path=ROOT / "GOVERNANCE/release/CDX-1.0-PUBLICATION-EVIDENCE-2026-10-29.json"
    order_path=ROOT / "GOVERNANCE/orders/CDX-RELEASE-1.0.0.json"
    assert_check(publication_path.exists(), "RELEASED CDX state lacks publication evidence")
    assert_check(order_path.exists(), "RELEASED CDX state lacks release order")
    if publication_path.exists() and order_path.exists():
        publication=json.loads(publication_path.read_text(encoding="utf-8"))
        release_order=json.loads(order_path.read_text(encoding="utf-8"))
        assert_check(publication.get("publication_verified") is True,
                     "RELEASED CDX state lacks verified publication")
        assert_check(publication.get("release_published") is True,
                     "RELEASED CDX state lacks observed GitHub Release")
        assert_check(publication.get("tag",{}).get("name") == "1.0.0",
                     "RELEASED CDX state has unexpected release tag")
        assert_check(release_order.get("state") == "PUBLISHED",
                     "RELEASED CDX state release order is not PUBLISHED")
        assert_check(release_order.get("publication_state") == "PUBLISHED_VERIFIED",
                     "RELEASED CDX state publication order is not verified")
else:
    assert_check(False, f"Unexpected CDX release state: {release_state}")
assert_check(state.get("enforcement_state") == "BOOTSTRAP",
             "Unexpected CDX enforcement promotion without runtime/protection evidence")
ffc = pending.get("Motherpher/form-flode", {})
assert_check(bool(ffc), "New FFC source not recorded as a pending admission")
assert_check(ffc.get("verification_state") == "NOT_VERIFIED",
             "FFC pending declaration must not claim verified binding")
assert_check(ffc.get("anchor_state") == "ANCHOR_DECLARED",
             "FFC WP09 anchor installation must be represented as ANCHOR_DECLARED")
assert_check(ffc.get("main_branch_anchor_present") is True,
             "FFC WP09 anchor must be observed on current main")
assert_check(ffc.get("binding_mode") == "PINNED_RELEASE" and ffc.get("cdx_ref") == "1.0.0",
             "FFC WP09 anchor must pin released CDX 1.0.0")
assert_check("Motherpher/form-flode" not in entries,
             "FFC must remain pending admission until WP13")
legacy_ff = sys_entries.get("Hybrismannen/form-flode", {})
legacy_ff_anchor = entries.get("Hybrismannen/form-flode", {})
assert_check(legacy_ff.get("record_state") == "HISTORICAL_ALIAS",
             "Historical form-flode systems record must be marked HISTORICAL_ALIAS")
assert_check(legacy_ff.get("canonical_repository") == "Motherpher/form-flode",
             "Historical form-flode canonical repository mismatch")
assert_check(legacy_ff.get("repository_id") == "1379622813",
             "Historical form-flode repository id mismatch")
assert_check(legacy_ff_anchor.get("record_state") == "HISTORICAL_ALIAS",
             "Historical form-flode anchor record must be provenance-only alias")
assert_check(legacy_ff_anchor.get("anchor_state") == "UNBOUND",
             "Historical form-flode alias cannot claim canonical binding")
assert_check(ffc.get("repository_id") == "1379622813",
             "FFC pending repository id mismatch")
assert_check(ffc.get("historical_alias") == "Hybrismannen/form-flode",
             "FFC pending record missing historical repository alias")
assert_check(ffc.get("migration_kind") == "REPOSITORY_IDENTITY_MIGRATION",
             "FFC must be represented as repository identity migration")
assert_check(ffos.get("binding_mode") == "PINNED_RELEASE",
             "FFOS anchor must be release-pinned after WP09")
assert_check(ffos.get("cdx_ref") == "1.0.0",
             "FFOS anchor registry must pin CDX release 1.0.0")
assert_check(ffos.get("anchor_verification_state") == "NOT_VERIFIED",
             "FFOS anchor must remain NOT_VERIFIED until WP10")
assert_check(ffos.get("cdx_ref") == binding.get("state_source_pin"),
             "FFOS pinned CDX release inconsistent with central state")
assert_check(anchors.get("canonical_local_anchor") == ".cdx/anchor.json",
             "Unexpected canonical CDX anchor path")
assert_check(not ffos_sys.get("consequential_enforcement_verified", False),
             "FFOS cannot claim runtime verified without tested local enforcement")

r2_records=registry_v2.get("records",[])
r2_current=[x for x in r2_records if x.get("record_kind")=="CURRENT_REPOSITORY"]
r2_alias=[x for x in r2_records if x.get("record_kind")=="HISTORICAL_ALIAS"]
assert_check(registry_v2.get("registry_id")=="CDX-ESTATE-REGISTRY-V2",
             "Registry v2 canonical identity missing")
assert_check(len(r2_records)==31 and len(r2_current)==30 and len(r2_alias)==1,
             "Registry v2 must preserve 31 identifiers / 30 current repositories / 1 alias")
assert_check(sum(1 for x in r2_current if x.get("applicability")=="GOVERNED_APPLICABLE")==28,
             "Registry v2 governed-applicable current count must be 28")
assert_check(sum(1 for x in r2_current if x.get("applicability")=="AUTHORITY_SOURCE")==1,
             "Registry v2 must contain one authority source")
assert_check(sum(1 for x in r2_current if x.get("applicability")=="EXCLUDED_BY_DECISION")==1,
             "Registry v2 must contain one explicit current exclusion")
bo=next((x for x in r2_current if x.get("repository_identifier")=="Hybrismannen/Barnombudet"),{})
assert_check(bo.get("applicability")=="EXCLUDED_BY_DECISION",
             "Barnombudet must remain explicitly excluded from CDX dependency")
assert_check(bo.get("anchor_requirement")=="NOT_REQUIRED_EXCLUDED",
             "Barnombudet exclusion must not create anchor dependency")
wp08=state.get("wp08_estate_registry_v2",{})
assert_check(wp08.get("state")=="COMPLETE_APPLICABILITY_CLASSIFIED",
             "system state does not record WP08 completion")
wp09=state.get("wp09_anchor_migration",{})
assert_check(wp09.get("state")=="COMPLETE_ANCHORS_MIGRATED",
             "system state does not record WP09 completion")
assert_check(wp09.get("governed_consumers_expected")==28 and wp09.get("governed_consumers_migrated")==28,
             "WP09 system state does not account for all 28 governed consumers")
assert_check(wp09.get("default_branch_readbacks_passed")==28,
             "WP09 system state lacks 28 default-branch readbacks")
assert_check(wp09.get("binding_mode")=="PINNED_RELEASE" and wp09.get("release_ref")=="1.0.0",
             "WP09 system state does not bind migration to CDX release 1.0.0")
assert_check(wp09.get("verification_state")=="NOT_VERIFIED",
             "WP09 may not pre-verify estate anchors before WP10")
assert_check(wp08.get("registry_ref")=="ESTATE-REGISTRY/registry-v2.json",
             "WP08 state does not bind canonical Registry v2")
assert_check(state.get("estate_integration_state")=="PENDING_RUNTIME_BINDINGS",
             "WP08/WP09 may not promote estate integration")
assert_check("CDX-BLOCK-ESTATE-RUNTIME-001" in state.get("estate_enforcement_blockers",[]),
             "WP08/WP09 may not close estate runtime blocker")

if issues:
    for item in issues:
        print("FAIL:", item)
    raise SystemExit(1)
print("PASS: CDX estate registry axes and admission statuses internally consistent.")
print("PASS: WP08 Registry v2 applicability classification complete for 31 identifiers / 30 current repositories.")
print("PASS: WP09 canonical anchors migrated across all 28 governed consumers; verification remains WP10.")
print(f"NOTE: CDX release_state={release_state}; no downstream runtime enforcement or external anchor verification is implied.")
