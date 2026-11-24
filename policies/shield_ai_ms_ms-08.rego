package shield_ai.ms.mcp_security_controls

import rego.v1

import data.shield_ai.lib.bad_schema_version

# SHIELD-AI(TM) MS-08: MCP Security Controls
# Pillar: MS -- Model Security
#
# Secure the MCP protocol layer for agent-tool communication.
#
# Maturity indicators:
#   L1: MCP used without gateway; no protocol-layer controls.
#   L2: MCP gateway deployed for agent-tool traffic; basic schema validation.
#   L3: Signed tool metadata; response validation against known-good schemas; trusted MCP registry.
#   L4: Continuous MCP protocol-layer testing; automated blocking of unsigned tool definitions.
#
# Regulatory mappings:
#   OWASP: LLM02 (Insecure Output Handling)
#   NIST AI RMF: PROTECT (PR.AC)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation (AutoJack, TrustFall,
# OX Security supply chain INC-12; Kiro MCP registry INC-20).
# Input model: input.action.kind == "mcp_connect";
# input.action.tool_def_signed (bool); input.action.server_registry
# ("trusted" | "untrusted"). Fail closed on missing claims.

# Envelope guard: reject fabricated/drifted schema-version input outright.
deny contains msg if {
    bad_schema_version(input)
    msg := sprintf("%s deny: input carries a schema_version not supported by this policy", ["MS-08"])
}
# Discriminator hoisted to one guard shared by all rules below.
applicable if {
    input.action.kind == "mcp_connect"
}


deny contains msg if {
    applicable
    not input.action.tool_def_signed
    msg := sprintf("MS-08 deny: MCP tool definitions from %q are not cryptographically signed", [input.action.server])
}

deny contains msg if {
    applicable
    not (input.action.server_registry == "trusted")
    msg := sprintf("MS-08 deny: MCP server %q is not from a trusted registry", [input.action.server])
}

deny contains msg if {
    applicable
    input.action.writes_execution_bearing == true
    msg := sprintf("MS-08 deny: MCP connection %q can write execution-bearing locations (registry launch-command class)", [input.action.server])
}

allow if {
    count(deny) == 0
}
