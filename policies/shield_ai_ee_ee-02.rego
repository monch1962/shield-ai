package shield_ai.ee.infrastructure_api_access_cont

import rego.v1

import data.shield_ai.lib.bad_schema_version

import data.shield_ai.lib.infrastructure_apis

# SHIELD-AI(TM) EE-02: Infrastructure API Access Control
# Pillar: EE -- Execution Environment
#
# Ensure agents cannot reach infrastructure control planes implicitly.
#
# Maturity indicators:
#   L1: Agents inherit infrastructure credentials or can reach control planes.
#   L2: Infrastructure credentials not mounted; network path blocked but untested.
#   L3: Explicit tool registration required for infrastructure access; metadata service disabled; blocked attempts logged.
#   L4: Continuous verification of credential scoping; automated alerting on any infrastructure API attempt.
#
# Regulatory mappings:
#   ISM: Guidelines for Gateways
#   NIST AI RMF: PROTECT (PR.AC)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (AWS AgentCore
# implicit IAM abuse, INC-04).
# Input model: input.action.tool = the API being called;
# input.action.registered_as_tool (bool) = explicitly registered via TP-01.
# Fail closed: no registration claim on an infrastructure API = deny.

# Cloud infrastructure control-plane APIs the agent must never reach
# implicitly. Deployment-defined; add the organisation's platform surface.
# Infrastructure control-plane APIs (from the shared
# registry policies/shield_ai_lib.rego).

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["EE-02"])
}

deny contains msg if {
    input.action.tool in infrastructure_apis
    not input.action.registered_as_tool
    msg := sprintf("EE-02 deny: agent call to infrastructure API %q without explicit tool registration", [input.action.tool])
}

allow if {
    count(deny) == 0
}
