package shield_ai.tp.tool_connection_and_launch_pat

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

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_16
#     msg := sprintf("TP-16 violation: agent %v does not meet control requirements", [agent.id])
# }
