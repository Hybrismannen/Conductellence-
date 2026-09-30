#!/usr/bin/env python3
from pathlib import Path
import argparse,json

PROCEDURES=Path("REVIEW-CATALOGUE/procedures.json")
BINDINGS=Path("REVIEW-CATALOGUE/bindings.json")

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def evaluate(request):
    procedures={x["procedure_id"]:x for x in load(PROCEDURES)["procedures"]}
    bindings={x["section_id"]:x for x in load(BINDINGS)["bindings"]}

    sid=request.get("section_id")
    binding=bindings.get(sid)
    if not binding:
        return {"state":"DENY","reason":"NO_REVIEW_BINDING","section_id":sid}

    proc=procedures.get(binding["procedure_id"])
    if not proc:
        return {"state":"DENY","reason":"MISSING_REVIEW_PROCEDURE","section_id":sid}

    required_class=proc["required_reviewer_class"]
    reviewer_class=request.get("reviewer_class")
    if reviewer_class!=required_class:
        return {
            "state":proc["fail_state"],
            "reason":"REVIEWER_CLASS_MISMATCH",
            "required_reviewer_class":required_class,
            "section_id":sid,
            "procedure_id":proc["procedure_id"]
        }

    if not request.get("reviewer_id"):
        return {"state":proc["fail_state"],"reason":"REVIEWER_ID_MISSING","section_id":sid,"procedure_id":proc["procedure_id"]}

    decision=request.get("decision")
    if decision not in proc["valid_decisions"]:
        return {"state":proc["fail_state"],"reason":"INVALID_OR_MISSING_DECISION","section_id":sid,"procedure_id":proc["procedure_id"]}

    if binding["auditability"] in {"PARTIALLY_AUTOMATABLE","HUMAN_REVIEW_REQUIRED"}:
        if not request.get("authority_ref"):
            return {"state":proc["fail_state"],"reason":"AUTHORITY_REF_MISSING","section_id":sid,"procedure_id":proc["procedure_id"]}
        if not request.get("evidence_refs"):
            return {"state":proc["fail_state"],"reason":"EVIDENCE_MISSING","section_id":sid,"procedure_id":proc["procedure_id"]}

    if binding["auditability"]=="LEGAL_REVIEW_REQUIRED":
        if not request.get("legal_basis_refs"):
            return {"state":"LEGAL_REVIEW_REQUIRED","reason":"LEGAL_BASIS_MISSING","section_id":sid,"procedure_id":proc["procedure_id"]}
        if not request.get("legal_snapshot_date"):
            return {"state":"LEGAL_REVIEW_REQUIRED","reason":"LEGAL_SNAPSHOT_MISSING","section_id":sid,"procedure_id":proc["procedure_id"]}

    if binding["auditability"]=="CONSTITUTIONAL_HUMAN_ONLY":
        if request.get("artificial_approval") is not False:
            return {"state":"CONSTITUTIONAL_STOP","reason":"ARTIFICIAL_APPROVAL_PROHIBITED","section_id":sid,"procedure_id":proc["procedure_id"]}
        if not request.get("authority_ref"):
            return {"state":"CONSTITUTIONAL_STOP","reason":"AUTHORITY_REF_MISSING","section_id":sid,"procedure_id":proc["procedure_id"]}

    return {
        "state":"REVIEW_RECORD_ACCEPTED",
        "section_id":sid,
        "procedure_id":proc["procedure_id"],
        "reviewer_class":reviewer_class,
        "reviewer_id":request["reviewer_id"],
        "decision":decision,
        "automatic_allow":False
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("request_json")
    a=p.parse_args()
    print(json.dumps(evaluate(load(a.request_json)),indent=2))

if __name__=="__main__":
    main()
