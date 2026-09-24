#!/usr/bin/env python3
"""Reachability-only regulator/source check for Conductellence Phase D.

Authority: CDX-CLR-LEGAL-BD-001

This script checks whether registered official source URLs can be reached.
It does NOT interpret HTTP failure, redirects, HTML changes or fingerprints as
amendment, repeal, supersession or non-applicability.
"""

from pathlib import Path
import argparse
import datetime as dt
import json
import urllib.request
import urllib.error

STATE = Path("REGULATORY-DRIFT/source-state.json")

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def check(source, timeout):
    req = urllib.request.Request(
        source["official_url"],
        method="GET",
        headers={"User-Agent":"Conductellence-Regulatory-Drift/0.1"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", 200))
            final_url = resp.geturl()
            return {
                "source_id":source["source_id"],
                "checked_at":now(),
                "reachable":200 <= status < 400,
                "http_status":status,
                "observed_url":final_url,
                "event_type":"REACHABLE" if final_url == source["official_url"] else "SOURCE_REDIRECTED",
                "interpretation_state":"NONE" if final_url == source["official_url"] else "DRIFT_CANDIDATE",
                "legal_change_inferred":False,
            }
    except urllib.error.HTTPError as exc:
        return {
            "source_id":source["source_id"],"checked_at":now(),"reachable":False,
            "http_status":exc.code,"observed_url":source["official_url"],
            "event_type":"SOURCE_UNREACHABLE","interpretation_state":"DRIFT_CANDIDATE",
            "legal_change_inferred":False,"error":str(exc)
        }
    except Exception as exc:
        return {
            "source_id":source["source_id"],"checked_at":now(),"reachable":False,
            "http_status":None,"observed_url":source["official_url"],
            "event_type":"SOURCE_UNREACHABLE","interpretation_state":"DRIFT_CANDIDATE",
            "legal_change_inferred":False,"error":str(exc)
        }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="regulatory-source-check.json")
    ap.add_argument("--timeout",type=int,default=20)
    args=ap.parse_args()
    state=json.loads(STATE.read_text(encoding="utf-8"))
    results=[check(s,args.timeout) for s in state.get("sources",[])]
    payload={
      "authority_ref":"CDX-CLR-LEGAL-BD-001",
      "generated_at":now(),
      "scope":"REACHABILITY_ONLY",
      "legal_change_inferred":False,
      "results":results
    }
    Path(args.output).write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(payload,indent=2))
    if any(not x["reachable"] for x in results):
        raise SystemExit(2)

if __name__=="__main__":
    main()
