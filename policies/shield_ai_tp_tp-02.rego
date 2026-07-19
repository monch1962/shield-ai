package shield_ai.tp.tool_access_control

# SHIELD-AI(TM) TP-02: Tool Access Control
# Pillar: TP -- Tool and Pipeline Security
#
# Enforce per-agent tool allow-lists at invocation time with authenticated agent identity and version-controlled, auditable access policies.
#
# Maturity indicators:
#   L1: Agents can invoke any registered tool. No per-agent access control.
#   L2: Per-agent tool allow-lists. Manual assignment.
#   L3: Tool-level least privilege enforced at invocation time. Agent identity authenticated by tool.
#   L4: Dynamic tool access assignment based on task and risk. Automated revocation on suspicious activity.
#
# Regulatory mappings:
#   OWASP LLM Top 10 v2: LLM08 (Excessive Agency)
#   NIST AI RMF: PROTECT (PR.AC)
#   Essential Eight: Application Control -- extended to tools

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_02
#     msg := sprintf("TP-02 violation: agent %v does not meet control requirements", [agent.id])
# }
