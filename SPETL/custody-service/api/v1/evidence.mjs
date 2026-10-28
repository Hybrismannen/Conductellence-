import { put } from "@vercel/blob";
import { authorizeRequest } from "../../lib/auth.mjs";
import { stableStringify, sha256Object } from "../../lib/canonical.mjs";
import { validateBundle } from "../../lib/validate.mjs";

function json(res, status, payload) {
  res.status(status).setHeader("content-type", "application/json; charset=utf-8").send(JSON.stringify(payload));
}

export default async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { error: "METHOD_NOT_ALLOWED" });
  try {
    const identity = await authorizeRequest(req);
    const bundle = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    validateBundle(bundle);
    if (bundle.producer.repository !== identity.repository) throw new Error("producer repository does not match OIDC identity");
    if (bundle.source_commit !== identity.sha) throw new Error("source_commit does not match OIDC sha");

    const digest = sha256Object(Object.fromEntries(Object.entries(bundle).filter(([key]) => key !== "bundle_hash")));
    if (digest !== bundle.bundle_hash) throw new Error("bundle digest mismatch");

    const date = new Date().toISOString().slice(0,10).replaceAll("-","/");
    const hex = digest.slice("sha256:".length);
    const pathname = `evidence/${date}/${bundle.bundle_id}-${hex}.json`;
    const envelope = {
      schema: "cdx.spetl.custody-envelope/v1.0",
      custody_id: "CDX-CUSTODY-001",
      received_at: new Date().toISOString(),
      sender: identity,
      bundle
    };
    const blob = await put(pathname, stableStringify(envelope), {
      access: "private",
      addRandomSuffix: false,
      allowOverwrite: false,
      contentType: "application/json"
    });
    return json(res, 201, {
      custody_id: "CDX-CUSTODY-001",
      status: "PRESERVED",
      bundle_id: bundle.bundle_id,
      bundle_hash: bundle.bundle_hash,
      pathname: blob.pathname,
      blob_url: blob.url,
      received_at: envelope.received_at,
      sender: identity
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "unknown error";
    const status = /token|OIDC|untrusted|repository|ref|workflow|source_commit/.test(message) ? 403 : 400;
    return json(res, status, { error: status === 403 ? "WRITE_DENIED" : "INVALID_EVIDENCE", detail: message });
  }
}
