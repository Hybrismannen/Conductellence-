#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import tempfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("spetl",ROOT/"SPETL/spetl.py")
spetl=importlib.util.module_from_spec(spec)
spec.loader.exec_module(spetl)

MANDATE="CDX-WP04-REFERENCE-MANDATE-001"

def digest_file(path):
    return "sha256:"+hashlib.sha256(Path(path).read_bytes()).hexdigest()

def event(request_id,decision,effect_status,policy_digest,run_id):
    return {
        "event_type":"POLICY_DECISION",
        "actor_id":"CDX-REFERENCE-RUNTIME",
        "subject_ref":"SUBJECT:PSEUDONYMOUS-WP04",
        "action":"REFERENCE_EXTERNAL_EFFECT",
        "resource_id":"RESOURCE:WP04-FIXTURE",
        "attempted_effect":{"surface":"reference","operation":"write","target_ref":"fixture"},
        "effect_status":effect_status,
        "decision":decision,
        "authority_ref":"CDX-LAW-001",
        "mandate_ref":MANDATE,
        "policy_ref":"DISTRIBUTION/conductellence-policy.json",
        "policy_version":"1.0.0",
        "policy_digest":policy_digest,
        "request_id":request_id,
        "correlation_id":"CORR-WP04-"+request_id,
        "causation_id":"ROOT-WP04",
        "run_id":str(run_id),
        "trace_ref":"TRACE-WP04-"+request_id,
        "reviewer_ref":None,
        "data_minimization":{
            "personal_data_present":False,
            "redacted_fields":[],
            "rationale":"Synthetic reference evidence; only pseudonymous subject reference and control metadata are retained."
        },
        "control_results":[],
        "evidence_refs":[]
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--source-commit",required=True)
    p.add_argument("--workflow-run-id",required=True)
    p.add_argument("--workflow-run-attempt",required=True)
    args=p.parse_args()
    if len(args.source_commit)!=40:
        raise SystemExit("source commit must be a 40-character SHA")
    policy_digest=digest_file(ROOT/"DISTRIBUTION/conductellence-policy.json")
    with tempfile.TemporaryDirectory() as td:
        ledger=Path(td)/"events.jsonl"
        spetl.append_event(ledger,event("REQ-ALLOW","ALLOW","PERMITTED",policy_digest,args.workflow_run_id))
        spetl.append_event(ledger,event("REQ-DENY","DENY","BLOCKED",policy_digest,args.workflow_run_id))
        spetl.append_event(ledger,event("REQ-POLICY-UNAVAILABLE","SECURITY_STOP","BLOCKED","UNAVAILABLE",args.workflow_run_id))
        producer={
            "system_id":"CDX-SYS-001",
            "runtime_id":"CDX-REFERENCE-RUNTIME",
            "repository":"Hybrismannen/Conductellence-",
            "workflow_run_id":str(args.workflow_run_id),
            "workflow_run_attempt":str(args.workflow_run_attempt)
        }
        bundle=spetl.build_custody_bundle(ledger,producer,args.source_commit,retention_class="REFERENCE_CUSTODY_90D")
        Path(args.output).write_text(json.dumps(bundle,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"bundle_id":bundle["bundle_id"],"bundle_hash":bundle["bundle_hash"],"events":len(bundle["events"])},indent=2))

if __name__=="__main__":
    main()
