#!/usr/bin/env python3
"""Conductellence Household clearance audit for Legal Integrity Phases B-D.

Audit ID: AUD-CDX-CLR-LEGAL-BD-001
Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import json
import re

ORDER = Path("GOVERNANCE/orders/CDX-CLR-LEGAL-BD-001.md")
MANIFEST = Path("GOVERNANCE/household/legal-integrity-bd-manifest.json")

def fail(msg):
    print("FAIL:", msg)
    raise SystemExit(1)

for p in (ORDER, MANIFEST):
    if not p.exists():
        fail(f"missing required clearance object: {p}")

order = ORDER.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

if manifest.get("authority_ref") != "CDX-CLR-LEGAL-BD-001":
    fail("manifest authority_ref does not match clearance order")

if "AUTHORITY_REF=CDX-CLR-LEGAL-BD-001" not in order:
    fail("canonical compact audit citation missing from clearance order")

required_phrase = "Director acceptance is valid only for committed state under audit"
if required_phrase not in order:
    fail("committed-state acceptance rule missing from order")

phases = manifest.get("phases", [])
if [p.get("phase") for p in phases] != ["B", "C", "D"]:
    fail("phase sequence must be exactly B -> C -> D")

expected_states = {
    "B": "DISPATCHED",
    "C": "CLEARED_PENDING_B",
    "D": "CLEARED_PENDING_C",
}
for phase in phases:
    ph = phase["phase"]
    if phase.get("state") != expected_states[ph]:
        fail(f"unexpected bootstrap state for Phase {ph}: {phase.get('state')}")

if phases[1].get("dependency") != "B:PASS":
    fail("Phase C must depend on B:PASS")
if phases[2].get("dependency") != "C:PASS":
    fail("Phase D must depend on C:PASS")

hard = set(manifest.get("hard_stops", []))
required_hard = {
    "SECURITY_STOP",
    "CONSTITUTIONAL_STOP",
    "LEGAL_REVIEW_REQUIRED",
    "DISPUTED_SEMANTIC_EQUIVALENCE",
    "DISPUTED_APPLICABILITY",
    "CONSTITUTIONAL_AMENDMENT_REQUIRED",
    "PRIMARY_SOURCE_CONFLICT",
}
missing = required_hard - hard
if missing:
    fail(f"clearance manifest missing hard stops: {sorted(missing)}")

statement = manifest.get("audit_reference_statement", "")
if "CDX-CLR-LEGAL-BD-001" not in statement:
    fail("audit_reference_statement missing authority ID")
if "does not pre-authorize PASS" not in statement:
    fail("audit_reference_statement must deny pre-authorized PASS")

# Optional future records: if they exist, enforce authority reference and hard-stop semantics.
record_root = Path("GOVERNANCE/household/records")
if record_root.exists():
    for path in sorted(record_root.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if rec.get("programme_id") != "CDX-PROG-LEGAL-BD-001":
            continue
        if rec.get("authority_ref") != "CDX-CLR-LEGAL-BD-001":
            fail(f"{path}: wrong/missing authority_ref")
        phase = rec.get("phase")
        if phase not in {"B", "C", "D"}:
            fail(f"{path}: invalid phase")
        state = rec.get("acceptance_state")
        stops = rec.get("hard_stops", [])
        legal = rec.get("unresolved_legal_review", [])
        sha = rec.get("committed_sha")
        if state in {"PASS", "REPAIRED_PASS"}:
            if not sha:
                fail(f"{path}: PASS lacks committed_sha")
            if stops:
                fail(f"{path}: PASS with unresolved hard_stops")
            if legal:
                fail(f"{path}: PASS with unresolved legal review")
            for field in ("janitor_scan_ref", "ci_run_ref", "accepted_at"):
                if not rec.get(field):
                    fail(f"{path}: PASS lacks {field}")

print("PASS: CDX-CLR-LEGAL-BD-001 is structurally valid")
print("PASS: B -> C -> D dependency and hard-stop semantics are preserved")
print("PASS: future Household acceptance records are authority-bound when present")
