import { sha256Object } from "./canonical.mjs";

export const DECISIONS = new Set([
  "ALLOW","ALLOW_WITH_CONTROLS","REQUIRE_HUMAN","QUARANTINE",
  "DENY","SECURITY_STOP","CONSTITUTIONAL_STOP"
]);
export const EFFECT_STATUSES = new Set(["NOT_ATTEMPTED","PERMITTED","BLOCKED","FAILED"]);
export const REQUIRED_EVENT_FIELDS = [
  "schema_version","event_id","event_type","recorded_at","actor_id","subject_ref","action",
  "attempted_effect","effect_status","decision","authority_ref","mandate_ref","policy_ref","policy_version",
  "policy_digest","request_id","correlation_id","causation_id","run_id","trace_ref","reviewer_ref",
  "data_minimization","control_results","evidence_refs","previous_hash","event_hash"
];
export const ALLOWED_EVENT_FIELDS = new Set([...REQUIRED_EVENT_FIELDS,"resource_id"]);

export function validateEvent(event) {
  if (!event || typeof event !== "object" || Array.isArray(event)) throw new Error("event must be an object");
  const missing = REQUIRED_EVENT_FIELDS.filter((key) => !(key in event));
  if (missing.length) throw new Error("missing event fields: " + missing.join(","));
  const unexpected = Object.keys(event).filter((key) => !ALLOWED_EVENT_FIELDS.has(key));
  if (unexpected.length) throw new Error("unexpected event fields: " + unexpected.join(","));
  if (event.schema_version !== "1.1") throw new Error("unsupported event schema");
  if (!DECISIONS.has(event.decision)) throw new Error("invalid decision");
  if (!EFFECT_STATUSES.has(event.effect_status)) throw new Error("invalid effect_status");
  if (!event.attempted_effect || typeof event.attempted_effect !== "object") throw new Error("attempted_effect required");
  for (const key of ["surface","operation","target_ref"]) {
    if (!(key in event.attempted_effect)) throw new Error("attempted_effect." + key + " required");
  }
  if (!event.data_minimization || typeof event.data_minimization !== "object") throw new Error("data_minimization required");
  if (typeof event.data_minimization.personal_data_present !== "boolean") throw new Error("personal_data_present must be boolean");
  if (!Array.isArray(event.data_minimization.redacted_fields)) throw new Error("redacted_fields must be array");
  if (typeof event.data_minimization.rationale !== "string" || !event.data_minimization.rationale) throw new Error("minimization rationale required");
  if (!Array.isArray(event.control_results) || !Array.isArray(event.evidence_refs)) throw new Error("control/evidence arrays required");
  for (const key of ["authority_ref","mandate_ref","policy_ref","policy_version","request_id","correlation_id","causation_id","run_id","trace_ref"]) {
    if (typeof event[key] !== "string" || !event[key]) throw new Error(key + " must be non-empty");
  }
  const denyLike = new Set(["DENY","REQUIRE_HUMAN","QUARANTINE","SECURITY_STOP","CONSTITUTIONAL_STOP"]);
  const allowLike = new Set(["ALLOW","ALLOW_WITH_CONTROLS"]);
  if (event.effect_status === "PERMITTED" && !allowLike.has(event.decision)) throw new Error("non-allow decision cannot permit effect");
  if (denyLike.has(event.decision) && event.effect_status === "PERMITTED") throw new Error("deny/stop decision cannot permit effect");
  if (allowLike.has(event.decision) && event.effect_status === "BLOCKED") throw new Error("allow decision cannot report blocked effect");
  if (event.policy_digest === "UNAVAILABLE") {
    if (!new Set(["SECURITY_STOP","DENY"]).has(event.decision)) throw new Error("unavailable policy must fail closed");
    if (!new Set(["BLOCKED","NOT_ATTEMPTED"]).has(event.effect_status)) throw new Error("unavailable policy cannot permit effect");
  }
  return true;
}

export function verifyEventChain(events) {
  let previous = null;
  const seen = new Set();
  for (const event of events) {
    validateEvent(event);
    if (event.previous_hash !== previous) throw new Error("previous_hash mismatch");
    const payload = Object.fromEntries(Object.entries(event).filter(([key]) => key !== "event_hash"));
    if (sha256Object(payload) !== event.event_hash) throw new Error("event_hash mismatch");
    if (seen.has(event.event_id)) throw new Error("duplicate event_id");
    seen.add(event.event_id);
    previous = event.event_hash;
  }
  return seen;
}

export function validateBundle(bundle) {
  if (!bundle || bundle.schema !== "cdx.spetl.custody-bundle/v1.0") throw new Error("invalid bundle schema");
  for (const key of ["bundle_id","created_at","producer","source_commit","expected_event_ids","events","retention","bundle_hash"]) {
    if (!(key in bundle)) throw new Error("missing bundle field: " + key);
  }
  if (!/^[0-9a-f]{40}$/.test(bundle.source_commit)) throw new Error("invalid source_commit");
  if (!bundle.producer || !bundle.producer.system_id || !bundle.producer.runtime_id || !bundle.producer.repository) throw new Error("invalid producer");
  if (!Array.isArray(bundle.events) || !bundle.events.length) throw new Error("events missing");
  if (!Array.isArray(bundle.expected_event_ids) || !bundle.expected_event_ids.length) throw new Error("expected_event_ids missing");
  const claimed = bundle.bundle_hash;
  const payload = Object.fromEntries(Object.entries(bundle).filter(([key]) => key !== "bundle_hash"));
  if (sha256Object(payload) !== claimed) throw new Error("bundle_hash mismatch");
  const seen = verifyEventChain(bundle.events);
  const missing = bundle.expected_event_ids.filter((id) => !seen.has(id));
  const unexpected = [...seen].filter((id) => !bundle.expected_event_ids.includes(id));
  if (missing.length) throw new Error("withheld evidence: " + missing.join(","));
  if (unexpected.length) throw new Error("injected evidence: " + unexpected.join(","));
  const ordered = bundle.events.map((event) => event.event_id);
  if (JSON.stringify(ordered) !== JSON.stringify(bundle.expected_event_ids)) throw new Error("evidence order/identity manifest mismatch");
  if (bundle.retention?.deletion_mode !== "GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION") throw new Error("invalid deletion mode");
  return true;
}
