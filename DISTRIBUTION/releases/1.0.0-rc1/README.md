# CDX 1.0.0 Release Candidate 1

Package ID: `CDX-DIST-1.0.0-RC1`

This directory contains the machine-readable manifest for the first frozen Conductellence 1.0 distribution candidate.

It is **not a release**.

The manifest pins each runtime/distribution artifact by Git blob SHA. Run:

```bash
python3 DISTRIBUTION/build_release_package.py --verify-only
```

To materialize an installable tree:

```bash
python3 DISTRIBUTION/build_release_package.py --output /tmp/cdx-1.0.0-rc1
```

Installation does not itself create a valid consumer anchor and does not establish `VERIFIED_RUNTIME_BOUND`. The consumer must complete the later estate binding/verification workflow.

WP07 is the only core stage permitted to convert this candidate into the CDX 1.0 release, and only after the core release blockers are closed.
