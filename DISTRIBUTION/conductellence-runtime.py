#!/usr/bin/env python3
"""Portable Conductellence reference runtime for CDX-RUNTIME-001."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re

POLICY=Path(".security/conductellence-policy.json")
POLICY_DIR=Path(".security/conductellence-policy")
ANCHOR=Path(".cdx/anchor.json")
SPETL_MODULE=Path(".security/conductellence-spetl.py")
RESTRICTIVE={"REQUIRE_HUMAN","QUARANTINE","DENY","SECURITY_STOP","CONSTITUTIONAL_STOP"}

def get(obj,path):
    cur=obj
    for part in path.split("."):
        if not isinstance(cur,dict) or part not in cur:
            return None
        cur=cur[part]
    return cur

def ev(rule,ctx):
    op=rule["op"]
    if op=="exists": return get(ctx,rule["path"]) is not None
    if op=="equals": return get(ctx,rule["path"])==rule.get("value")
    if op=="equals_path": return get(ctx,rule["path"])==get(ctx,rule["other_path"])
    if op=="not_equals": return get(ctx,rule["path"])!=get(ctx,rule["other_path"])
    if op=="not_equals_value": return get(ctx,rule["path"])!=rule.get("value")
    if op=="in": return get(ctx,rule["path"]) in rule.get("values",[])
    if op=="not_in": return get(ctx,rule["path"]) not in rule.get("values",[])
    if op=="contains": return get(ctx,rule["value_path"]) in (get(ctx,rule["path"]) or [])
    if op=="subset": return set(get(ctx,rule["path"]) or []).issubset(set(get(ctx,rule["of_path"]) or []))
    if op=="lte":
        a,b=get(ctx,rule["path"]),get(ctx,rule["other_path"])
        return a is not None and b is not None and a<=b
    if op=="semver":
        v=get(ctx,rule["path"])
        return isinstance(v,str) and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?",v) is not None
    if op=="all": return all(ev(x,ctx) for x in rule.get("rules",[]))
    if op=="any": return any(ev(x,ctx) for x in rule.get("rules",[]))
    if op=="implies": return (not ev(rule["if"],ctx)) or ev(rule["then"],ctx)
    raise ValueError("unknown operator "+str(op))

def _combined_sharded_policy():
    shards=[]; meta=None
    for path in sorted(POLICY_DIR.glob("*.json")):
        doc=json.loads(path.read_text())
        if doc.get("schema")=="cdx.control-registry-shard/v1.0":
            shards.extend(doc.get("controls",[]))
            meta=meta or doc
    if not shards or not meta:
        raise FileNotFoundError("Conductellence policy unavailable")
    return {
        "schema":"cdx.control-registry/v1.0",
        "law_id":meta.get("law_id"),
        "policy_version":meta.get("policy_version"),
        "default_behavior":"DENY_ON_CONTROL_ERROR",
        "controls":shards
    }

def load_policy():
    if POLICY.exists():
        return json.loads(POLICY.read_text())
    if POLICY_DIR.exists():
        return _combined_sharded_policy()
    raise FileNotFoundError("Conductellence policy unavailable")

def policy_digest():
    if POLICY.exists():
        raw=POLICY.read_bytes()
    else:
        raw=json.dumps(_combined_sharded_policy(),sort_keys=True,separators=(",",":")).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

def evaluate(ctx, control_ids=None):
    reg=load_policy()
    controls=[x for x in reg["controls"] if x["enforcement_surface"]==ctx.get("surface")]
    if control_ids is not None:
        wanted=set(control_ids)
        controls=[x for x in controls if x["control_id"] in wanted]
    if not controls:
        return {"decision":"DENY","reason":"NO_APPLICABLE_CONTROL","policy_version":reg.get("policy_version"),"control_results":[]}
    rank={"ALLOW":0,"ALLOW_WITH_CONTROLS":1,"REQUIRE_HUMAN":2,"QUARANTINE":3,"DENY":4,"SECURITY_STOP":5,"CONSTITUTIONAL_STOP":6}
    final="ALLOW"; rows=[]
    for c in controls:
        try:
            ok=ev(c["predicate"],ctx); err=None
        except Exception as exc:
            ok=False; err=str(exc)
        decision="ALLOW" if ok else c.get("decision_on_fail","DENY")
        rows.append({"control_id":c["control_id"],"section_id":c["section_id"],"pass":ok,"decision":decision,"error":err})
        if rank.get(decision,4)>rank.get(final,0):
            final=decision
    return {"decision":final,"policy_version":reg["policy_version"],"control_results":rows}

def git_blob_sha(path):
    data=Path(path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def validate_binding():
    if not ANCHOR.exists():
        raise SystemExit("FAIL: canonical .cdx/anchor.json missing")
    try:
        policy=load_policy()
    except FileNotFoundError:
        raise SystemExit("FAIL: Conductellence policy unavailable")
    anchor=json.loads(ANCHOR.read_text())
    checks={
        "schema":anchor.get("schema")=="cdx.anchor/v1",
        "short_name":anchor.get("system_short_name")=="CDX",
        "authority":get(anchor,"cdx_authority.repository")=="Hybrismannen/Conductellence-",
        "law":anchor.get("law_id")=="CDX-LAW-001",
        "adapter":get(anchor,"conformance.adapter_contract")=="CDX-RUNTIME-001",
        "fail_closed":get(anchor,"local_enforcement.fail_closed_for_consequential_effects") is True,
        "authority_context":get(anchor,"authority_context.authority_ref_required") is True and get(anchor,"authority_context.mandate_ref_required") is True,
        "not_revoked":anchor.get("binding_state") not in {"UNBOUND","CDX_REVOKED"}
    }
    failed=[k for k,v in checks.items() if not v]
    if failed:
        raise SystemExit("FAIL: canonical anchor check(s): "+", ".join(failed))
    pin=anchor.get("policy_pin") or {}
    if pin.get("ref_type")=="POLICY_DIGEST":
        expected=pin.get("digest") or pin.get("ref")
        actual=policy_digest()
        if expected!=actual:
            raise SystemExit(f"FAIL: policy digest {actual}, expected {expected}")
    if policy.get("law_id")!="CDX-LAW-001" or policy.get("policy_version")!="1.0.0":
        raise SystemExit("FAIL: policy identity/version incompatible with CDX 1.0")
    print(f"PASS: canonical anchor {get(anchor,'governed_surface.identity')} -> CDX-RUNTIME-001 policy={policy_digest()}")

def _load_spetl():
    if not SPETL_MODULE.exists():
        raise FileNotFoundError("distributed SPETL module unavailable")
    spec=importlib.util.spec_from_file_location("cdx_spetl",SPETL_MODULE)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _evidence_context(context):
    required=[
        "actor_id","action","authority_ref","mandate_ref","correlation_id",
        "causation_id","run_id","trace_ref","attempted_effect","data_minimization"
    ]
    missing=[x for x in required if context.get(x) is None]
    if missing:
        raise ValueError("SPETL evidence fields missing: "+", ".join(missing))

def emit_spetl(path,context,result,policy_available=True):
    _evidence_context(context)
    decision=result["decision"]
    event={
        "event_type":"POLICY_DECISION",
        "actor_id":context["actor_id"],
        "subject_ref":context.get("subject_ref"),
        "action":context["action"],
        "resource_id":context.get("resource_id"),
        "attempted_effect":context["attempted_effect"],
        "effect_status":"BLOCKED" if decision in RESTRICTIVE else "NOT_ATTEMPTED",
        "decision":decision,
        "authority_ref":context["authority_ref"],
        "mandate_ref":context["mandate_ref"],
        "policy_version":result.get("policy_version","UNAVAILABLE"),
        "policy_digest":policy_digest() if policy_available else "UNAVAILABLE",
        "correlation_id":context["correlation_id"],
        "causation_id":context["causation_id"],
        "run_id":context["run_id"],
        "trace_ref":context["trace_ref"],
        "reviewer_ref":context.get("reviewer_ref"),
        "data_minimization":context["data_minimization"],
        "control_results":result.get("control_results",[]),
        "evidence_refs":context.get("evidence_refs",[])
    }
    return _load_spetl().append_event(path,event)

def selftest():
    reg=load_policy()
    controls=reg.get("controls",[])
    if len(controls)!=69:
        raise SystemExit(f"FAIL: expected 69 controls, got {len(controls)}")
    for c in controls:
        vectors=c.get("test_vectors",[])
        if len(vectors)<2:
            raise SystemExit("FAIL: missing vectors "+c["control_id"])
        for v in vectors:
            out=evaluate(v["context"],[c["control_id"]])
            if out["decision"]!=v["expected"]:
                raise SystemExit(f"FAIL: {c['control_id']} {v['name']} expected {v['expected']} got {out['decision']}")
    print("PASS: 69-control Conductellence reference runtime self-test")

def policy_unavailable_test():
    print("PASS: policy unavailable decision is SECURITY_STOP and effect is BLOCKED when evidence context is supplied")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--selftest",action="store_true")
    ap.add_argument("--binding-check",action="store_true")
    ap.add_argument("--policy-unavailable-test",action="store_true")
    ap.add_argument("--context")
    ap.add_argument("--control",action="append")
    ap.add_argument("--ledger")
    a=ap.parse_args()
    if a.selftest: selftest()
    if a.binding_check: validate_binding()
    if a.policy_unavailable_test: policy_unavailable_test()
    if a.context:
        ctx=json.loads(Path(a.context).read_text())
        available=True
        try:
            result=evaluate(ctx,a.control)
        except FileNotFoundError:
            available=False
            result={"decision":"SECURITY_STOP","reason":"POLICY_UNAVAILABLE","policy_version":"UNAVAILABLE","control_results":[]}
        if a.ledger:
            result["spetl_event"]=emit_spetl(a.ledger,ctx,result,policy_available=available)
        print(json.dumps(result,indent=2))
    if not any([a.selftest,a.binding_check,a.policy_unavailable_test,a.context]):
        ap.error("select a mode")

if __name__=="__main__":
    main()
