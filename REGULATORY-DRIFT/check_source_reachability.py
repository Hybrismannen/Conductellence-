#!/usr/bin/env python3
"""Conductellence regulatory-source observation.

Authority: CDX-CLR-LEGAL-BD-001
Phase: D

Fetches official source endpoints, produces transport fingerprints, and compares
against an optional prior observation. A fetch failure, redirect or fingerprint
change is a drift candidate only. This script never infers amendment, repeal,
supersession, or legal applicability.
"""

from pathlib import Path
import argparse, datetime as dt, hashlib, json, urllib.request, urllib.error

STATE=Path("REGULATORY-DRIFT/source-state.json")

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def load_optional(path):
    if not path: return {}
    p=Path(path)
    if not p.exists(): return {}
    try:
        doc=json.loads(p.read_text(encoding="utf-8"))
        return {x["source_id"]:x for x in doc.get("results",[])}
    except Exception:
        return {}

def observe(source,prior,timeout):
    req=urllib.request.Request(source["official_url"],headers={"User-Agent":"Conductellence-Regulatory-Drift/0.2"})
    base={
      "source_id":source["source_id"],"official_url":source["official_url"],
      "checked_at":now(),"legal_change_inferred":False,
      "affected_provision_ids":source.get("provision_ids",[])
    }
    try:
        with urllib.request.urlopen(req,timeout=timeout) as resp:
            body=resp.read()
            status=int(getattr(resp,"status",200)); final=resp.geturl()
            fp="sha256:"+hashlib.sha256(body).hexdigest()
            prior_fp=(prior or {}).get("content_fingerprint")
            if final!=source["official_url"]:
                event="SOURCE_REDIRECTED"; interp="DRIFT_CANDIDATE"
            elif prior_fp and prior_fp!=fp:
                event="FINGERPRINT_CHANGED"; interp="DRIFT_CANDIDATE"
            elif prior_fp==fp:
                event="NO_CHANGE_OBSERVED"; interp="NONE"
            else:
                event="REACHABLE"; interp="NONE"
            return {**base,"reachable":True,"http_status":status,"observed_url":final,
              "content_fingerprint":fp,"fingerprint_semantics":"TRANSPORT_SNAPSHOT_ONLY",
              "content_length":len(body),"event_type":event,"interpretation_state":interp,
              "requires_reassessment":interp=="DRIFT_CANDIDATE"}
    except urllib.error.HTTPError as exc:
        return {**base,"reachable":False,"http_status":exc.code,"observed_url":source["official_url"],
          "content_fingerprint":None,"fingerprint_semantics":"TRANSPORT_SNAPSHOT_ONLY",
          "event_type":"SOURCE_UNREACHABLE","interpretation_state":"DRIFT_CANDIDATE",
          "requires_reassessment":True,"error":str(exc)}
    except Exception as exc:
        return {**base,"reachable":False,"http_status":None,"observed_url":source["official_url"],
          "content_fingerprint":None,"fingerprint_semantics":"TRANSPORT_SNAPSHOT_ONLY",
          "event_type":"SOURCE_UNREACHABLE","interpretation_state":"DRIFT_CANDIDATE",
          "requires_reassessment":True,"error":str(exc)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="regulatory-source-observation.json")
    ap.add_argument("--prior",default=None)
    ap.add_argument("--timeout",type=int,default=25)
    a=ap.parse_args()
    state=json.loads(STATE.read_text(encoding="utf-8"))
    prior=load_optional(a.prior)
    results=[observe(s,prior.get(s["source_id"]),a.timeout) for s in state.get("sources",[])]
    doc={"authority_ref":"CDX-CLR-LEGAL-BD-001","generated_at":now(),"scope":"TRANSPORT_OBSERVATION_ONLY",
      "legal_change_inferred":False,"results":results,
      "drift_candidates":[x["source_id"] for x in results if x.get("requires_reassessment")]}
    Path(a.output).write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(doc,indent=2))

if __name__=="__main__": main()
