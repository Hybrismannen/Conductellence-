import test from "node:test";
import assert from "node:assert/strict";
import { sha256Object } from "../lib/canonical.mjs";
import { validateBundle } from "../lib/validate.mjs";
import { validateGithubClaims } from "../lib/claims.mjs";

function event() {
  const e = {
    schema_version:"1.1", event_id:"E1", event_type:"POLICY_DECISION",
    recorded_at:"2026-10-28T20:00:00Z", actor_id:"A", subject_ref:"S", action:"WRITE",
    attempted_effect:{surface:"test",operation:"write",target_ref:"T"}, effect_status:"PERMITTED",
    decision:"ALLOW", authority_ref:"CDX-LAW-001", mandate_ref:"M1", policy_version:"1.0.0",
    policy_digest:"sha256:"+"a".repeat(64), correlation_id:"C", causation_id:"ROOT", run_id:"R",
    trace_ref:"TR", reviewer_ref:null,
    data_minimization:{personal_data_present:false,redacted_fields:[],rationale:"synthetic"},
    control_results:[], evidence_refs:[], previous_hash:null
  };
  e.event_hash=sha256Object(e);
  return e;
}
function bundle() {
  const e=event();
  const b={
    schema:"cdx.spetl.custody-bundle/v1.0", bundle_id:"B1", created_at:"2026-10-28T20:01:00Z",
    producer:{system_id:"CDX-SYS-001",runtime_id:"CDX-REFERENCE-RUNTIME",repository:"Hybrismannen/Conductellence-"},
    source_commit:"0".repeat(40), expected_event_ids:["E1"], events:[e],
    retention:{class:"CDX_AUDIT_EVIDENCE",deletion_mode:"GOVERNED_TOMBSTONE_AND_AUTHORIZED_ADMIN_ACTION"}
  };
  b.bundle_hash=sha256Object(b);
  return b;
}
test("valid bundle passes",()=>assert.equal(validateBundle(bundle()),true));
test("tamper is rejected",()=>{
  const b=bundle(); b.events[0].action="TAMPER";
  assert.throws(()=>validateBundle(b),/bundle_hash mismatch/);
});
test("withheld evidence is rejected",()=>{
  const b=bundle(); b.expected_event_ids.push("E2");
  const payload=Object.fromEntries(Object.entries(b).filter(([k])=>k!=="bundle_hash"));
  b.bundle_hash=sha256Object(payload);
  assert.throws(()=>validateBundle(b),/withheld evidence/);
});
test("trusted GitHub OIDC claims pass",()=>{
  const claims={repository:"Hybrismannen/Conductellence-",ref:"refs/heads/main",
    workflow_ref:"Hybrismannen/Conductellence-/.github/workflows/spetl-evidence-publish.yml@refs/heads/main",
    run_id:"1",actor:"Hybrismannen",sha:"0".repeat(40)};
  const id=validateGithubClaims(claims,{repository:claims.repository,ref:claims.ref,workflowRef:claims.workflow_ref});
  assert.equal(id.run_id,"1");
});
test("different repository is denied",()=>{
  const claims={repository:"attacker/repo",ref:"refs/heads/main",workflow_ref:"x",run_id:"1"};
  assert.throws(()=>validateGithubClaims(claims,{repository:"Hybrismannen/Conductellence-",ref:"refs/heads/main",workflowRef:"x"}),/untrusted repository/);
});

test("deny cannot report permitted effect",()=>{
  const b=bundle(); b.events[0].decision="DENY"; b.events[0].effect_status="PERMITTED";
  const eventPayload=Object.fromEntries(Object.entries(b.events[0]).filter(([k])=>k!=="event_hash"));
  b.events[0].event_hash=sha256Object(eventPayload);
  const payload=Object.fromEntries(Object.entries(b).filter(([k])=>k!=="bundle_hash"));
  b.bundle_hash=sha256Object(payload);
  assert.throws(()=>validateBundle(b),/cannot permit effect/);
});
test("policy unavailable fails closed",()=>{
  const b=bundle(); b.events[0].policy_digest="UNAVAILABLE"; b.events[0].decision="SECURITY_STOP"; b.events[0].effect_status="BLOCKED";
  const eventPayload=Object.fromEntries(Object.entries(b.events[0]).filter(([k])=>k!=="event_hash"));
  b.events[0].event_hash=sha256Object(eventPayload);
  const payload=Object.fromEntries(Object.entries(b).filter(([k])=>k!=="bundle_hash"));
  b.bundle_hash=sha256Object(payload);
  assert.equal(validateBundle(b),true);
});
