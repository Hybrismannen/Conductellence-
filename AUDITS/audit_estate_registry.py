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
if not registry_path.exists():fail("missing estate registry")
if not anchor_path.exists():fail("missing canonical anchor registry")
d=json.loads(registry_path.read_text())
ar=json.loads(anchor_path.read_text())
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

print(f"PASS: Estate Registry contains {len(systems)} unique governed repository records")
print(f"PASS: {legacy} legacy bindings + {canonical} canonical anchors differentiated")
print("PASS: repository binding separate from application-runtime evidence")
print("NOTE: registry audit does not by itself establish CDX-RUNTIME-001 verification")
