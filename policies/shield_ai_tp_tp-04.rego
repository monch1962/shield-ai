package shield_ai.tp.tool_output_validation

# SHIELD-AI(TM) TP-04: Tool Output Validation
# Pillar: TP -- Tool and Pipeline Security
#
# Validate all tool outputs against known-good schemas before passing to agent context, with content-type verification, size limits, and sandboxed execution for code-generation tools.
#
# Maturity indicators:
#   L1: No tool output validation. Raw tool responses passed to agent context.
#   L2: Basic schema validation on tool outputs. Manual review of violations.
#   L3: Automated schema validation, content-type checking, and sanitisation. Size limits enforced.
#   L4: Sandbox execution for code-generation tools. Automated blocking of invalid outputs.
#
# Regulatory mappings:
#   OWASP LLM Top 10 v2: LLM02 (Insecure Output Handling)
#   NIST AI RMF: MEASURE (ME.AD)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.tp_tp_04
#     msg := sprintf("TP-04 violation: agent %v does not meet control requirements", [agent.id])
# }
