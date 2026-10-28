#!/usr/bin/env python3
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import uuid

SCHEMA_VERSION = "1.1"
DECISIONS = {
    "ALLOW", "ALLOW_WITH_CONTROLS", "REQUIRE_HUMAN", "QUARANTINE",
    "DENY", "SECURITY_STOP", "CONSTITUTIONAL_STOP"
}
EFFECT_STATUSES = {"NOT_ATTEMPTED", "PERMITTED", "BLOCKED", "FAILED"}
REQUIRED_INPUT_FIELDS = {
    "event_type", "actor_id", "subject_ref", "action", "attempted_effect",
    "effect_status", "decision", "authority_ref", "mandate_ref",
    "policy_ref", "policy_version", "policy_digest", "request_id", "correlation_id", "causation_id",
    "run_id", "trace_ref", "reviewer_ref", "data_minimization",
    "control_results", "evidence_refs"
}
REQUIRED_STORED_FIELDS = REQUIRED_INPUT_FIELDS | {
    "schema_version", "event_id", "recorded_at", "previous_hash", "event_hash"
}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_obj(obj):
    return "sha256:" + hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()

def _require_string(event, key, allow_unavailable=False):
    value = event.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    if key == "policy_digest" and not allow_unavailable:
        if not value.startswith("sha256:") or len(value) != 71:
            raise ValueError("policy_digest must be sha256:<64 hex> or UNAVAILABLE")

def validate_event(event, stored=False):
    if not isinstance(event, dict):
        raise ValueError("event must be an object")
    required = REQUIRED_STORED_FIELDS if stored else REQUIRED_INPUT_FIELDS
    missing = sorted(k for k in required if k not in event)
    if missing:
        raise ValueError("missing required SPETL field(s): " + ", ".join(missing))

    if stored and event.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported schema_version")
    if event.get("decision") not in DECISIONS:
        raise ValueError("invalid decision")
    if event.get("effect_status") not in EFFECT_STATUSES:
        raise ValueError("invalid effect_status")

    for key in (
        "event_type", "actor_id", "action", "authority_ref", "mandate_ref",
        "policy_ref", "policy_version", "request_id", "correlation_id", "causation_id", "run_id", "trace_ref"
    ):
        _require_string(event, key)

    policy_digest = event.get("policy_digest")
    if policy_digest != "UNAVAILABLE":
        _require_string(event, "policy_digest")
        try:
            int(policy_digest[7:], 16)
        except ValueError as exc:
            raise ValueError("policy_digest must contain hexadecimal sha256") from exc

    attempted = event.get("attempted_effect")
    if not isinstance(attempted, dict):
        raise ValueError("attempted_effect must be an object")
    for key in ("surface", "operation"):
        if not isinstance(attempted.get(key), str) or not attempted.get(key):
            raise ValueError(f"attempted_effect.{key} must be non-empty")
    if "target_ref" not in attempted:
        raise ValueError("attempted_effect.target_ref is required")

    minimization = event.get("data_minimization")
    if not isinstance(minimization, dict):
        raise ValueError("data_minimization must be an object")
    if not isinstance(minimization.get("personal_data_present"), bool):
        raise ValueError("data_minimization.personal_data_present must be boolean")
    if not isinstance(minimization.get("redacted_fields"), list):
        raise ValueError("data_minimization.redacted_fields must be an array")
    if not isinstance(minimization.get("rationale"), str) or not minimization.get("rationale"):
        raise ValueError("data_minimization.rationale must be non-empty")

    if not isinstance(event.get("control_results"), list):
        raise ValueError("control_results must be an array")
    if not isinstance(event.get("evidence_refs"), list):
        raise ValueError("evidence_refs must be an array")

    decision = event.get("decision")
    effect_status = event.get("effect_status")
    deny_like = {"DENY", "REQUIRE_HUMAN", "QUARANTINE", "SECURITY_STOP", "CONSTITUTIONAL_STOP"}
    allow_like = {"ALLOW", "ALLOW_WITH_CONTROLS"}
    if effect_status == "PERMITTED" and decision not in allow_like:
        raise ValueError("non-allow decision cannot have PERMITTED effect_status")
    if decision in deny_like and effect_status == "PERMITTED":
        raise ValueError("deny/stop decision cannot permit an effect")
    if decision in allow_like and effect_status == "BLOCKED":
        raise ValueError("allow decision cannot report BLOCKED effect_status")
    if policy_digest == "UNAVAILABLE":
        if decision not in {"SECURITY_STOP", "DENY"}:
            raise ValueError("unavailable policy must fail closed")
        if effect_status not in {"BLOCKED", "NOT_ATTEMPTED"}:
            raise ValueError("unavailable policy cannot permit or execute an effect")

    if stored:
        _require_string(event, "event_id")
        _require_string(event, "recorded_at")
        if event.get("previous_hash") is not None and not str(event.get("previous_hash")).startswith("sha256:"):
            raise ValueError("previous_hash is invalid")
        if not str(event.get("event_hash", "")).startswith("sha256:"):
            raise ValueError("event_hash is invalid")

    return True

def append_event(path, event):
    validate_event(event, stored=False)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    previous = None
    if p.exists():
        rows = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        if rows:
            previous = json.loads(rows[-1]).get("event_hash")
    e = dict(event)
    e.setdefault("schema_version", SCHEMA_VERSION)
    e.setdefault("event_id", "CDX-EVT-" + uuid.uuid4().hex.upper())
    e.setdefault("recorded_at", dt.datetime.now(dt.timezone.utc).isoformat())
    e["previous_hash"] = previous
    payload = {k: v for k, v in e.items() if k != "event_hash"}
    e["event_hash"] = sha256_obj(payload)
    validate_event(e, stored=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(canonical(e) + "\n")
    return e

def verify(path):
    p = Path(path)
    if not p.exists():
        return True, 0, None
    previous = None
    count = 0
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        original = json.loads(line)
        try:
            validate_event(original, stored=True)
        except ValueError as exc:
            return False, count, str(exc)
        claimed = original.get("event_hash")
        payload = {k: v for k, v in original.items() if k != "event_hash"}
        if payload.get("previous_hash") != previous:
            return False, count, "previous_hash mismatch"
        calc = sha256_obj(payload)
        if calc != claimed:
            return False, count, "event_hash mismatch"
        previous = claimed
        count += 1
    return True, count, None

def build_custody_bundle(path, producer, source_commit, retention_class="CDX_AUDIT_EVIDENCE"):
    ok, count, error = verify(path)
    if not ok or count == 0:
        raise ValueError(f"cannot bundle invalid/empty ledger: {error or 'empty'}")
    events = [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    bundle = {
        "schema": "cdx.spetl.custody-bundle/v1.0",
        "bundle_id": "CDX-BUNDLE-" + uuid.uuid4().hex.upper(),
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "producer": producer,
        "source_commit": source_commit,
        "expected_event_ids": [e["event_id"] for e in events],
        "events": events,
        "retention": {
            "class": retention_class,
            "deletion_mode": "GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION"
        }
    }
    bundle["bundle_hash"] = sha256_obj(bundle)
    return bundle

def verify_custody_bundle(bundle, expected_producer=None, allowed_authorities=None):
    if not isinstance(bundle, dict) or bundle.get("schema") != "cdx.spetl.custody-bundle/v1.0":
        return False, "invalid bundle schema"
    claimed = bundle.get("bundle_hash")
    if not isinstance(claimed, str):
        return False, "missing bundle_hash"
    payload = {k: v for k, v in bundle.items() if k != "bundle_hash"}
    if sha256_obj(payload) != claimed:
        return False, "bundle_hash mismatch"

    producer = bundle.get("producer")
    if not isinstance(producer, dict):
        return False, "producer missing"
    for key in ("system_id", "runtime_id", "repository"):
        if not isinstance(producer.get(key), str) or not producer.get(key):
            return False, f"producer.{key} missing"
    if expected_producer and producer.get("runtime_id") != expected_producer:
        return False, "unexpected producer runtime identity"

    events = bundle.get("events")
    if not isinstance(events, list) or not events:
        return False, "events missing"
    previous = None
    seen = set()
    for idx, event in enumerate(events):
        try:
            validate_event(event, stored=True)
        except ValueError as exc:
            return False, f"event {idx}: {exc}"
        if event.get("previous_hash") != previous:
            return False, f"event {idx}: previous_hash mismatch"
        payload_event = {k: v for k, v in event.items() if k != "event_hash"}
        if sha256_obj(payload_event) != event.get("event_hash"):
            return False, f"event {idx}: event_hash mismatch"
        if allowed_authorities is not None and event.get("authority_ref") not in allowed_authorities:
            return False, f"event {idx}: untrusted authority_ref"
        seen.add(event["event_id"])
        previous = event["event_hash"]

    expected = set(bundle.get("expected_event_ids") or [])
    missing = sorted(expected - seen)
    if missing:
        return False, "withheld evidence: " + ", ".join(missing)

    retention = bundle.get("retention")
    if not isinstance(retention, dict) or retention.get("deletion_mode") != "GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION":
        return False, "invalid retention/deletion mode"
    return True, None

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("append")
    a.add_argument("ledger")
    a.add_argument("event_json")
    v = sub.add_parser("verify")
    v.add_argument("ledger")
    b = sub.add_parser("bundle")
    b.add_argument("ledger")
    b.add_argument("output")
    b.add_argument("--system-id", required=True)
    b.add_argument("--runtime-id", required=True)
    b.add_argument("--repository", required=True)
    b.add_argument("--source-commit", required=True)
    vb = sub.add_parser("verify-bundle")
    vb.add_argument("bundle")
    vb.add_argument("--expected-producer")
    args = p.parse_args()

    if args.cmd == "append":
        print(json.dumps(append_event(args.ledger, json.loads(Path(args.event_json).read_text())), indent=2))
    elif args.cmd == "verify":
        ok, n, err = verify(args.ledger)
        print(json.dumps({"valid": ok, "events": n, "error": err}, indent=2))
        raise SystemExit(0 if ok else 1)
    elif args.cmd == "bundle":
        producer = {"system_id": args.system_id, "runtime_id": args.runtime_id, "repository": args.repository}
        bundle = build_custody_bundle(args.ledger, producer, args.source_commit)
        Path(args.output).write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"bundle_id": bundle["bundle_id"], "bundle_hash": bundle["bundle_hash"]}, indent=2))
    else:
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        ok, err = verify_custody_bundle(bundle, expected_producer=args.expected_producer)
        print(json.dumps({"valid": ok, "error": err}, indent=2))
        raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
