export default function handler(req, res) {
  if (req.method !== "GET") return res.status(405).json({ error: "METHOD_NOT_ALLOWED" });
  return res.status(200).json({
    service: "CDX SPETL Independent Custody",
    custody_id: "CDX-CUSTODY-001",
    status: "READY",
    storage: "PRIVATE_BLOB",
    source_auth: "GITHUB_ACTIONS_OIDC",
    delete_api: false
  });
}
