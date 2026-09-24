#!/usr/bin/env python3
"""Build a non-semantic regulatory-drift impact queue.

Authority: CDX-CLR-LEGAL-BD-001

Input is a transport/source observation. This script maps drift candidates to
registered legal provisions and to Conductellence paragraphs/proofs that depend
on those provisions. It does not interpret the legal meaning of the drift.
"""

from pathlib import Path
import argparse, datetime as dt, json

PARA_MAP=Path("LEGAL-REFERENCES/paragraph-legal-map.json")
PROOFS=Path("LEGAL-REFERENCES/legal-support-proofs.json")
PROFILES=Path("LEGAL-RESOLVER/scope-profiles.json")
TEMPORAL=Path("REGULATORY-DRIFT/provision-temporal-state.json")

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("observation_json")
    ap.add_argument("--output",default="regulatory-impact-queue.json")
    a=ap.parse_args()

    obs=load(a.observation_json)
    pmap=load(PARA_MAP)
    proofs=load(PROOFS).get("proofs",[])
    profiles=load(PROFILES).get("profiles",[])
    temporal={x["provision_id"]:x for x in load(TEMPORAL).get("provisions",[])}

    para_by_prov={}
    for p in pmap.get("paragraphs",[]):
        for r in p.get("references",[]):
            para_by_prov.setdefault(r["provision_id"],set()).add(p["paragraph_id"])

    proofs_by_prov={}
    for p in proofs:
        proofs_by_prov.setdefault(p.get("provision_id"),set()).add(p.get("proof_id"))

    rules_by_prov={}
    for prof in profiles:
        for rule in prof.get("outcomes",[]):
            for ref in rule.get("source_refs",[]):
                rules_by_prov.setdefault(ref,set()).add(rule.get("rule_id"))

    items=[]
    seq=1
    for result in obs.get("results",[]):
        if not result.get("requires_reassessment"):
            continue
        for pid in sorted(set(result.get("affected_provision_ids",[]))):
            items.append({
                "impact_id":f"CDX-RDI-{seq:05d}",
                "authority_ref":"CDX-CLR-LEGAL-BD-001",
                "source_id":result.get("source_id"),
                "source_event_type":result.get("event_type"),
                "provision_id":pid,
                "paragraph_ids":sorted(para_by_prov.get(pid,set())),
                "semantic_proof_ids":sorted(x for x in proofs_by_prov.get(pid,set()) if x),
                "scope_rule_ids":sorted(x for x in rules_by_prov.get(pid,set()) if x),
                "has_temporal_state":pid in temporal,
                "state":"REASSESSMENT_REQUIRED",
                "legal_change_inferred":False
            })
            seq+=1

    doc={
      "schema":"cdx.regulatory-drift.impact-queue/v0.1",
      "authority_ref":"CDX-CLR-LEGAL-BD-001",
      "generated_at":now(),
      "source_observation_generated_at":obs.get("generated_at"),
      "legal_change_inferred":False,
      "items":items,
      "counts":{
        "drift_sources":len(set(x["source_id"] for x in items)),
        "affected_provisions":len(set(x["provision_id"] for x in items)),
        "affected_paragraphs":len(set(p for x in items for p in x["paragraph_ids"])),
        "items":len(items)
      }
    }
    Path(a.output).write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(doc,indent=2))

if __name__=="__main__": main()
