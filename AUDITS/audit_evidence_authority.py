#!/usr/bin/env python3
"""Conductellence Scientific Evidence Authority audit.

Audit ID: AUD-CDX-EVID-001
"""

from pathlib import Path
import json

ROOT=Path("EVIDENCE-AUTHORITY")
POLICY=ROOT/"provider/scite-policy.json"
PUBS=ROOT/"registry/publications.json"
CLAIMS=ROOT/"registry/claims.json"
BINDINGS=ROOT/"registry/claim-evidence-bindings.json"
DRIFT=ROOT/"registry/evidence-drift.json"

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (POLICY,PUBS,CLAIMS,BINDINGS,DRIFT):
    if not p.exists(): fail(f"missing {p}")

policy=json.loads(POLICY.read_text())
pubs=json.loads(PUBS.read_text())
claims=json.loads(CLAIMS.read_text())
bindings=json.loads(BINDINGS.read_text())
drift=json.loads(DRIFT.read_text())

if policy.get("system_id")!="CDX-EVID-001": fail("wrong evidence system id")
if policy.get("authority_state")!="EXTERNAL_EVIDENCE_PROVIDER_ONLY":
    fail("Scite must remain external evidence provider only")

budget=policy.get("budget_policy",{})
if budget.get("default_search_limit",999)>10: fail("default Scite search limit exceeds credit-efficient ceiling")
if budget.get("maximum_search_limit_without_explicit_override",999)>25:
    fail("ungated Scite search ceiling exceeds 25")
if budget.get("no_scheduled_literature_searches") is not True:
    fail("scheduled literature searches must remain disabled")
if budget.get("prefer_exact_doi_lookup") is not True or budget.get("prefer_cached_result") is not True:
    fail("DOI-first/cache-first rules missing")

for bad in (
 "scientific_evidence_equals_legal_authority",
 "scite_output_equals_legal_applicability",
 "citation_count_equals_truth"
):
    if bad not in policy.get("prohibited_inferences",[]): fail(f"missing prohibited inference {bad}")

pub_ids={p.get("publication_id") for p in pubs.get("publications",[])}
claim_ids={c.get("claim_id") for c in claims.get("claims",[])}
seen=set()
for b in bindings.get("bindings",[]):
    bid=b.get("binding_id")
    if not bid or bid in seen: fail(f"missing/duplicate binding id {bid}")
    seen.add(bid)
    if b.get("publication_id") not in pub_ids: fail(f"{bid}: unknown publication")
    if b.get("claim_id") not in claim_ids: fail(f"{bid}: unknown claim")
    if b.get("support_state")=="DIRECTLY_SUPPORTED" and b.get("review_state")!="REVIEWED":
        fail(f"{bid}: direct support requires reviewed state")
    notices=(b.get("scite_metadata") or {}).get("editorial_notices") or []
    if any(str(n.get("status","")).lower()=="retracted" for n in notices):
        if b.get("support_state") not in {"RETRACTED","DEGRADED"}:
            fail(f"{bid}: retracted source cannot remain active support")

for e in drift.get("events",[]):
    if e.get("legal_change_inferred") is True: fail("evidence drift may not infer legal change")

print("PASS: CDX-EVID-001 provider boundary is preserved")
print("PASS: Scite budget policy is DOI-first, cache-first and non-scheduled")
print(f"PASS: {len(pub_ids)} publications, {len(claim_ids)} claims and {len(seen)} bindings are internally coherent")
