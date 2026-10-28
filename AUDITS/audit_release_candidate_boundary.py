#!/usr/bin/env python3
"""AUD-CDX-RC-BOUNDARY-001 — enforce the CDX RC-01 capability boundary."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

boundary=load("GOVERNANCE/release-candidate-boundary.json")
bindings=load("CONTROL-CATALOGUE/law-bindings.json")
controls=load("POLICY/control-registry.json")
procedures=load("REVIEW-CATALOGUE/procedures.json")
state=load("GOVERNANCE/system-state.json")

if boundary.get("boundary_id")!="CDX-RC-01": fail("unexpected release-candidate boundary id")
if boundary.get("state")!="FROZEN_FOR_CLOSURE": fail("RC-01 boundary is not frozen for closure")
if boundary.get("target_release")!="1.0.0": fail("RC-01 target release changed")
if boundary.get("no_state_promotion") is None: fail("missing no-state-promotion rule")

frozen=boundary["freeze_dimensions"]

actual_dirs={p.name for p in ROOT.iterdir() if p.is_dir() and p.name not in {".git","__pycache__"}}
allowed=set(frozen["top_level_capability_domains"])|set(frozen["reserved_non_capability_roots"])
unexpected=sorted(actual_dirs-allowed)
if unexpected: fail("unreserved top-level domain(s): "+", ".join(unexpected))
missing=sorted(set(frozen["top_level_capability_domains"])-actual_dirs)
if missing: fail("frozen capability domain(s) missing: "+", ".join(missing))

actual_sections=[s["section_id"] for s in bindings.get("sections",[])]
if actual_sections!=frozen["law_section_ids"]:
    missing_ids=sorted(set(frozen["law_section_ids"])-set(actual_sections))
    added_ids=sorted(set(actual_sections)-set(frozen["law_section_ids"]))
    fail(f"law section boundary changed; missing={missing_ids} added={added_ids}")
if len(actual_sections)!=131 or frozen.get("law_section_count")!=131:
    fail("RC-01 must preserve exactly 131 law section IDs")
if bindings.get("law_id")!=frozen["law_id"]:
    fail("canonical law id changed")

actual_auditability=sorted(set(s.get("auditability") for s in bindings["sections"]))
if actual_auditability!=sorted(frozen["auditability_classes"]):
    fail("auditability class grammar changed")

actual_surfaces=sorted(set(c.get("enforcement_surface") for c in controls.get("controls",[]) if c.get("enforcement_surface")))
if actual_surfaces!=sorted(frozen["enforcement_surface_classes"]):
    fail("enforcement-surface grammar changed")

actual_reviews=sorted((p.get("procedure_id") or p.get("id")) for p in procedures.get("procedures",[]))
if actual_reviews!=sorted(frozen["review_procedure_classes"]):
    fail("review procedure class grammar changed")

if controls.get("default_behavior")!=frozen["default_policy_behavior"]:
    fail("default policy behavior changed")
if frozen["default_policy_behavior"]!="DENY_ON_CONTROL_ERROR":
    fail("RC-01 requires fail-closed default behavior")

if state.get("release_state")!="PRE_RELEASE":
    fail("boundary freeze must not promote release state")
if state.get("enforcement_state")!="BOOTSTRAP":
    fail("boundary freeze must not promote enforcement state")

print("PASS: CDX-RC-01 capability boundary remains frozen.")
print("PASS: 131 law section IDs and canonical decision grammars unchanged.")
print("PASS: no unreserved top-level capability domain detected.")
print("PASS: release/enforcement state remains PRE_RELEASE / BOOTSTRAP.")
