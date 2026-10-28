import { get } from "@vercel/blob";
import { authorizeRequest } from "../../lib/auth.mjs";
import { sha256Object } from "../../lib/canonical.mjs";
import { validateBundle } from "../../lib/validate.mjs";

function json(res, status, payload) {
  res.status(status).setHeader("content-type", "application/json; charset=utf-8").send(JSON.stringify(payload));
}

export default async function handler(req, res) {
  if (req.method !== "POST") return json(res, 405, { error: "METHOD_NOT_ALLOWED" });
  try {
    await authorizeRequest(req);
    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    if (!body?.blob_url || !body?.expected_bundle_hash) return json(res, 400, { error: "MISSING_VERIFY_INPUT" });
    const result = await get(body.blob_url, { access: "private", useCache: false });
    if (!result) return json(res, 404, { error: "EVIDENCE_LOSS", detail: "object not found" });
    const text = await new Response(result.stream).text();
    const envelope = JSON.parse(text);
    validateBundle(envelope.bundle);
    const payload = Object.fromEntries(Object.entries(envelope.bundle).filter(([key]) => key !== "bundle_hash"));
    const digest = sha256Object(payload);
    if (digest !== body.expected_bundle_hash || digest !== envelope.bundle.bundle_hash) {
      return json(res, 409, { error: "TAMPER_DETECTED", observed_bundle_hash: digest });
    }
    return json(res, 200, {
      custody_id: envelope.custody_id,
      status: "VERIFIED",
      bundle_id: envelope.bundle.bundle_id,
      bundle_hash: digest,
      received_at: envelope.received_at,
      sender: envelope.sender
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "unknown error";
    const auth = /token|OIDC|untrusted|repository|ref|workflow/.test(message);
    return json(res, auth ? 403 : 400, { error: auth ? "READ_DENIED" : "VERIFY_FAILED", detail: message });
  }
}
