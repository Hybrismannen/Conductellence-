#!/usr/bin/env python3
"""Build a zero-provider-call refresh queue for Scite evidence cache."""

from pathlib import Path
import argparse, datetime as dt, json

CACHE=Path("EVIDENCE-AUTHORITY/cache/scite")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--as-of")
    ap.add_argument("--output",default="EVIDENCE-AUTHORITY/provider/scite-refresh-queue.json")
    a=ap.parse_args()
    now=dt.datetime.fromisoformat(a.as_of) if a.as_of else dt.datetime.now(dt.timezone.utc)
    items=[]
    if CACHE.exists():
        for path in sorted(CACHE.glob("*.json")):
            rec=json.loads(path.read_text())
            fresh=dt.datetime.fromisoformat(rec["fresh_until"])
            if fresh<=now:
                items.append({
                  "cache_id":rec["cache_id"],
                  "query_mode":rec["query_mode"],
                  "request_key":rec["request_key"],
                  "fresh_until":rec["fresh_until"],
                  "state":"REFRESH_DUE",
                  "provider_call_authorized":False
                })
    out={"schema":"cdx.scite-refresh-queue/v0.1","generated_at":now.isoformat(),"items":items,
         "policy":"This queue never calls Scite. A provider refresh is an explicit evidence task."}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
