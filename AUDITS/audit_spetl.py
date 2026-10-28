#!/usr/bin/env python3
from pathlib import Path
import copy
import importlib.util
import json
import tempfile

spec=importlib.util.spec_from_file_location("ledger",Path("SPETL/spetl.py"))
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def base_event(decision="ALLOW", effect_status="PERMITTED", policy_digest=None):
    if policy_digest is None:
        policy_digest="sha256:" + "a"*64
    return {
        "event_type":"POLICY_DECISION",
        "actor_id":"CDX-TEST-ACTOR",
        "subject_ref":"SUBJECT:PSEUDONYMOUS-001",
        "action":"TEST_EFFECT",
        "resource_id":"RESOURCE:FIXTURE",
        "attempted_effect":{"surface":"test","operation":"write","target_ref":"fixture"},
        "effect_status":effect_status,
        "decision":decision,
        "authority_ref":"CDX-LAW-001",
        "mandate_ref":"CDX-TEST-MANDATE-001",
        "policy_version":"1.0.0",
        "policy_digest":policy_digest,
        "correlation_id":"CORR-001",
        "causation_id":"ROOT",
        "run_id":"RUN-001",
        "trace_ref":"TRACE-001",
        "reviewer_ref":None,
        "data_minimization":{
            "personal_data_present":False,
            "redacted_fields":[],
            "rationale":"Synthetic audit fixture; no direct personal data."
        },
        "control_results":[],
        "evidence_refs":[]
    }

with tempfile.TemporaryDirectory() as td:
    p=Path(td)/"events.jsonl"
    allow=m.append_event(p,base_event())
    deny_event=base_event("DENY","BLOCKED")
    deny_event["correlation_id"]="CORR-002"
    deny_event["run_id"]="RUN-002"
    deny=m.append_event(p,deny_event)
    unavailable_event=base_event("SECURITY_STOP","BLOCKED","UNAVAILABLE")
    unavailable_event["correlation_id"]="CORR-003"
    unavailable_event["run_id"]="RUN-003"
    unavailable=m.append_event(p,unavailable_event)

    ok,count,error=m.verify(p)
    if not ok or count!=3:
        raise SystemExit("FAIL: valid ledger rejected: "+str(error))

    producer={"system_id":"CDX-SYS-001","runtime_id":"CDX-REFERENCE-RUNTIME","repository":"Hybrismannen/Conductellence-"}
    bundle=m.build_custody_bundle(p,producer,"0"*40)
    ok,error=m.verify_custody_bundle(bundle,expected_producer="CDX-REFERENCE-RUNTIME",allowed_authorities={"CDX-LAW-001"})
    if not ok:
        raise SystemExit("FAIL: valid custody bundle rejected: "+str(error))

    tampered=copy.deepcopy(bundle)
    tampered["events"][0]["action"]="TAMPERED"
    ok,error=m.verify_custody_bundle(tampered,expected_producer="CDX-REFERENCE-RUNTIME",allowed_authorities={"CDX-LAW-001"})
    if ok or "bundle_hash mismatch" not in str(error):
        raise SystemExit("FAIL: tampered bundle was not rejected")

    withheld=copy.deepcopy(bundle)
    withheld["events"]=withheld["events"][:-1]
    payload={k:v for k,v in withheld.items() if k!="bundle_hash"}
    withheld["bundle_hash"]=m.sha256_obj(payload)
    ok,error=m.verify_custody_bundle(withheld,expected_producer="CDX-REFERENCE-RUNTIME",allowed_authorities={"CDX-LAW-001"})
    if ok or "withheld evidence" not in str(error):
        raise SystemExit("FAIL: withheld evidence was not detected")

    forged=copy.deepcopy(bundle)
    forged["events"][0]["authority_ref"]="FORGED-AUTHORITY"
    event_payload={k:v for k,v in forged["events"][0].items() if k!="event_hash"}
    forged["events"][0]["event_hash"]=m.sha256_obj(event_payload)
    forged["events"][1]["previous_hash"]=forged["events"][0]["event_hash"]
    event_payload={k:v for k,v in forged["events"][1].items() if k!="event_hash"}
    forged["events"][1]["event_hash"]=m.sha256_obj(event_payload)
    forged["events"][2]["previous_hash"]=forged["events"][1]["event_hash"]
    event_payload={k:v for k,v in forged["events"][2].items() if k!="event_hash"}
    forged["events"][2]["event_hash"]=m.sha256_obj(event_payload)
    payload={k:v for k,v in forged.items() if k!="bundle_hash"}
    forged["bundle_hash"]=m.sha256_obj(payload)
    ok,error=m.verify_custody_bundle(forged,expected_producer="CDX-REFERENCE-RUNTIME",allowed_authorities={"CDX-LAW-001"})
    if ok or "untrusted authority_ref" not in str(error):
        raise SystemExit("FAIL: forged authority was not rejected")

    ok,error=m.verify_custody_bundle(bundle,expected_producer="DIFFERENT-RUNTIME",allowed_authorities={"CDX-LAW-001"})
    if ok or "unexpected producer runtime identity" not in str(error):
        raise SystemExit("FAIL: different runtime identity was not rejected")

    missing=base_event()
    del missing["trace_ref"]
    try:
        m.append_event(Path(td)/"bad.jsonl",missing)
        raise SystemExit("FAIL: missing required event field was accepted")
    except ValueError:
        pass

print("PASS: SPETL v1.1 allow/deny/policy-unavailable event semantics")
print("PASS: custody bundle tamper, withheld-evidence, forged-authority and runtime-identity negative cases")
