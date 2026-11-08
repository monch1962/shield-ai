package shield_ai.tp.tool_connection_and_launch_path_integrity

import rego.v1

# SHIELD-AI(TM) TP-16: Tool-Connection and Launch-Path Integrity
# Pillar: TP -- Tool and Pipeline Security
#
# Keep remote peer-supplied protocol metadata (OAuth/discovery/connection fields) out of process-launch and shell execution primitives; origin-bound and validate the authorization endpoint.
#
# Maturity indicators:
#   L1: Tool/connection adapters pass server-supplied transport fields (authorization_endpoint, discovery docs) to a process launcher or shell; no origin comparison.
#   L2: Connection adapters identified and audited for launch-path handoff; URL-scheme checks in place as defence in depth but not sole control.
#   L3: Authorization endpoint origin-bound and validated on canonical value; no transport field crosses into a launch/shell primitive; launch commands allowlisted; connection termination and alert on any violation.
#   L4: Launch-path fail-closed and red-teamed; reconnection and server-hijack scenarios tested; onboarding treats later server compromise as in-threat-model.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.DS)
#   EU AI Act: Art. 14 (Human Oversight)
#   ISM: Guidelines for System Hardening, Application Control

# IMPLEMENTED (v1.20, Nov 2026) -- reference implementation (INC-79 opencode MCP
# OAuth RCE; INC-85 AgentScope registration-time launch; INC-88 MCP protocol
# pivoting / cross-protocol trust; INC-92 peer-agent collaboration surfaces).
# Input model: input.action.kind == "tool_connect" / "tool_launch". Remote
# peer-supplied protocol metadata must never cross into a process-launch or shell
# primitive; the authorization endpoint is origin-bound and validated on its
# canonical value.

deny contains msg if {
    input.action.kind == "tool_connect"
    input.action.connection.transport_metadata_to_launch == true
    msg := sprintf("TP-16 deny: agent %q connection hands server-supplied protocol metadata to a process-launch/shell primitive (code-execution boundary)", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "tool_connect"
    input.action.connection.auth_endpoint_origin_bound == false
    msg := sprintf("TP-16 deny: agent %q authorization endpoint is not origin-bound to the configured server", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "tool_connect"
    input.action.connection.auth_endpoint_validated_canonical == false
    msg := sprintf("TP-16 deny: agent %q accepts the server-advertised authorization endpoint without validating the canonical processed value against the configured origin", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "tool_launch"
    input.action.launch.command_allowlisted == false
    msg := sprintf("TP-16 deny: agent %q launch command registered through a tool/server definition is not on the allowlist", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "tool_launch"
    input.action.launch.model_derived_command == true
    msg := sprintf("TP-16 deny: agent %q auto-launch command is model-influenced or externally derived; a server definition must not register an arbitrary OS command", [input.agent.id])
}

deny contains msg if {
    input.action.kind == "tool_connect"
    input.action.connection.peer_supplied_transport_field_crosses_launch == true
    msg := sprintf("TP-16 deny: agent %q connection has a peer-supplied transport field crossing into an execution/launch primitive; terminated and alerted (fail closed)", [input.agent.id])
}

allow if {
    count(deny) == 0
}