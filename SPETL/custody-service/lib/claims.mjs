export function validateGithubClaims(claims, config) {
  if (!claims || typeof claims !== "object") throw new Error("missing OIDC claims");
  if (claims.repository !== config.repository) throw new Error("untrusted repository");
  if (claims.ref !== config.ref) throw new Error("untrusted ref");
  if (config.workflowRef && claims.workflow_ref !== config.workflowRef) throw new Error("untrusted workflow_ref");
  if (!claims.run_id) throw new Error("missing run_id claim");
  return {
    repository: claims.repository,
    ref: claims.ref,
    workflow_ref: claims.workflow_ref,
    run_id: String(claims.run_id),
    actor: claims.actor || null,
    sha: claims.sha || null
  };
}
