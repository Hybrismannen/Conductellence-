#!/usr/bin/env python3
from pathlib import Path
import argparse, datetime as dt, hashlib, json, uuid

def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"))

def append_event(path,event):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    previous=None
    if p.exists():
        rows=[x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        if rows: previous=json.loads(rows[-1]).get("event_hash")
    e=dict(event)
    e.setdefault("event_id","CDX-EVT-"+uuid.uuid4().hex.upper())
    e.setdefault("recorded_at",dt.datetime.now(dt.timezone.utc).isoformat())
    e["previous_hash"]=previous
    payload={k:v for k,v in e.items() if k!="event_hash"}
    e["event_hash"]="sha256:"+hashlib.sha256(canonical(payload).encode()).hexdigest()
    with p.open("a",encoding="utf-8") as f:
        f.write(canonical(e)+"\n")
    return e

def verify(path):
    p=Path(path)
    if not p.exists(): return True,0,None
    previous=None; count=0
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        e=json.loads(line)
        claimed=e.pop("event_hash",None)
        if e.get("previous_hash")!=previous:
            return False,count,"previous_hash mismatch"
        calc="sha256:"+hashlib.sha256(canonical(e).encode()).hexdigest()
        if calc!=claimed:
            return False,count,"event_hash mismatch"
        previous=claimed; count+=1
    return True,count,None

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("append"); a.add_argument("ledger"); a.add_argument("event_json")
    v=sub.add_parser("verify"); v.add_argument("ledger")
    x=p.parse_args()
    if x.cmd=="append":
        print(json.dumps(append_event(x.ledger,json.loads(Path(x.event_json).read_text())),indent=2))
    else:
        ok,n,err=verify(x.ledger)
        print(json.dumps({"valid":ok,"events":n,"error":err},indent=2))
        raise SystemExit(0 if ok else 1)

if __name__=="__main__":
    main()
