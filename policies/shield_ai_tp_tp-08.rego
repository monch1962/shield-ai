package shield_ai.tp.api_gateway_infrastructure_iso

import rego.v1

# SHIELD-AI(TM) TP-08: API Gateway Infrastructure-Isolation Mode
# Pillar: TP -- Tool and Pipeline Security
#
# Prevent agents from reaching cloud infrastructure control planes.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation. Gateway-side
# enforcement complementing EE-02 (agent-side): the gateway allow-list must
# exclude all cloud infrastructure control-plane APIs, and any infra API
# attempt is blocked and treated as a compromise indicator.
# Input model: input.action.gateway = {"infra_isolation": bool,
# "allowlist_active": bool}; input.action.tool (the API being called).
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

# Cloud infrastructure control-plane APIs (mirrors the EE-02 deny set at the
# gateway boundary).
infrastructure_apis := {
    "ec2",
    "iam",
    "lambda",
    "s3",
    "kms",
    "cloudformation",
    "azure_vm",
    "azure_rbac",
    "azure_resource_manager",
    "gcp_compute",
    "gcp_iam",
    "gcp_cloud_resource_manager",
}

deny contains msg if {
    not input.action.gateway.allowlist_active
    msg := sprintf("TP-08 deny: tool %q call without an active gateway API allow-list", [input.action.tool])
}

deny contains msg if {
    input.action.tool in infrastructure_apis
    not input.action.gateway.infra_isolation
    msg := sprintf("TP-08 deny: infrastructure control-plane API %q not blocked by the gateway (infra-isolation mode off)", [input.action.tool])
}

allow if {
    count(deny) == 0
}
