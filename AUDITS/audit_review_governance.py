#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json

LAW=Path("CONTROL-CATALOGUE/law-bindings.json")
PROCEDURES=Path("REVIEW-CATALOGUE/procedures.json")
BINDINGS=Path("REVIEW-CATALOGUE/bindings.json")
ENGINE=Path("REVIEW-CATALOGUE/engine.py")

def fail(msg):
    print("FAIL:",msg)
    raise SystemExit(1)

for p in (LAW,PROCEDURES,BINDINGS,ENGINE):
    if not p.exists(): fail(f"missing {p}")

law=json.loads(LAW.read_text())
procedures={x["procedure_id"]:x for x in json.loads(PROCEDURES.read_text())["procedures"]}
bindings=json.loads(BINDINGS.read_text())["bindings"]

nonfull=[s for s in law["sections"] if s["auditability"]!="FULLY_AUTOMATABLE"]
if len(nonfull)!=62:
    fail(f"expected 62 non-fully-automatable sections, got {len(nonfull)}")

bmap={x["section_id"]:x for x in bindings}
if len(bmap)!=62:
    fail(f"expected 62 unique review bindings, got {len(bmap)}")

for s in nonfull:
    b=bmap.get(s["section_id"])
    if not b: fail(f"{s['section_id']}: missing review binding")
    if b["auditability"]!=s["auditability"]:
        fail(f"{s['section_id']}: auditability mismatch")
    proc=procedures.get(b["procedure_id"])
    if not proc: fail(f"{s['section_id']}: unknown procedure {b['procedure_id']}")
    if proc["applies_to"]!=s["auditability"]:
        fail(f"{s['section_id']}: procedure class mismatch")
    if proc.get("automatic_allow") is not False:
        fail(f"{proc['procedure_id']}: automatic_allow must be false")

spec=importlib.util.spec_from_file_location("review_engine",ENGINE)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

cases=[
    ({
      "section_id":"CDX-LAW-001-01-02","reviewer_class":"HUMAN_AUTHORIZED",
      "reviewer_id":"H1","authority_ref":"AUTH","evidence_refs":["E1"],"decision":"APPROVE"
    },"REVIEW_RECORD_ACCEPTED"),
    ({
      "section_id":"CDX-LAW-001-01-02","reviewer_class":"AGENT",
      "reviewer_id":"A1","authority_ref":"AUTH","evidence_refs":["E1"],"decision":"APPROVE"
    },"DENY"),
    ({
      "section_id":"CDX-LAW-001-01-01","reviewer_class":"HUMAN_AUTHORIZED",
      "reviewer_id":"H1","authority_ref":"AUTH","evidence_refs":["E1"],"decision":"APPROVE_WITH_CONTROLS"
    },"REVIEW_RECORD_ACCEPTED"),
    ({
      "section_id":"CDX-LAW-001-01-01","reviewer_class":"AGENT",
      "reviewer_id":"A1","authority_ref":"AUTH","evidence_refs":["E1"],"decision":"APPROVE"
    },"REQUIRE_HUMAN"),
    ({
      "section_id":"CDX-LAW-001-02-02","reviewer_class":"QUALIFIED_LEGAL_REVIEW",
      "reviewer_id":"L1","legal_basis_refs":["CFR-51-1"],"legal_snapshot_date":"2026-09-30",
      "decision":"LEGAL_CLEAR_WITH_CONTROLS"
    },"REVIEW_RECORD_ACCEPTED"),
    ({
      "section_id":"CDX-LAW-001-02-02","reviewer_class":"HUMAN_AUTHORIZED",
      "reviewer_id":"H1","legal_basis_refs":["CFR-51-1"],"legal_snapshot_date":"2026-09-30",
      "decision":"LEGAL_CLEAR"
    },"LEGAL_REVIEW_REQUIRED"),
    ({
      "section_id":"CDX-LAW-001-17-03","reviewer_class":"HUMAN_CONSTITUTIONAL_AUTHORITY",
      "reviewer_id":"H1","authority_ref":"HUMAN_SOVEREIGN_AUTHORITY",
      "artificial_approval":False,"decision":"CONSTITUTIONAL_APPROVE"
    },"REVIEW_RECORD_ACCEPTED"),
    ({
      "section_id":"CDX-LAW-001-17-03","reviewer_class":"HUMAN_CONSTITUTIONAL_AUTHORITY",
      "reviewer_id":"H1","authority_ref":"HUMAN_SOVEREIGN_AUTHORITY",
      "artificial_approval":True,"decision":"CONSTITUTIONAL_APPROVE"
    },"CONSTITUTIONAL_STOP")
]

for req,expected in cases:
    out=m.evaluate(req)
    if out["state"]!=expected:
        fail(f"{req['section_id']}: expected {expected}, got {out}")
    if out["state"]=="REVIEW_RECORD_ACCEPTED" and out.get("automatic_allow") is not False:
        fail(f"{req['section_id']}: accepted review record must not become automatic allow")
    if out["state"]=="ALLOW":
        fail("review engine emitted prohibited ALLOW state")

print("PASS: 62/62 non-fully-automatable §§ are review-bound")
print("PASS: review procedures preserve partial/human/legal/constitutional authority classes")
print("PASS: review engine validates decision records without autonomous ALLOW")
