package shield_ai.tp.tool_inventory_and_registry

import rego.v1

# SHIELD-AI(TM) TP-01: Tool Inventory and Registry
# Pillar: TP -- Tool and Pipeline Security
#
# Maintain a central registry of all tools accessible to agents, with security review, versioning, and integration with the authorisation system.
#
# Maturity indicators:
#   L1: No tool registry. Tools documented informally or not at all.
#   L2: Basic tool registry for critical tools. Manual registration.
#   L3: Central tool registry with full metadata. Automated security review. Integration with authorisation.
#   L4: Continuous registry scanning for unregistered tools. Automated deregistration of deprecated tools.
#
# Regulatory mappings:
#   ISM: Guidelines for Gateways
#   NIST AI RMF: IDENTIFY (ID.AM)
#   SOCI Act: CIRMP s.4(c)
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.tool = the tool being invoked. The registry below
# is the demo set; a real deployment replaces it with the organisation's
# approved registry (TP-09 requires explicit registration, no auto-registration).

# Deployment-defined approved registry. Replace with the organisation's set.
registered_tools := {
    "search_documents",
    "send_email_draft",
    "read_calendar",
    "create_meeting",
    "summarise_thread",
    "shell_exec",
    "write_file",
    "install_package",
    "transfer_funds",
}

deny contains "TP-01 deny: action has no tool to check against the registry" if {
    not input.action.tool
}

deny contains msg if {
    tool := input.action.tool
    not tool in registered_tools
    msg := sprintf("TP-01 deny: tool %q is not in the approved tool registry", [tool])
}

allow if {
    count(deny) == 0
}
