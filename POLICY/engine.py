#!/usr/bin/env python3
"""Conductellence deterministic policy engine.

Reference runtime for CDX fully-automatable controls.
Unknown/malformed control evaluation fails closed.
"""
from pathlib import Path
import argparse, json, re

REG=Path("POLICY/control-registry.json")
DECISIONS={"ALLOW","ALLOW_WITH_CONTROLS","REQUIRE_HUMAN","QUARANTINE","DENY","SECURITY_STOP","CONSTITUTIONAL_STOP"}

def get(obj,path):
    cur=obj
    for p in path.split("."):
        if not isinstance(cur,dict) or p not in cur: return None
        cur=cur[p]
    return cur

def eval_rule(rule,ctx):
    op=rule["op"]
    if op=="exists": return get(ctx,rule["path"]) is not None
    if op=="equals": return get(ctx,rule["path"])==rule.get("value")
    if op=="equals_path": return get(ctx,rule["path"])==get(ctx,rule["other_path"])
    if op=="not_equals": return get(ctx,rule["path"])!=get(ctx,rule["other_path"])
    if op=="not_equals_value": return get(ctx,rule["path"])!=rule.get("value")
    if op=="in": return get(ctx,rule["path"]) in rule.get("values",[])
    if op=="not_in": return get(ctx,rule["path"]) not in rule.get("values",[])
    if op=="contains":
        seq=get(ctx,rule["path"]) or []
        val=get(ctx,rule["value_path"])
        return val in seq
    if op=="subset":
        a=set(get(ctx,rule["path"]) or [])
        b=set(get(ctx,rule["of_path"]) or [])
        return a.issubset(b)
    if op=="lte":
        a=get(ctx,rule["path"]); b=get(ctx,rule["other_path"])
        return a is not None and b is not None and a<=b
    if op=="semver":
        v=get(ctx,rule["path"])
        return isinstance(v,str) and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?",v) is not None
    if op=="all": return all(eval_rule(r,ctx) for r in rule.get("rules",[]))
    if op=="any": return any(eval_rule(r,ctx) for r in rule.get("rules",[]))
    if op=="implies": return (not eval_rule(rule["if"],ctx)) or eval_rule(rule["then"],ctx)
    raise ValueError("unknown operator "+str(op))

def evaluate(context, control_ids=None):
    reg=json.loads(REG.read_text())
    controls=[c for c in reg["controls"] if c["enforcement_surface"]==context.get("surface")]
    if control_ids is not None:
        wanted=set(control_ids); controls=[c for c in controls if c["control_id"] in wanted]
    if not controls:
        return {"decision":"DENY","reason":"NO_APPLICABLE_CONTROL","control_results":[]}
    results=[]; final="ALLOW"
    for c in controls:
        try: ok=eval_rule(c["predicate"],context); err=None
        except Exception as exc: ok=False; err=str(exc)
        decision="ALLOW" if ok else c.get("decision_on_fail","DENY")
        results.append({"control_id":c["control_id"],"section_id":c["section_id"],"pass":ok,"decision":decision,"error":err})
        if decision=="CONSTITUTIONAL_STOP": final="CONSTITUTIONAL_STOP"
        elif decision=="SECURITY_STOP" and final!="CONSTITUTIONAL_STOP": final="SECURITY_STOP"
        elif decision=="DENY" and final not in {"CONSTITUTIONAL_STOP","SECURITY_STOP"}: final="DENY"
        elif decision=="REQUIRE_HUMAN" and final=="ALLOW": final="REQUIRE_HUMAN"
    return {"decision":final,"policy_version":reg["policy_version"],"control_results":results}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("context_json"); ap.add_argument("--control",action="append")
    a=ap.parse_args(); ctx=json.loads(Path(a.context_json).read_text())
    print(json.dumps(evaluate(ctx,a.control),indent=2))
if __name__=="__main__": main()
