#!/usr/bin/env python3
"""Terminal CDX 1.0 programme acceptance audit.

Validates final programme acceptance without conflating canonical governance
completion with downstream consequential runtime enforcement.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def fail(message):
    print("FAIL:", message)
    raise SystemExit(1)

state = load("GOVERNANCE/system-state.json")
ledger = load("PROGRAMME/CDX-1.0-WORK-PACKAGE-LEDGER.json")
residual = load("GOVERNANCE/CDX-1.0-RESIDUAL-OBLIGATIONS.json")
anchors = load("ESTATE-REGISTRY/cdx-anchors.json")
registry = load("ESTATE-REGISTRY/registry-v2.json")
wp14 = load("ESTATE-REGISTRY/wp14-estate-propagation-closure-evidence.json")

expected_axes = {
    "constitutional_state": "ADOPTED",
    "core_runtime_state": "VERIFIED_REFERENCE_RUNTIME",
    "release_state": "RELEASED",
    "estate_integration_state": "BINDINGS_IN_PROGRESS",
    "enforcement_state": "BOOTSTRAP",
}
for key, expected in expected_axes.items():
    if state.get(key) != expected:
        fail(f"{key}: expected {expected}, found {state.get(key)}")

wp15 = state.get("wp15_final_programme_acceptance", {})
if wp15.get("state") != "COMPLETE_FINAL_PROGRAMME_ACCEPTANCE":
    fail("WP15 final acceptance missing")
if wp15.get("verified_runtime_bound_claim") is not False:
    fail("WP15 must not claim VERIFIED_RUNTIME_BOUND")
if wp15.get("enforcing_claim") is not False:
    fail("WP15 must not claim ENFORCING")

closure = state.get("programme_closure", {})
if closure.get("state") != "FINAL_ACCEPTED_WITH_RESIDUAL_DOWNSTREAM_OBLIGATIONS":
    fail("programme closure is not final accepted")
if closure.get("final_work_package") != "WP15":
    fail("WP15 is not recorded as final work package")

summary = ledger.get("completion_summary", {})
if summary != {
    "total_work_packages": 16,
    "complete": 15,
    "transferred_residual_obligation": 1,
    "abandoned": 0,
    "cancelled": 0,
}:
    fail(f"work-package summary mismatch: {summary}")

rows = {x.get("work_package"): x for x in ledger.get("work_packages", [])}
if len(rows) != 16:
    fail("work-package ledger must contain exactly WP00-WP15")
for n in range(16):
    wp = f"WP{n:02d}"
    if wp not in rows:
        fail(f"missing {wp} from final ledger")
if rows["WP11"].get("state") != "TRANSFERRED_RESIDUAL_OBLIGATION":
    fail("WP11 must remain transferred residual obligation")
for wp, row in rows.items():
    if wp != "WP11" and row.get("state") != "COMPLETE":
        fail(f"{wp} must be complete in terminal ledger")

obligations = {x.get("id"): x for x in residual.get("obligations", [])}
required = {
    "CDX-RESIDUAL-RUNTIME-001": "OPEN",
    "CDX-RESIDUAL-WP11-FFOS-001": "OPEN",
    "CDX-RESIDUAL-METADATA-001": "OPEN_NON_BLOCKING",
}
for oid, expected in required.items():
    if obligations.get(oid, {}).get("state") != expected:
        fail(f"{oid}: residual state mismatch")
if len(obligations) != 3:
    fail("terminal residual register must contain exactly three classified obligations")

records = registry.get("records", [])
governed = [x for x in records if x.get("record_kind") == "CURRENT_REPOSITORY" and x.get("applicability") == "GOVERNED_APPLICABLE"]
entries = {x.get("repository"): x for x in anchors.get("entries", [])}
if len(governed) != 28:
    fail("governed repository count must remain 28")
for rec in governed:
    repo = rec.get("repository_identifier")
    entry = entries.get(repo, {})
    if entry.get("anchor_state") != "CDX_BOUND" or entry.get("anchor_verification_state") != "PASS":
        fail(f"{repo}: terminal anchor state must remain CDX_BOUND / PASS")
if anchors.get("pending_admissions"):
    fail("terminal state must have zero pending admissions")

if wp14.get("result", {}).get("governance_propagation_closure") != "PASS":
    fail("WP14 propagation closure evidence not PASS")
if wp14.get("runtime_boundary", {}).get("consequential_verified_runtime_count") != 0:
    fail("terminal state must not invent verified consequential runtimes")

blockers = set(state.get("estate_enforcement_blockers", []))
for blocker in {"CDX-BLOCK-ESTATE-RUNTIME-001", "CDX-BLOCK-WP11-FFOS-EXECUTION-001"}:
    if blocker not in blockers:
        fail(f"required residual blocker missing: {blocker}")

print("PASS: CDX 1.0 terminal programme acceptance is internally consistent.")
print("PASS: WP00-WP10 and WP12-WP15 are complete; WP11 is preserved as transferred residual obligation.")
print("PASS: 28/28 governed repositories remain CDX_BOUND / PASS with zero pending admissions.")
print("PASS: runtime and enforcement axes remain BINDINGS_IN_PROGRESS / BOOTSTRAP with zero false consequential-runtime claims.")
