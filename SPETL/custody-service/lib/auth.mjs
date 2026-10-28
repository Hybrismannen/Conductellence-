import { createRemoteJWKSet, jwtVerify } from "jose";
import { validateGithubClaims } from "./claims.mjs";

const ISSUER = "https://token.actions.githubusercontent.com";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

export async function authorizeRequest(req) {
  const header = req.headers.authorization || req.headers.Authorization;
  if (!header || !header.startsWith("Bearer ")) throw new Error("missing bearer token");
  const token = header.slice("Bearer ".length);
  const audience = process.env.CDX_CUSTODY_AUDIENCE || "cdx-spetl-custody";
  const repository = process.env.CDX_CUSTODY_SOURCE_REPOSITORY || "Hybrismannen/Conductellence-";
  const ref = process.env.CDX_CUSTODY_SOURCE_REF || "refs/heads/main";
  const workflowRef = process.env.CDX_CUSTODY_WORKFLOW_REF ||
    "Hybrismannen/Conductellence-/.github/workflows/spetl-evidence-publish.yml@refs/heads/main";
  const { payload } = await jwtVerify(token, JWKS, { issuer: ISSUER, audience });
  return validateGithubClaims(payload, { repository, ref, workflowRef });
}
