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
assert_check(ffos.get("anchor_state") == "CDX_CI_MONITORED",
             "FFOS repository-level CDX binding state differs from source evidence")
assert_check(ffos_sys.get("security_state") == "CDX_CI_MONITORED",
             "FFOS systems registry repository-level CDX state mismatch")
assert_check(ffos.get("runtime_integration_state") == "BOUND_PENDING_RUNTIME_INTEGRATION",
             "FFOS source runtime integration unexpectedly promoted")
assert_check(ffos_sys.get("runtime_integration_state") == "BOUND_PENDING_RUNTIME_INTEGRATION",
             "FFOS runtime entry unexpectedly promoted")
assert_check(state.get("consumer_binding_scope") == "RUNTIME_INTEGRATION_ONLY",
             "Central consumer runtime state field is ambiguous")
assert_check(state.get("consumer_bindings", {}).get("Motherpher/FFOS") == "NOT_STARTED",
             "No production runtime evidence was supplied to advance the CDX central state")
binding = state.get("repository_anchor_bindings", {}).get("Motherpher/FFOS", {})
assert_check(binding.get("state") == "CDX_CI_MONITORED",
             "Central repository axis does not match FFOS anchor registry")
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
assert_check("Motherpher/form-flode" not in entries,
             "FFC development PR cannot become admitted by premature registry entry")
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
assert_check(ffos.get("binding_mode") == "PINNED_COMMIT",
             "Pre-release FFOS anchor source pin altered unexpectedly")
assert_check(bool(ffos.get("cdx_ref")), "FFOS pinned CDX ref missing")
assert_check(ffos.get("cdx_ref") == binding.get("state_source_pin", ffos.get("cdx_ref")),
             "FFOS pinned CDX ref inconsistent")
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
assert_check(wp08.get("registry_ref")=="ESTATE-REGISTRY/registry-v2.json",
             "WP08 state does not bind canonical Registry v2")
assert_check(state.get("estate_integration_state")=="PENDING_RUNTIME_BINDINGS",
             "WP08 classification may not promote estate integration")
assert_check("CDX-BLOCK-ESTATE-RUNTIME-001" in state.get("estate_enforcement_blockers",[]),
             "WP08 classification may not close estate runtime blocker")

if issues:
    for item in issues:
        print("FAIL:", item)
    raise SystemExit(1)
print("PASS: CDX estate registry axes and admission statuses internally consistent.")
print("PASS: WP08 Registry v2 applicability classification complete for 31 identifiers / 30 current repositories.")
print(f"NOTE: CDX release_state={release_state}; no downstream runtime enforcement or external anchor verification is implied.")
