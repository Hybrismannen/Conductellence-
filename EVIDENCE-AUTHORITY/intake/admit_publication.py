#!/usr/bin/env python3
"""Local-only scientific publication admission for CDX-EVID-001.

This script NEVER calls Scite. It admits a previously retrieved provider payload
(or manually verified publication metadata) into Conductellence's publication
registry and cache. Network/provider retrieval happens explicitly outside CI.
"""

from pathlib import Path
import argparse, datetime as dt, hashlib, json, re

ROOT=Path("EVIDENCE-AUTHORITY")
PUBS=ROOT/"registry/publications.json"
CACHE_DIR=ROOT/"cache/scite"

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def now(): return dt.datetime.now(dt.timezone.utc)

def norm_doi(v):
    if not v: return None
    v=v.strip()
    v=re.sub(r"^https?://(dx\.)?doi\.org/","",v,flags=re.I)
    return v.lower()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("provider_json")
    ap.add_argument("--doi",required=True)
    ap.add_argument("--title",required=True)
    ap.add_argument("--journal")
    ap.add_argument("--year",type=int)
    ap.add_argument("--domain",action="append",default=[])
    ap.add_argument("--metadata-days",type=int,default=30)
    args=ap.parse_args()

    doi=norm_doi(args.doi)
    payload=load(args.provider_json)
    raw=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
    digest=hashlib.sha256(raw).hexdigest()
    retrieved=now()
    fresh=retrieved+dt.timedelta(days=args.metadata_days)

    cache_id="CDX-SCITE-CACHE-"+hashlib.sha256(("doi:"+doi).encode()).hexdigest()[:16].upper()
    cache={
      "cache_id":cache_id,
      "provider_id":"CDX-PROV-SCITE-001",
      "query_mode":"DOI_METADATA",
      "request_key":"doi:"+doi,
      "retrieved_at":retrieved.isoformat(),
      "fresh_until":fresh.isoformat(),
      "payload_sha256":"sha256:"+digest,
      "provider_payload":payload,
      "authority_effect":"NONE",
      "legal_effect":"NONE"
    }
    CACHE_DIR.mkdir(parents=True,exist_ok=True)
    (CACHE_DIR/(cache_id+".json")).write_text(json.dumps(cache,indent=2)+"\n",encoding="utf-8")

    doc=load(PUBS)
    pubs=doc.setdefault("publications",[])
    existing=next((p for p in pubs if p.get("doi")==doi),None)
    if existing:
        existing.update({
          "title":args.title,"journal":args.journal,"year":args.year,
          "domains":sorted(set(existing.get("domains",[])+args.domain)),
          "provider_cache_ref":str(CACHE_DIR/(cache_id+".json")),
          "provider_last_retrieved_at":retrieved.isoformat(),
          "editorial_state":"UNASSESSED",
          "authority_state":"EVIDENCE_ONLY"
        })
        pub=existing
    else:
        pub_id="CDX-PUB-"+hashlib.sha256(doi.encode()).hexdigest()[:16].upper()
        pub={
          "publication_id":pub_id,
          "doi":doi,
          "title":args.title,
          "journal":args.journal,
          "year":args.year,
          "domains":sorted(set(args.domain)),
          "provider":"Scite",
          "provider_cache_ref":str(CACHE_DIR/(cache_id+".json")),
          "provider_last_retrieved_at":retrieved.isoformat(),
          "editorial_state":"UNASSESSED",
          "evidence_state":"SOURCED",
          "authority_state":"EVIDENCE_ONLY"
        }
        pubs.append(pub)
        pubs.sort(key=lambda x:x["publication_id"])

    PUBS.write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"publication_id":pub["publication_id"],"doi":doi,"cache_id":cache_id,"fresh_until":fresh.isoformat()},indent=2))

if __name__=="__main__": main()
