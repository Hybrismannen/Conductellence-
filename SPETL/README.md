# SPETL — Security Penetration, Execution & Traceability Ledger

**System ID:** `CDX-SYS-002`  
**Canonical reference runtime:** `SPETL/spetl.py`

SPETL is the Conductellence evidence plane. Runtime decisions are recorded as append-oriented events with correlation, causation, authority, policy and control evidence.

The canonical reference runtime:

- appends JSONL events;
- links each event to the prior event hash;
- verifies the resulting hash chain;
- treats corrections as new events rather than rewriting prior evidence.

`SPETL/spetl.py` is the only canonical reference implementation in this repository.

Production deployments should preserve the same event semantics in an independently controlled evidence store. Git history and the local reference runtime do not, by themselves, constitute independent production evidence preservation.
