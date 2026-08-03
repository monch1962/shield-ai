package shield_ai.tp.explicit_tool_registration

# SHIELD-AI(TM) TP-09: Explicit Tool Registration
# Pillar: TP -- Tool and Pipeline Security
#
# Eliminate implicit tool exposure in agent frameworks.
#
# Maturity indicators:
#   L1: Frameworks auto-expose internal functions; no registry enforcement.
#   L2: Explicit registry for critical tools; auto-registration partially disabled.
#   L3: Auto-registration disabled by default; all callables audited; unregistered callables blocked.
#   L4: Continuous callable-audit in CI/CD; automated blocking of implicitly exposed tools.
#
# Regulatory mappings:
#   OWASP: LLM08 (Excessive Agency)
#   NIST AI RMF: IDENTIFY (ID.AM)
#   EU AI Act: Art. 15(b)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_09
#     msg := sprintf("TP-09 violation: agent %v does not meet control requirements", [agent.id])
# }
