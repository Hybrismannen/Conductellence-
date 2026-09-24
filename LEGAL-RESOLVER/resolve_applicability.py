#!/usr/bin/env python3
"""Conductellence fail-safe legal applicability resolver.
Authority: CDX-CLR-LEGAL-BD-001
Phase: C

Resolution order:
1) instrument scope;
2) temporal applicability;
3) provision-specific condition.

Citation presence, semantic relevance, model confidence, or missing facts never create APPLIES.
"""

from pathlib import Path
import argparse, datetime as dt, json

PROVISIONS=Path("LEGAL-REFERENCES/legal-provision-registry.json")
PROFILES=Path("LEGAL-RESOLVER/scope-profiles.json")
TEMPORAL=Path("REGULATORY-DRIFT/provision-temporal-state.json")

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def d(v): return dt.date.fromisoformat(v)

def profile_for(pid, profiles):
    m=[p for p in profiles if pid.startswith(p["provision_prefix"])]
    return m[0] if len(m)==1 else None

def match(when,facts):
    missing=[]
    for k,v in when.items():
        if k not in facts or facts.get(k) is None:
            missing.append(k); continue
        if facts.get(k)!=v: return False,missing
    return len(missing)==0,missing

def resolve_scope(profile,facts):
    if facts.get("legal_conflict") is True or facts.get("disputed_classification") is True:
        return {"result":"LEGAL_REVIEW_REQUIRED","reasoning_state":"CONFLICT","rule_id":None,"source_refs":[],"reasoning_summary":"Disputed legal classification or conflict."}
    matches=[]
    for rule in profile.get("outcomes",[]):
        ok,_=match(rule.get("when",{}),facts)
        if ok: matches.append(rule)
    if matches:
        results={r["result"] for r in matches}
        if len(results)>1:
            return {"result":"LEGAL_REVIEW_REQUIRED","reasoning_state":"CONFLICT","rule_id":None,"source_refs":sorted({x for r in matches for x in r.get("source_refs",[])}),"reasoning_summary":"Multiple exact scope rules match with conflicting results."}
        rule=sorted(matches,key=lambda r:len(r.get("when",{})),reverse=True)[0]
        return {"result":rule["result"],"reasoning_state":"DETERMINISTIC_SCOPE_RULE","rule_id":rule["rule_id"],"source_refs":rule.get("source_refs",[]),"reasoning_summary":rule.get("reason","Exact registered scope rule matched supplied facts.")}
    missing=[k for k in profile.get("required_facts",[]) if k not in facts or facts.get(k) is None]
    if missing:
        return {"result":"UNKNOWN","reasoning_state":"MISSING_FACTS","rule_id":None,"source_refs":profile.get("scope_sources",[]),"reasoning_summary":"Missing scope facts: "+", ".join(sorted(missing))}
    return {"result":"UNKNOWN","reasoning_state":"NO_MATCHING_SCOPE_RULE","rule_id":None,"source_refs":profile.get("scope_sources",[]),"reasoning_summary":"No admitted deterministic scope rule matches the supplied facts."}

def resolve_temporal(pid,snapshot,facts,tmap):
    rec=tmap.get(pid)
    if not rec:
        return {"result":"UNKNOWN","reasoning_state":"NO_TEMPORAL_RULE","source_refs":[],"reasoning_summary":"No temporal rule exists for this exact provision."}
    snap=d(snapshot); mode=rec.get("mode")
    if mode=="FIXED_DATE":
        eff=d(rec["effective_from"])
        return {"result":"APPLIES" if snap>=eff else "DOES_NOT_APPLY","reasoning_state":"TEMPORALLY_APPLICABLE" if snap>=eff else "NOT_YET_APPLICABLE","source_refs":rec.get("source_refs",[]),"reasoning_summary":f"Effective from {eff.isoformat()}."}
    if mode=="AI_HIGH_RISK_SPLIT":
        basis=facts.get("high_risk_basis")
        if not basis:
            return {"result":"UNKNOWN","reasoning_state":"MISSING_FACTS","source_refs":sorted({x for b in rec.get("branches",[]) for x in b.get("source_refs",[])}),"reasoning_summary":"high_risk_basis is required."}
        branches=[b for b in rec.get("branches",[]) if b.get("high_risk_basis")==basis]
        if len(branches)!=1:
            return {"result":"LEGAL_REVIEW_REQUIRED","reasoning_state":"UNRECOGNISED_HIGH_RISK_BASIS","source_refs":sorted({x for b in rec.get("branches",[]) for x in b.get("source_refs",[])}),"reasoning_summary":"High-risk basis is not an admitted temporal branch."}
        b=branches[0]; eff=d(b["effective_from"])
        return {"result":"APPLIES" if snap>=eff else "DOES_NOT_APPLY","reasoning_state":"TEMPORALLY_APPLICABLE" if snap>=eff else "NOT_YET_APPLICABLE","source_refs":b.get("source_refs",[]),"reasoning_summary":f"Branch effective from {eff.isoformat()}."}
    if mode=="DIRECTIVE_TRANSPOSITION":
        eff=d(rec["effective_from"])
        if snap<eff:
            return {"result":"DOES_NOT_APPLY","reasoning_state":"PRE_TRANSPOSITION_APPLICATION_DATE","source_refs":rec.get("source_refs",[]),"reasoning_summary":f"Snapshot predates {eff.isoformat()}."}
        return {"result":"CONDITIONAL","reasoning_state":"NATIONAL_IMPLEMENTATION_REQUIRED","source_refs":rec.get("source_refs",[]),"reasoning_summary":"Directive is temporally operative; entity-facing applicability requires national implementation."}
    if mode=="IN_FORCE_REFERENCE":
        eff=d(rec["effective_from"])
        return {"result":"APPLIES" if snap>=eff else "DOES_NOT_APPLY","reasoning_state":"IN_FORCE_REFERENCE" if snap>=eff else "NOT_YET_IN_FORCE","source_refs":rec.get("source_refs",[]),"reasoning_summary":rec.get("note") or ""}
    if mode=="CURRENT_CONSOLIDATED_TEXT":
        eff=d(rec["effective_from"])
        if snap<eff:
            return {"result":"LEGAL_REVIEW_REQUIRED","reasoning_state":"HISTORICAL_VERSION_REQUIRED","source_refs":rec.get("source_refs",[]),"reasoning_summary":"Snapshot predates current consolidated text."}
        return {"result":"APPLIES","reasoning_state":"CURRENT_TEXT_APPLICABLE","source_refs":rec.get("source_refs",[]),"reasoning_summary":rec.get("note") or ""}
    return {"result":"UNKNOWN","reasoning_state":"UNKNOWN_TEMPORAL_MODE","source_refs":rec.get("source_refs",[]),"reasoning_summary":"Temporal rule mode is not executable."}

def scope_or_temporal(pid,profile):
    return pid in set(profile.get("scope_sources",[])) or pid.startswith("EU-AIA-113-") or pid in {"GDPR-99-2","NIS2-41-1","NIS2-45","SE-CYBER-TRANS-1"}

def combine(scope,temp,pid,profile,facts):
    if scope["result"] in {"DOES_NOT_APPLY","LEGAL_REVIEW_REQUIRED","UNKNOWN"}: return scope["result"],"SCOPE_"+scope["reasoning_state"]
    if temp["result"] in {"DOES_NOT_APPLY","LEGAL_REVIEW_REQUIRED","UNKNOWN"}: return temp["result"],"TEMPORAL_"+temp["reasoning_state"]
    if scope_or_temporal(pid,profile):
        if scope["result"]=="APPLIES" and temp["result"]=="APPLIES": return "APPLIES","SCOPE_TEMPORAL_COMPLETE"
        return "CONDITIONAL","SCOPE_OR_TEMPORAL_PROVISION_CONDITIONAL"
    cond=facts.get("provision_condition_met")
    if cond is None: return "CONDITIONAL","PROVISION_CONDITION_NOT_ESTABLISHED"
    if cond is False: return "DOES_NOT_APPLY","PROVISION_CONDITION_NOT_MET"
    if scope["result"]=="APPLIES" and temp["result"]=="APPLIES": return "APPLIES","ALL_THREE_STAGES_SATISFIED"
    return "CONDITIONAL","SCOPE_OR_TEMPORAL_CONDITIONAL"

def resolve(case):
    preg=load(PROVISIONS); profiles=load(PROFILES)["profiles"]; temporal=load(TEMPORAL)
    pmap={p["id"]:p for p in preg["provisions"]}; tmap={x["provision_id"]:x for x in temporal["provisions"]}
    pid=case.get("provision_id"); facts=case.get("facts") or {}; snap=case.get("legal_snapshot_date")
    if pid not in pmap:
        return {"result":"LEGAL_REVIEW_REQUIRED","reasoning_state":"UNKNOWN_PROVISION","provision_id":pid,"scope":None,"temporal":None,"reasoning_summary":"Provision ID absent from exact verified registry."}
    if not snap:
        return {"result":"UNKNOWN","reasoning_state":"MISSING_SNAPSHOT_DATE","provision_id":pid,"scope":None,"temporal":None,"reasoning_summary":"legal_snapshot_date is required."}
    profile=profile_for(pid,profiles)
    if not profile:
        return {"result":"LEGAL_REVIEW_REQUIRED","reasoning_state":"NO_UNIQUE_SCOPE_PROFILE","provision_id":pid,"scope":None,"temporal":None,"reasoning_summary":"No unique admitted scope profile."}
    scope=resolve_scope(profile,facts); temp=resolve_temporal(pid,snap,facts,tmap)
    result,state=combine(scope,temp,pid,profile,facts)
    return {
        "result":result,"reasoning_state":state,"provision_id":pid,"instrument":pmap[pid]["instrument"],
        "legal_snapshot_date":snap,"scope":scope,"temporal":temp,
        "provision_condition_met":facts.get("provision_condition_met"),
        "applicability_inferred_from_citation":False,
        "reasoning_summary":"Resolved through independent scope, temporal and provision-condition stages."
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("case_json"); a=ap.parse_args()
    print(json.dumps(resolve(load(a.case_json)),indent=2))

if __name__=="__main__": main()
