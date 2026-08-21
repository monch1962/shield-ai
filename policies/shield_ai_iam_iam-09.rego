package shield_ai.iam.multi_tenant_agent_platform_is

import rego.v1

# SHIELD-AI(TM) IAM-09: Multi-Tenant Agent Platform Isolation
# Pillar: IAM -- Identity and Access
#
# Enforce data-layer tenant isolation on managed agent platforms.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (Langflow
# CVE-2026-55255 IDOR / CVE-2026-9198 login-bypass RCE, INC-16).
# Input model: input.tenant = {"id": string, "scoped": bool};
# input.action.user_controlled_object_id (bool) -- the request references an
# object ID supplied by the caller. User-controlled object IDs must never
# bypass tenant scoping (CWE-639).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.tenant.scoped
    msg := "IAM-09 deny: request not scoped to tenant ID at the data layer (presentation-layer checks only)"
}

deny contains msg if {
    input.action.user_controlled_object_id == true
    not input.tenant.scoped
    msg := "IAM-09 deny: user-controlled object ID bypasses tenant scoping (CWE-639 IDOR class)"
}

allow if {
    count(deny) == 0
}
