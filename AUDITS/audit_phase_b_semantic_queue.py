#!/usr/bin/env python3
"""Phase B semantic queue integrity audit.

Authority: CDX-CLR-LEGAL-BD-001
"""

from pathlib import Path
import json

MAP=Path("LEGAL-REFERENCES/paragraph-legal-map.json")
QUEUE=Path("LEGAL-REFERENCES/phase-b/semantic-review-queue.json")
PROOFS=Path("LEGAL-REFERENCES/legal-support-proofs.json")

def fail(msg):
    print("FAIL:",msg); raise SystemExit(1)

for p in (MAP,QUEUE,PROOFS):
    if not p.exists(): fail(f"missing {p}")

pm=json.loads(MAP.read_text())
q=json.loads(QUEUE.read_text())
proofs=json.loads(PROOFS.read_text()).get("proofs",[])

expected={(p["paragraph_id"],r["provision_id"]) for p in pm["paragraphs"] for r in p["references"]}
items=q.get("items",[])
actual={(x["paragraph_id"],x["provision_id"]) for x in items}

if expected!=actual:
    fail(f"semantic queue mismatch: missing={len(expected-actual)} orphan={len(actual-expected)}")
if len(items)!=len(actual):
    fail("duplicate paragraph/provision queue items")
if q.get("authority_ref")!="CDX-CLR-LEGAL-BD-001":
    fail("wrong authority_ref")

proof_keys={(p.get("paragraph_id"),p.get("provision_id"),p.get("relationship")) for p in proofs if p.get("review_state")=="VERIFIED"}
for x in items:
    state=x.get("review_state")
    if state not in {"PENDING_SEMANTIC_REVIEW","REVIEWED"}:
        fail(f"{x['queue_id']}: invalid review_state {state}")
    if q.get("state") in {"COMPLETE_PENDING_DIRECTOR_ACCEPTANCE","ACCEPTED"} and state != "REVIEWED":
        fail(f"{x['queue_id']}: completed Phase B still contains non-reviewed item")
    decision=x.get("decision")
    if decision in {"PROMOTE_DERIVED_WITH_PROOF","PROMOTE_TEXTUAL_WITH_PROOF"}:
        rel="DERIVED" if decision=="PROMOTE_DERIVED_WITH_PROOF" else "TEXTUAL"
        if (x["paragraph_id"],x["provision_id"],rel) not in proof_keys:
            fail(f"{x['queue_id']}: promotion lacks VERIFIED proof")

if q.get("state") in {"COMPLETE_PENDING_DIRECTOR_ACCEPTANCE","ACCEPTED"}:
    unresolved=[x["queue_id"] for x in items if x.get("review_state")!="REVIEWED" or not x.get("decision")]
    if unresolved:
        fail(f"completed Phase B has unresolved items: {unresolved[:20]}")
    print(f"PASS: Phase B substantive review complete for {len(items)} edges")

print(f"PASS: Phase B queue exactly covers {len(expected)} paragraph/provision edges")
print(f"PASS: {len(proof_keys)} VERIFIED stronger-support proof keys registered")
