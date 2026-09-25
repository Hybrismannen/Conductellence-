#!/usr/bin/env python3
from pathlib import Path
import argparse,json

def load_twin(path):
    p=Path(path)
    if p.exists(): return json.loads(p.read_text())
    return {"schema":"cdx.security-twin/v1.0","nodes":[],"edges":[]}

def add_node(nodes,index,node):
    if node["id"] not in index:
        nodes.append(node);index.add(node["id"])

def main():
    p=argparse.ArgumentParser()
    p.add_argument("ledger")
    p.add_argument("--twin",default="SECURITY-TWIN/twin.json")
    a=p.parse_args()
    twin=load_twin(a.twin)
    nodes=twin.setdefault("nodes",[]);edges=twin.setdefault("edges",[])
    idx={n["id"] for n in nodes}
    for line in Path(a.ledger).read_text().splitlines():
        if not line.strip():continue
        e=json.loads(line)
        actor=e.get("actor_id");resource=e.get("resource_id");event=e.get("event_id")
        if actor:add_node(nodes,idx,{"id":actor,"type":"PRINCIPAL"})
        if resource:add_node(nodes,idx,{"id":resource,"type":"RESOURCE"})
        if actor and resource:
            edges.append({"from":actor,"to":resource,"relation":"ATTEMPTED_"+str(e.get("action")),"decision":e.get("decision"),"event_id":event})
    Path(a.twin).write_text(json.dumps(twin,indent=2)+"\n")
    print(json.dumps({"nodes":len(nodes),"edges":len(edges)},indent=2))
if __name__=="__main__":main()
