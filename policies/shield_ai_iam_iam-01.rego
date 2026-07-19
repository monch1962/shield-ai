package shield_ai.iam.agent_identity_management

# SHIELD-AI™ IAM-01: Agent Identity Management
# Pillar: IAM — Identity and Access
#
# Ensure every agent has a unique, lifecycle-managed digital identity distinct from human user identities, integrated with the organisation's identity provider.
#
# Maturity indicators:
#   L1: Agents use shared human credentials or no credentials. No agent identity exists.
#   L2: Per-agent service accounts created. Manual lifecycle management.
#   L3: Automated agent identity lifecycle. Integrated with IDP. Agent identities flagged in monitoring.
#   L4: SPIFFE/SPIRE workload identity for every agent. Automated credential rotation. Cross-platform identity federation.
#
# Regulatory mappings:
#   ISM: Guidelines for System Management — identification and authentication
#   Essential Eight: Restrict Administrative Privileges
#   NIST AI RMF: IDENTIFY (ID.AM)

# Default deny
default deny = false

# TODO: Implement control test logic
# Example structure:
#
# deny[msg] {
#     agent := input.agents[_]
#     not agent.iam_iam_01
#     msg := sprintf("IAM-01 violation: agent %v does not meet control requirements", [agent.id])
# }
