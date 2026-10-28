#!/usr/bin/env python3
"""Build or verify a pinned Conductellence distribution candidate."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST=ROOT/"DISTRIBUTION/releases/1.0.0-rc1/manifest.json"

def git_blob_sha(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def load_manifest(path):
    doc=json.loads(path.read_text(encoding="utf-8"))
    if doc.get("schema")!="cdx.distribution-package/v1.0":
        raise SystemExit("FAIL: unsupported distribution package schema")
    if doc.get("status")!="RELEASE_CANDIDATE_NOT_RELEASED":
        raise SystemExit("FAIL: WP06 builder only accepts non-released candidate manifests")
    return doc

def verify(doc):
    rows=[]
    for artifact in doc.get("artifacts",[]):
        src=ROOT/artifact["source"]
        if not src.exists():
            raise SystemExit("FAIL: missing source artifact "+artifact["source"])
        observed=git_blob_sha(src)
        expected=artifact["git_blob_sha"]
        if observed!=expected:
            raise SystemExit(f"FAIL: {artifact['source']} blob {observed}, expected {expected}")
        rows.append({"source":artifact["source"],"git_blob_sha":observed})
    if not rows:
        raise SystemExit("FAIL: empty package")
    return rows

def materialize(doc,out):
    out.mkdir(parents=True,exist_ok=True)
    for artifact in doc["artifacts"]:
        src=ROOT/artifact["source"]
        dst=out/artifact["target"]
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,dst)
    (out/"PACKAGE-MANIFEST.json").write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",default=str(DEFAULT_MANIFEST))
    ap.add_argument("--output")
    ap.add_argument("--verify-only",action="store_true")
    args=ap.parse_args()
    manifest_path=Path(args.manifest)
    doc=load_manifest(manifest_path)
    rows=verify(doc)
    if args.output:
        materialize(doc,Path(args.output))
    if not args.output and not args.verify_only:
        ap.error("use --verify-only or --output")
    print(json.dumps({
        "package_id":doc["package_id"],
        "status":doc["status"],
        "artifacts_verified":len(rows),
        "release_authorized":doc.get("release_authorized",False)
    },indent=2))

if __name__=="__main__":
    main()
