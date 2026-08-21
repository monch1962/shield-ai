package shield_ai.tp.api_gateway_security

import rego.v1

# SHIELD-AI(TM) TP-03: API Gateway Security
# Pillar: TP -- Tool and Pipeline Security
#
# Deploy a gateway between agents and tools that enforces rate limiting, schema validation, audit logging, and MCP protocol awareness where applicable.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.gateway = {"rate_limited": bool,
# "schema_validated": bool, "audited": bool}. Tool calls that bypass the
# gateway's controls fail closed.
# Maturity indicators and regulatory mappings: assets/shield-ai-control-schema.json.

deny contains msg if {
    not input.action.gateway.rate_limited
    msg := sprintf("TP-03 deny: tool %q call not rate-limited by the gateway", [input.action.tool])
}

deny contains msg if {
    not input.action.gateway.schema_validated
    msg := sprintf("TP-03 deny: tool %q call payload not schema-validated by the gateway", [input.action.tool])
}

deny contains msg if {
    not input.action.gateway.audited
    msg := sprintf("TP-03 deny: tool %q call not audit-logged by the gateway", [input.action.tool])
}

allow if {
    count(deny) == 0
}
