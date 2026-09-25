#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime as dt,hashlib,json,uuid

def canonical(o):
    return json.dumps(o,sort_keys=True,separators=(",",":"))

def append_event(path,event):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    prev=None
    if p.exists():
        rows=[x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        if rows: prev=json.loads(rows[-1]).get("event_hash")
    e=dict(event)
    e.setdefault("event_id","CDX-EVT-"+uuid.uuid4().hex.upper())
    e.setdefault("recorded_at",dt.datetime.now(dt.timezone.utc).isoformat())
    e["previous_hash"]=prev
    payload={k:v for k,v in e.items() if k!="event_hash"}
    e["event_hash"]="sha256:"+hashlib.sha256(canonical(payload).encode()).hexdigest()
    with p.open("a",encoding="utf-8") as f:f.write(canonical(e)+"\n")
    return e

def verify(path):
    prev=None;count=0
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():continue
        item=json.loads(line);claimed=item.pop("event_hash",None)
        if item.get("previous_hash")!=prev:return False,count,"previous_hash mismatch"
        calc="sha256:"+hashlib.sha256(canonical(item).encode()).hexdigest()
        if calc!=claimed:return False,count,"event_hash mismatch"
        prev=claimed;count+=1
    return True,count,None

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("append");a.add_argument("ledger");a.add_argument("event_json")
    v=s.add_parser("verify");v.add_argument("ledger")
    args=p.parse_args()
    if args.cmd=="append":
        print(json.dumps(append_event(args.ledger,json.loads(Path(args.event_json).read_text())),indent=2))
    else:
        ok,n,err=verify(args.ledger);print(json.dumps({"valid":ok,"events":n,"error":err},indent=2));raise SystemExit(0 if ok else 1)
if __name__=="__main__":main()
