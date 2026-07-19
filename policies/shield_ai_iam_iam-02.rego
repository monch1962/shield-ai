package shield_ai.iam.scope_bound_delegation

# SHIELD-AI IAM-02: Scope-Bound Delegation
# Pillar: IAM — Identity and Access
#
# Limit each agent's permissions to the minimum set of tools, data, and actions required for its function, enforced by a policy-as-code engine at invocation time.
#
# Maturity indicators:
#   L1: Agents have the same permissions as the initiating human. No scope boundaries.
#   L2: Agent permissions manually scoped to a subset of human permissions. Static tool allow-lists.
#   L3: Policy-as-code engine enforces per-agent scope at invocation time. Bounded delegation in multi-agent architectures.
#   L4: Dynamic scope adjustment based on context and risk. Continuous verification of scope compliance.
#
# Regulatory mappings:
#   OWASP LLM Top 10 v2: LLM08 (Excessive Agency)
#   NIST AI RMF: GOVERN (GV.AC)
#   Essential Eight: Restrict Administrative Privileges, User Application Hardening
#   SOCI Act: CIRMP s.4(b)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.iam_iam_02
#     msg := sprintf("IAM-02 violation: agent %v does not meet control requirements", [agent.id])
# }
