#!/usr/bin/env python3
"""CDX estate integrity audit. Supports legacy bindings and canonical .cdx anchors.

Does not certify runtime enforcement. Enforces distinction between repository
registration/CI observation and application-runtime evidence.
"""
from pathlib import Path
import json

def fail(message):
    print("FAIL:",message)
    raise SystemExit(1)

registry_path=Path("ESTATE-REGISTRY/systems.json")
anchor_path=Path("ESTATE-REGISTRY/cdx-anchors.json")
registry_v2_path=Path("ESTATE-REGISTRY/registry-v2.json")
wp09_evidence_path=Path("ESTATE-REGISTRY/wp09-migration-evidence.json")
if not registry_path.exists():fail("missing estate registry")
if not anchor_path.exists():fail("missing canonical anchor registry")
if not registry_v2_path.exists():fail("missing Registry v2 applicability classification")
if not wp09_evidence_path.exists():fail("missing WP09 migration evidence")
d=json.loads(registry_path.read_text())
ar=json.loads(anchor_path.read_text())
r2=json.loads(registry_v2_path.read_text())
wp09=json.loads(wp09_evidence_path.read_text())
systems=d.get("systems",[])
if not systems:fail("empty estate registry")
ids=[s.get("system_id") for s in systems]
repos=[s.get("repository") for s in systems]
if len(ids)!=len(set(ids)):fail("duplicate system_id")
if len(repos)!=len(set(repos)):fail("duplicate repository")
root=[s for s in systems if s.get("system_id")=="CDX-SYS-001"]
if len(root)!=1:fail("Conductellence root missing or duplicated")
anchors={a.get("repository"):a for a in ar.get("entries",[])}
pending={a.get("repository"):a for a in ar.get("pending_admissions",[])}
assert not set(anchors).intersection(pending), "A candidate must not also be an admitted anchor"

legacy=0
canonical=0
for s in systems:
    sid=s.get("system_id")
    rep=s.get("repository")
    if not rep:fail(f"{sid}: repository missing")
    if sid=="CDX-SYS-001":continue
    if s.get("authority_ref")!="CDX-SYS-001":fail(f"{sid}: wrong authority_ref")
    manifest=s.get("binding_manifest")
    state=s.get("runtime_integration_state")
    if manifest==".security/conductellence.json":
        # Preserve historical estate evidence; do not silently rewrite this
        # validation merely because a newer canonical anchor is introduced.
        legacy+=1
        if state not in {"NOT_VERIFIED","VERIFIED_REFERENCE_RUNTIME","VERIFIED_PRODUCTION_RUNTIME"}:
            fail(f"{sid}: invalid legacy runtime integration state {state}")
    elif manifest==".cdx/anchor.json":
        canonical+=1
        a=anchors.get(rep)
        if not a:fail(f"{sid}: canonical anchor missing from CDX anchor estate")
        if a.get("system_id")!=sid:fail(f"{sid}: mismatched system identity")
        if a.get("anchor_manifest")!=".cdx/anchor.json":fail(f"{sid}: invalid anchor path")
        if s.get("security_state")!=a.get("anchor_state"):
            fail(f"{sid}: repository-level binding states do not agree")
        if s.get("binding_mode")!=a.get("binding_mode"):
            fail(f"{sid}: binding mode mismatch")
        if s.get("cdx_ref")!=a.get("cdx_ref"):
            fail(f"{sid}: pinned CDX source mismatch")
        if state!=a.get("runtime_integration_state"):
            fail(f"{sid}: conflicting runtime status")
        if state=="NOT_VERIFIED":
            if a.get("anchor_state")!="ANCHOR_DECLARED":
                fail(f"{sid}: NOT_VERIFIED runtime state is only valid for an unverified ANCHOR_DECLARED binding")
        elif state not in {"BOUND_PENDING_RUNTIME_INTEGRATION","RUNTIME_GUARDED_UNVERIFIED",
                           "VERIFIED_REFERENCE_RUNTIME","VERIFIED_RUNTIME_BOUND"}:
            fail(f"{sid}: invalid canonical-anchor runtime state {state}")
        if state=="VERIFIED_RUNTIME_BOUND":
            if s.get("consequential_enforcement_verified") is not True:
                fail(f"{sid}: verified runtime requires actual effect gate evidence")
            if not s.get("spetl_runtime_evidence_ref"):
                fail(f"{sid}: verified runtime requires SPETL evidence reference")
    else:
        fail(f"{sid}: binding manifest missing or unrecognized")

# Developmental FFC anchor must remain pending until its consumer PR has merged
# and independent schema/estate verification is performed.
ffc=pending.get("Motherpher/form-flode")
if ffc and ffc.get("verification_state")!="NOT_VERIFIED":
    fail("pending FFC admission must remain NOT_VERIFIED")
if ffc and "Motherpher/form-flode" in repos:
    fail("pending FFC development branch admitted without verification")

# Historical Form & Flöde path is a provenance alias of the current Motherpher repository,
# not a second repository. Both identities must remain explicitly reconciled.
legacy_ff=next((s for s in systems if s.get("repository")=="Hybrismannen/form-flode"),None)
legacy_ff_anchor=anchors.get("Hybrismannen/form-flode")
if legacy_ff:
    if legacy_ff.get("record_state")!="HISTORICAL_ALIAS":
        fail("historical form-flode system record must be marked HISTORICAL_ALIAS")
    if legacy_ff.get("canonical_repository")!="Motherpher/form-flode":
        fail("historical form-flode canonical repository mismatch")
    if legacy_ff.get("repository_id")!="1379622813":
        fail("historical form-flode repository id mismatch")
if legacy_ff_anchor:
    if legacy_ff_anchor.get("record_state")!="HISTORICAL_ALIAS":
        fail("historical form-flode anchor record must be marked HISTORICAL_ALIAS")
    if legacy_ff_anchor.get("anchor_state")!="UNBOUND":
        fail("historical alias cannot claim canonical CDX binding")
if ffc:
    if ffc.get("repository_id")!="1379622813":
        fail("FFC pending record repository id mismatch")
    if ffc.get("historical_alias")!="Hybrismannen/form-flode":
        fail("FFC pending record must preserve historical alias")
    if ffc.get("migration_kind")!="REPOSITORY_IDENTITY_MIGRATION":
        fail("FFC must be modeled as repository identity migration")

# WP08 Registry v2 applicability classification.
if r2.get("schema")!="cdx.estate-registry/v2.0":
    fail("Registry v2 schema mismatch")
if r2.get("registry_id")!="CDX-ESTATE-REGISTRY-V2":
    fail("Registry v2 identity mismatch")
top=r2.get("topology",{})
expected_top={
    "known_repository_identifiers":31,
    "unique_current_repository_objects":30,
    "current_authority_sources":1,
    "current_governed_applicable":28,
    "current_excluded_by_decision":1,
    "historical_alias_records":1,
}
if top!=expected_top:
    fail(f"Registry v2 topology mismatch: {top}")
r2_records=r2.get("records",[])
if len(r2_records)!=31:
    fail(f"Registry v2 must contain 31 identifier records, found {len(r2_records)}")
rids=[x.get("record_id") for x in r2_records]
idents=[x.get("repository_identifier") for x in r2_records]
if len(rids)!=len(set(rids)):
    fail("Registry v2 duplicate record_id")
if len(idents)!=len(set(idents)):
    fail("Registry v2 duplicate repository identifier")

current=[x for x in r2_records if x.get("record_kind")=="CURRENT_REPOSITORY"]
aliases=[x for x in r2_records if x.get("record_kind")=="HISTORICAL_ALIAS"]
if len(current)!=30 or len(aliases)!=1:
    fail("Registry v2 current/alias topology must be 30/1")
current_repo_ids=[x.get("repository_id") for x in current]
if len(current_repo_ids)!=len(set(current_repo_ids)):
    fail("Registry v2 current repository IDs are not unique")

counts={}
for x in r2_records:
    counts[x.get("applicability")]=counts.get(x.get("applicability"),0)+1
if counts!={"AUTHORITY_SOURCE":1,"HISTORICAL_ALIAS":1,"GOVERNED_APPLICABLE":28,"EXCLUDED_BY_DECISION":1}:
    fail(f"Registry v2 applicability counts invalid: {counts}")

authority=next((x for x in r2_records if x.get("applicability")=="AUTHORITY_SOURCE"),None)
if not authority or authority.get("repository_identifier")!="Hybrismannen/Conductellence-" or authority.get("anchor_requirement")!="SELF_AUTHORITY_SOURCE":
    fail("Registry v2 authority source classification invalid")

excluded=next((x for x in r2_records if x.get("applicability")=="EXCLUDED_BY_DECISION"),None)
if not excluded or excluded.get("repository_identifier")!="Hybrismannen/Barnombudet":
    fail("Barnombudet explicit exclusion missing from Registry v2")
if excluded.get("anchor_requirement")!="NOT_REQUIRED_EXCLUDED" or excluded.get("wp09_action")!="NONE":
    fail("Excluded Barnombudet repository may not be scheduled for CDX anchor migration")

alias=aliases[0]
ffc_current=next((x for x in current if x.get("repository_identifier")=="Motherpher/form-flode"),None)
if (alias.get("repository_identifier")!="Hybrismannen/form-flode"
    or alias.get("canonical_repository")!="Motherpher/form-flode"
    or alias.get("repository_id")!="1379622813"
    or not ffc_current
    or ffc_current.get("repository_id")!="1379622813"):
    fail("Form & Flöde historical alias/current repository identity reconciliation invalid")

governed=[x for x in current if x.get("applicability")=="GOVERNED_APPLICABLE"]
for x in governed:
    if x.get("anchor_requirement")!="REQUIRED":
        fail(f"{x.get('repository_identifier')}: governed current repository must require canonical anchor")
    if x.get("wp09_action")=="NONE":
        fail(f"{x.get('repository_identifier')}: governed current repository lacks WP09 action")
    if x.get("wp10_action")!="VERIFY_AFTER_WP09":
        fail(f"{x.get('repository_identifier')}: governed current repository lacks WP10 verification handoff")

# WP09 canonical anchor migration must be complete but not prematurely verified.
if r2.get("wp09_migration",{}).get("state")!="COMPLETE":
    fail("Registry v2 does not record WP09 completion")
if r2.get("wp09_migration",{}).get("governed_consumers_migrated")!=28:
    fail("WP09 migrated consumer count must be 28")

expected_digest="git-blob-sha1:55dbcdac2f822b59a5a5f0f19eeadfa61d2c7ed0"
for x in governed:
    rep=x.get("repository_identifier")
    if x.get("anchor_state")!="ANCHOR_DECLARED":
        fail(f"{rep}: WP09 migrated anchor must remain ANCHOR_DECLARED pending WP10")
    if x.get("wp09_status")!="COMPLETE_MIGRATED":
        fail(f"{rep}: WP09 migration status incomplete")
    if x.get("anchor_observed_on_default_branch") is not True:
        fail(f"{rep}: default-branch anchor readback missing")
    if x.get("binding_mode")!="PINNED_RELEASE" or x.get("cdx_ref")!="1.0.0":
        fail(f"{rep}: canonical anchor not pinned to released CDX 1.0.0")
    if x.get("policy_digest")!=expected_digest:
        fail(f"{rep}: CDX 1.0.0 policy digest mismatch")
    if x.get("anchor_verification_state")!="NOT_VERIFIED":
        fail(f"{rep}: WP09 must not pre-verify anchor before WP10")
    if x.get("wp10_action")!="VERIFY_AFTER_WP09":
        fail(f"{rep}: missing WP10 verification handoff")

if wp09.get("programme")!="CDX-WP09":
    fail("WP09 migration evidence identity mismatch")
if wp09.get("governed_consumers_expected")!=28 or wp09.get("governed_consumers_migrated")!=28:
    fail("WP09 migration evidence does not account for all governed consumers")
if wp09.get("all_default_branch_readbacks_passed") is not True:
    fail("WP09 default-branch readbacks not complete")
if len(wp09.get("migrations",[]))!=28:
    fail("WP09 migration evidence must contain 28 repository records")
for m in wp09.get("migrations",[]):
    if (m.get("binding_mode")!="PINNED_RELEASE" or m.get("release_ref")!="1.0.0"
        or m.get("policy_digest")!=expected_digest
        or m.get("anchor_state")!="ANCHOR_DECLARED"
        or m.get("verification_state")!="NOT_VERIFIED"):
        fail(f"{m.get('repository')}: invalid WP09 migration evidence")

allowed_runtime=set(r2.get("classification_rules",{}).get("runtime_screening",[]))
for x in r2_records:
    if x.get("runtime_screening") not in allowed_runtime:
        fail(f"{x.get('repository_identifier')}: invalid runtime screening class")
    if x.get("runtime_screening") in {"VERIFIED_RUNTIME_BOUND","VERIFIED_PRODUCTION_RUNTIME"}:
        fail("Registry v2 classification must not promote runtime verification")

print(f"PASS: Estate Registry contains {len(systems)} unique governed repository records")
print(f"PASS: {legacy} legacy bindings + {canonical} canonical anchors differentiated")
print("PASS: Registry v2 classifies 31 identifiers / 30 current repository objects with explicit applicability")
print("PASS: WP09 migrated all 28 governed consumers to release-pinned ANCHOR_DECLARED / NOT_VERIFIED state")
print("PASS: repository binding separate from application-runtime evidence")
print("NOTE: registry audit does not by itself establish CDX-RUNTIME-001 verification")
