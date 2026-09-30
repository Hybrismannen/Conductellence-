#!/usr/bin/env python3
from pathlib import Path
import json

def build():
    estate=json.loads(Path("ESTATE-REGISTRY/systems.json").read_text())
    controls=json.loads(Path("POLICY/control-registry.json").read_text())
    nodes=[{"id":"CDX-SYS-001","type":"AUTHORITY","label":"Conductellence"}]
    edges=[]
    for s in estate["systems"]:
        if s["system_id"]!="CDX-SYS-001":
            nodes.append({"id":s["system_id"],"type":"SYSTEM","label":s["repository"],"security_state":s["security_state"]})
            edges.append({"from":"CDX-SYS-001","to":s["system_id"],"relation":"GOVERNS","state":s["security_state"]})
    for c in controls["controls"]:
        nodes.append({"id":c["control_id"],"type":"CONTROL","label":c["title"],"surface":c["enforcement_surface"]})
        edges.append({"from":"CDX-SYS-001","to":c["control_id"],"relation":"DEFINES_CONTROL","section_id":c["section_id"]})
    return {"schema":"cdx.security-twin/v1.0","nodes":nodes,"edges":edges}

if __name__=="__main__":
    d=build()
    Path("SECURITY-TWIN/twin.json").write_text(json.dumps(d,indent=2)+"\n")
    print(json.dumps({"nodes":len(d["nodes"]),"edges":len(d["edges"])},indent=2))
