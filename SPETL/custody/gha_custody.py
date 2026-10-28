#!/usr/bin/env python3
from pathlib import Path
import argparse
import datetime as dt
import importlib.util
import json
import shutil
import uuid

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("spetl",ROOT/"spetl.py")
spetl=importlib.util.module_from_spec(spec)
spec.loader.exec_module(spetl)

CUSTODY_ID="CDX-CUSTODY-GHA-001"
EXPECTED_RUNTIME="CDX-REFERENCE-RUNTIME"
EXPECTED_SYSTEM="CDX-SYS-001"
EXPECTED_REPOSITORY="Hybrismannen/Conductellence-"
EXPECTED_AUTHORITY="CDX-LAW-001"
EXPECTED_MANDATE="CDX-WP04-REFERENCE-MANDATE-001"

def fail(msg):
    raise ValueError(msg)

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verify_bundle_claims(bundle, expected_source_commit=None, expected_producer_run_id=None):
    ok,error=spetl.verify_custody_bundle(
        bundle,
        expected_producer=EXPECTED_RUNTIME,
        allowed_authorities={EXPECTED_AUTHORITY},
    )
    if not ok:
        fail(error)
    producer=bundle.get("producer",{})
    if producer.get("system_id")!=EXPECTED_SYSTEM:
        fail("unexpected producer system identity")
    if producer.get("repository")!=EXPECTED_REPOSITORY:
        fail("unexpected producer repository")
    if expected_producer_run_id is not None and str(producer.get("workflow_run_id"))!=str(expected_producer_run_id):
        fail("producer workflow run identity mismatch")
    if expected_source_commit is not None and bundle.get("source_commit")!=expected_source_commit:
        fail("source commit mismatch")
    events=bundle.get("events",[])
    for idx,event in enumerate(events):
        if event.get("mandate_ref")!=EXPECTED_MANDATE:
            fail(f"event {idx}: unexpected mandate_ref")
        if event.get("authority_ref")!=EXPECTED_AUTHORITY:
            fail(f"event {idx}: unexpected authority_ref")
        if not event.get("correlation_id") or not event.get("causation_id"):
            fail(f"event {idx}: request/correlation provenance missing")
        if not event.get("policy_version") or not event.get("policy_digest"):
            fail(f"event {idx}: policy pin/digest missing")
        if event.get("data_minimization",{}).get("personal_data_present") is not False:
            fail(f"event {idx}: direct personal data is prohibited in reference custody")
    return events

def receive(bundle_path,out_dir,expected_source_commit,expected_producer_run_id,custody_run_id,custody_run_attempt):
    bundle=load_json(bundle_path)
    events=verify_bundle_claims(bundle,expected_source_commit,expected_producer_run_id)
    out=Path(out_dir)
    out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(bundle_path,out/"evidence-bundle.json")
    receipt={
        "schema":"cdx.spetl.gha-custody-receipt/v1.0",
        "receipt_id":"CDX-GHA-RCPT-"+uuid.uuid4().hex.upper(),
        "custody_id":CUSTODY_ID,
        "received_at":dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_commit":bundle["source_commit"],
        "producer_workflow_run_id":str(expected_producer_run_id),
        "custody_workflow_run_id":str(custody_run_id),
        "custody_workflow_run_attempt":str(custody_run_attempt),
        "bundle_id":bundle["bundle_id"],
        "bundle_hash":bundle["bundle_hash"],
        "event_count":len(events),
        "first_event_hash":events[0]["event_hash"],
        "last_event_hash":events[-1]["event_hash"],
        "retention_days":90,
        "storage_principal":"GITHUB_ACTIONS_ARTIFACT_SERVICE",
        "trust_separation":{
            "separate_workflow_run":True,
            "custodian_executes_producer_code":False,
            "trusted_code_ref":"refs/heads/main",
            "repository_write_permission":False,
        },
    }
    receipt["receipt_hash"]=spetl.sha256_obj(receipt)
    (out/"custody-receipt.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

def verify_package(package_dir,expected_custody_run_id=None):
    root=Path(package_dir)
    bundle_path=root/"evidence-bundle.json"
    receipt_path=root/"custody-receipt.json"
    if not bundle_path.exists():
        fail("EVIDENCE_LOSS: evidence-bundle.json missing")
    if not receipt_path.exists():
        fail("EVIDENCE_LOSS: custody-receipt.json missing")
    bundle=load_json(bundle_path)
    receipt=load_json(receipt_path)
    events=verify_bundle_claims(bundle)
    claimed=receipt.get("receipt_hash")
    payload={k:v for k,v in receipt.items() if k!="receipt_hash"}
    if spetl.sha256_obj(payload)!=claimed:
        fail("custody receipt hash mismatch")
    if receipt.get("custody_id")!=CUSTODY_ID:
        fail("wrong custody id")
    if receipt.get("bundle_id")!=bundle.get("bundle_id") or receipt.get("bundle_hash")!=bundle.get("bundle_hash"):
        fail("receipt is not bound to custody bundle")
    if receipt.get("event_count")!=len(events):
        fail("receipt event count mismatch")
    if receipt.get("first_event_hash")!=events[0]["event_hash"] or receipt.get("last_event_hash")!=events[-1]["event_hash"]:
        fail("receipt event boundary hash mismatch")
    if expected_custody_run_id is not None and str(receipt.get("custody_workflow_run_id"))!=str(expected_custody_run_id):
        fail("custody workflow run identity mismatch")
    if receipt.get("storage_principal")!="GITHUB_ACTIONS_ARTIFACT_SERVICE":
        fail("unexpected storage principal")
    if receipt.get("retention_days")!=90:
        fail("unexpected reference retention")
    return bundle,receipt

def write_report(package_dir,report_path,expected_custody_run_id,verifier_run_id,verifier_run_attempt):
    bundle,receipt=verify_package(package_dir,expected_custody_run_id)
    report={
        "schema":"cdx.spetl.gha-custody-verification/v1.0",
        "verification_id":"CDX-GHA-VERIFY-"+uuid.uuid4().hex.upper(),
        "verified_at":dt.datetime.now(dt.timezone.utc).isoformat(),
        "status":"PASS",
        "custody_id":CUSTODY_ID,
        "custody_workflow_run_id":str(expected_custody_run_id),
        "verifier_workflow_run_id":str(verifier_run_id),
        "verifier_workflow_run_attempt":str(verifier_run_attempt),
        "source_commit":bundle["source_commit"],
        "bundle_id":bundle["bundle_id"],
        "bundle_hash":bundle["bundle_hash"],
        "receipt_hash":receipt["receipt_hash"],
        "event_count":receipt["event_count"],
    }
    report["report_hash"]=spetl.sha256_obj(report)
    Path(report_path).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    r=sub.add_parser("receive")
    r.add_argument("bundle")
    r.add_argument("out_dir")
    r.add_argument("--expected-source-commit",required=True)
    r.add_argument("--expected-producer-run-id",required=True)
    r.add_argument("--custody-run-id",required=True)
    r.add_argument("--custody-run-attempt",required=True)
    v=sub.add_parser("verify")
    v.add_argument("package_dir")
    v.add_argument("--expected-custody-run-id",required=True)
    v.add_argument("--report",required=True)
    v.add_argument("--verifier-run-id",required=True)
    v.add_argument("--verifier-run-attempt",required=True)
    args=p.parse_args()
    try:
        if args.cmd=="receive":
            out=receive(args.bundle,args.out_dir,args.expected_source_commit,args.expected_producer_run_id,args.custody_run_id,args.custody_run_attempt)
        else:
            out=write_report(args.package_dir,args.report,args.expected_custody_run_id,args.verifier_run_id,args.verifier_run_attempt)
        print(json.dumps(out,indent=2))
    except Exception as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)},indent=2))
        raise SystemExit(1)

if __name__=="__main__":
    main()
