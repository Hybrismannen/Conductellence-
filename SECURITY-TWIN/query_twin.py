#!/usr/bin/env python3
from pathlib import Path
import argparse,json

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--node")
    p.add_argument("--relation")
    a=p.parse_args()
    d=json.loads(Path("SECURITY-TWIN/twin.json").read_text())
    edges=d["edges"]
    if a.node:
        edges=[e for e in edges if e.get("from")==a.node or e.get("to")==a.node]
    if a.relation:
        edges=[e for e in edges if e.get("relation")==a.relation]
    print(json.dumps(edges,indent=2))
if __name__=="__main__":main()
