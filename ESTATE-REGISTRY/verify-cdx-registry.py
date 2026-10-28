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
assert_check(state.get("release_state") == "PRE_RELEASE",
             "Unexpected CDX release promotion without release evidence")
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

if issues:
    for item in issues:
        print("FAIL:", item)
    raise SystemExit(1)
print("PASS: CDX estate registry axes and admission statuses internally consistent.")
print("NOTE: No CDX runtime enforcement, branch protection or external anchor verification established.")
