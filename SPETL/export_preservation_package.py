#!/usr/bin/env python3
"""Build a portable SPETL preservation package.

This creates a deterministic evidence package suitable for transfer to an
independent evidence store. It does not itself make the destination independent.
"""

from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil, datetime as dt

SPETL_RUNTIME = Path("SPETL/spetl.py")

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return "sha256:"+h.hexdigest()

def load_spetl():
    spec=importlib.util.spec_from_file_location("cdx_spetl",SPETL_RUNTIME)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("output_dir")
    ap.add_argument("--source-commit")
    ap.add_argument("--authority-ref",default="CDX-SYS-001")
    args=ap.parse_args()

    ledger=Path(args.ledger)
    out=Path(args.output_dir)
    out.mkdir(parents=True,exist_ok=True)

    if not ledger.exists():
        raise SystemExit("ledger does not exist")

    spetl=load_spetl()
    ok,count,error=spetl.verify(ledger)
    if not ok:
        raise SystemExit("SPETL verification failed: "+str(error))

    copied=out/"spetl-ledger.jsonl"
    shutil.copyfile(ledger,copied)

    head_hash=None
    rows=[x for x in copied.read_text(encoding="utf-8").splitlines() if x.strip()]
    if rows:
        head_hash=json.loads(rows[-1]).get("event_hash")

    manifest={
      "schema":"cdx.spetl.preservation-package/v1.0",
      "system_id":"CDX-SYS-002",
      "authority_ref":args.authority_ref,
      "created_at":dt.datetime.now(dt.timezone.utc).isoformat(),
      "source_commit":args.source_commit,
      "event_count":count,
      "head_event_hash":head_hash,
      "files":{
        "spetl-ledger.jsonl":{
          "sha256":sha256(copied),
          "bytes":copied.stat().st_size
        }
      },
      "verification":{
        "spetl_chain_valid":True,
        "runtime":"SPETL/spetl.py"
      },
      "destination_state":"UNASSIGNED",
      "independence_claimed":False,
      "rule":"This package is ready for independent preservation. Independence is satisfied only after transfer to a separately controlled target with verified retention, access control and recovery."
    }

    manifest_path=out/"manifest.json"
    manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__":
    main()
